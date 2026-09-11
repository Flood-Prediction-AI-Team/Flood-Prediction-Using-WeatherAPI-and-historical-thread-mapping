import os
import requests
import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

# 1. Initialization and Configurations
# Load environment variables from the .env file securely
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)
CORS(app) # Enables frontend-backend communication

# 2. Load the Machine Learning Model
try:
    model = joblib.load("flood_model.pkl")
    print("✅ ML Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading ML model: {e}")

# 3. Load the Historical Database
db_path = "Merged_dataset/fused_historical_database.csv"
try:
    historical_df = pd.read_csv(db_path)
    print("✅ Historical database loaded successfully.")
except Exception as e:
    print(f"❌ Error loading historical database: {e}")

# 4. Geospatial Logic: Haversine Distance
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates the geodesic distance in kilometers between two GPS coordinates."""
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# 5. Core API Endpoint
@app.route('/predict', methods=['GET'])
def predict_risk():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "No city provided"}), 400

    # Step A: Fetch Live Weather from OpenWeatherMap API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch weather data. API returned {response.status_code}"}), 404
        
    weather = response.json()
    target_lat = weather['coord']['lat']
    target_lon = weather['coord']['lon']
    
    temp = weather['main']['temp']
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    # Extract 1-hour rain volume if available, otherwise default to 0.0
    rain_1h = weather.get('rain', {}).get('1h', 0.0)

    # Step B: Calculate Real Spatial Proximity to Historical Floods
    historical_df['Distance_km'] = haversine_distance(
        target_lat, target_lon, 
        historical_df['Centroid_Y'], historical_df['Centroid_X']
    )
    
    # Calculate localized threat metrics (within 100km radius)
    floods_in_radius = historical_df[historical_df['Distance_km'] <= 100.0]
    past_floods_100km = len(floods_in_radius)
    nearest_flood_km = historical_df['Distance_km'].min()

    # Step C: Build the ML Feature Vector
    # The column names must perfectly match the ones used in train_model.ipynb
    features = pd.DataFrame([{
        'live_rain_mm': rain_1h,
        'humidity_pct': humidity,
        'wind_speed_ms': wind_speed,
        'past_floods_100km': past_floods_100km,
        'nearest_flood_km': nearest_flood_km
    }])

    # Step D: Execute ML Inference
    prediction = model.predict(features)[0]
    
    # Map numeric classes to categorical risk labels
    risk_labels = {0: "LOW RISK", 1: "MEDIUM RISK", 2: "HIGH RISK"}
    risk_text = risk_labels.get(prediction, "UNKNOWN RISK")
    
    # Step E: Construct and Return the Final JSON Response
    return jsonify({
        "city": city,
        "lat": target_lat,
        "lon": target_lon,
        "temperature": f"{temp}°C",
        "humidity": f"{humidity}%",
        "wind_speed": f"{wind_speed} m/s",
        "rain": f"{rain_1h} mm",
        "past_floods": past_floods_100km,
        "nearest_flood": f"{nearest_flood_km:.1f} km",
        "risk_level": risk_text
    })

if __name__ == '__main__':
    # Run the Flask server on port 5000
    app.run(debug=True, port=5000)