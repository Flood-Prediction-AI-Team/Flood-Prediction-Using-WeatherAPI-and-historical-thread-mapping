from flask import Flask, request, jsonify
import pandas as pd
import joblib
import math
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Set absolute paths so VS Code doesn't lose the files
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ==========================================
# TIER 3: SERVICES AND DATA
# ==========================================

class LocationQuery:
    def __init__(self, city_name):
        self._city_name = city_name
        self._latitude = None
        self._longitude = None

    def geocode_city(self):
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={self._city_name}&format=json&limit=1"
            headers = {'User-Agent': 'FloodPredictionApp/1.0'}
            response = requests.get(url, headers=headers).json()
            if response:
                self._latitude = float(response[0]['lat'])
                self._longitude = float(response[0]['lon'])
                return True
        except Exception as e:
            print(f"Geocoding failed: {e}")
        return False

    def get_coordinates(self):
        return (self._latitude, self._longitude)


class WeatherAPIService:
    def __init__(self):
        # Securely loading your real API key from the .env file
        self._api_key = os.getenv("WEATHER_API_KEY") 
        self._endpoint_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_live_weather(self, lat, lon):
        if not self._api_key:
            print("WARNING: WEATHER_API_KEY not found in .env file!")
            return self.execute_mock_fallback()
            
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self._api_key,
                'units': 'metric'
            }
            response = requests.get(self._endpoint_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                rain_1h = data.get('rain', {}).get('1h', 0.0)
                return {
                    "live_rain_mm": rain_1h,
                    "humidity_pct": data['main']['humidity'],
                    "wind_speed_ms": data['wind']['speed']
                }
            print(f"Weather API Error: {data}")
            return self.execute_mock_fallback()
        except Exception as e:
            print(f"Weather Request Failed: {e}")
            return self.execute_mock_fallback()

    def execute_mock_fallback(self):
        print("API failed. Triggering fallback data (0..1 Multiplicity).")
        return {"live_rain_mm": 0.0, "humidity_pct": 50.0, "wind_speed_ms": 3.0}


class HistoricalDatabase:
    def __init__(self):
        # Bulletproof path resolving
        self._dataset_path = BASE_DIR / "Merged_dataset" / "fused_historical_database.csv"
        try:
            self._historical_data = pd.read_csv(self._dataset_path)
            print(f"Database loaded successfully: {len(self._historical_data)} records.")
        except Exception as e:
            print(f"CRITICAL: Could not load historical CSV at {self._dataset_path}. Error: {e}")
            self._historical_data = pd.DataFrame() 

    def calculate_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371.0 
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_past_floods_100km(self, lat, lon):
        if self._historical_data.empty:
            return 0, 999.0
        
        distances = []
        for idx, row in self._historical_data.iterrows():
            dist = self.calculate_haversine(lat, lon, row['Centroid_Y'], row['Centroid_X'])
            distances.append(dist)
            
        self._historical_data['distance_km'] = distances
        floods_100km = self._historical_data[self._historical_data['distance_km'] <= 100]
        
        count = len(floods_100km)
        min_dist = min(distances) if distances else 999.0
        return count, min_dist


class MLPredictor:
    def __init__(self):
        # Bulletproof path resolving
        self._model_weights = BASE_DIR / "flood_model.pkl"
        self._model = None
        self.load_model()

    def load_model(self):
        try:
            self._model = joblib.load(self._model_weights)
            print("Random Forest Model loaded successfully.")
            return True
        except Exception as e:
            print(f"CRITICAL: Failed to load model at {self._model_weights}. Error: {e}")
            return False

    def predict_risk_level(self, feature_df):
        if self._model:
            pred = self._model.predict(feature_df)[0]
            mapping = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
            return mapping.get(pred, "Unknown")
        return "Model Offline"


# ==========================================
# TIER 2: CONTROLLERS
# ==========================================

class DataFusionEngine:
    def __init__(self):
        pass

    def orchestrate_pipeline(self, lat, lon):
        weather_service = WeatherAPIService()
        live_data = weather_service.fetch_live_weather(lat, lon)

        db = HistoricalDatabase()
        flood_count, nearest_km = db.get_past_floods_100km(lat, lon)

        feature_df = pd.DataFrame({
            'live_rain_mm': [live_data['live_rain_mm']],
            'humidity_pct': [live_data['humidity_pct']],
            'wind_speed_ms': [live_data['wind_speed_ms']],
            'past_floods_100km': [flood_count],
            'nearest_flood_km': [nearest_km]
        })

        predictor = MLPredictor()
        risk_level = predictor.predict_risk_level(feature_df)

        return {
            "latitude": lat,
            "longitude": lon,
            "live_weather": live_data,
            "historical_floods_nearby": flood_count,
            "nearest_historical_flood_km": round(nearest_km, 2),
            "risk_level": risk_level
        }


class PredictionController:
    def __init__(self):
        self._flask_app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        @self._flask_app.route("/predict", methods=['GET'])
        def predict_route():
            city = request.args.get('city')
            if not city:
                return self._return_error_response(400)
            return jsonify(self.handle_predict_route(city))

    def handle_predict_route(self, city):
        location = LocationQuery(city)
        if location.geocode_city():
            lat, lon = location.get_coordinates()
            engine = DataFusionEngine()
            return engine.orchestrate_pipeline(lat, lon)
        return self._return_error_response(404)

    def _return_error_response(self, code):
        errors = {
            400: {"error": "City parameter is missing"},
            404: {"error": "City could not be geocoded"}
        }
        return errors.get(code, {"error": "Unknown error"})

    def run(self):
        self._flask_app.run(debug=True, use_reloader=False, port=5000)


# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    app_controller = PredictionController()
    app_controller.run()