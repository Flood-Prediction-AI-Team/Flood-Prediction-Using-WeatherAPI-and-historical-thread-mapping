from flask import Flask, request, jsonify
import pandas as pd
import pickle
import math

# ==========================================
# TIER 3: SERVICES AND DATA
# ==========================================

class LocationQuery:
    def __init__(self, city_name):
        self._city_name = city_name
        self._latitude = None
        self._longitude = None

    def geocode_city(self):
        # TODO: Implement geocoding API logic here
        self._latitude = 30.3398  # Example coordinates for Patiala
        self._longitude = 76.3869
        return True

    def get_coordinates(self):
        return (self._latitude, self._longitude)


class WeatherAPIService:
    def __init__(self):
        self._api_key = "YOUR_OPENWEATHER_KEY"
        self._endpoint_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_live_weather(self, lat, lon):
        try:
            # TODO: Add requests.get() logic here
            return {"temp": 28.5, "humidity": 80, "rainfall": 15.2}
        except Exception:
            return self.execute_mock_fallback(lat, lon)

    def execute_mock_fallback(self, lat, lon):
        print("API failed or timed out. Triggering fallback data (0..1 Multiplicity condition).")
        return {"temp": 30.0, "humidity": 75, "rainfall": 10.0}


class HistoricalDatabase:
    def __init__(self):
        self._dataset_path = "fused_historical_database.csv"
        # self._historical_data = pd.read_csv(self._dataset_path)

    def calculate_haversine(self, lat1, lon1, lat2, lon2):
        # TODO: Add Haversine math formula here
        return 45.5 

    def get_past_floods_100km(self, lat, lon):
        # TODO: Filter self._historical_data based on distance
        return 3  # Example: 3 past floods found in radius


class MLPredictor:
    def __init__(self):
        self._model_weights = "flood_model.pkl"
        self._random_forest = None
        self.load_model()

    def load_model(self):
        # with open(self._model_weights, 'rb') as f:
        #     self._random_forest = pickle.load(f)
        return True

    def predict_risk_level(self, feature_vector):
        # prediction = self._random_forest.predict([feature_vector])
        return "High Risk"


# ==========================================
# TIER 2: CONTROLLERS
# ==========================================

class DataFusionEngine:
    def __init__(self):
        self._feature_vector = []
        self._confidence_score = 0.0

    def normalize_data(self, weather, spatial_count):
        # Combine API data and DB counts into a single array for the ML model
        return [weather['temp'], weather['humidity'], weather['rainfall'], spatial_count]

    def orchestrate_pipeline(self, lat, lon):
        # 1. Fetch live data
        weather_service = WeatherAPIService()
        live_data = weather_service.fetch_live_weather(lat, lon)

        # 2. Query history
        db = HistoricalDatabase()
        flood_count = db.get_past_floods_100km(lat, lon)

        # 3. Fuse features
        self._feature_vector = self.normalize_data(live_data, flood_count)

        # 4. Execute model
        predictor = MLPredictor()
        risk_level = predictor.predict_risk_level(self._feature_vector)

        return {
            "latitude": lat,
            "longitude": lon,
            "live_weather": live_data,
            "historical_floods_nearby": flood_count,
            "risk_level": risk_level
        }


class PredictionController:
    def __init__(self):
        self._flask_app = Flask(__name__)
        self._api_endpoint = "/predict"
        self._setup_routes()

    def _setup_routes(self):
        @self._flask_app.route(self._api_endpoint, methods=['GET'])
        def predict_route():
            city = request.args.get('city')
            if not city:
                return self._return_error_response(400)
            return jsonify(self.handle_predict_route(city))

    def handle_predict_route(self, city):
        # Validate location
        location = LocationQuery(city)
        if location.geocode_city():
            lat, lon = location.get_coordinates()
            
            # Trigger Fusion Engine
            engine = DataFusionEngine()
            result = engine.orchestrate_pipeline(lat, lon)
            return result
        return self._return_error_response(404)

    def _return_error_response(self, code):
        errors = {
            400: {"error": "City parameter is missing"},
            404: {"error": "City not found"}
        }
        return errors.get(code, {"error": "Unknown error"})

    def run(self):
        self._flask_app.run(debug=True, port=5000)


# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    app_controller = PredictionController()
    app_controller.run()