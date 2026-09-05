import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates the distance in km between two GPS points."""
    R = 6371.0  # Earth radius in kilometers
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def extract_features(city_name, historical_db_path="fused_historical_database.csv"):
    """Fetches live weather, calculates spatial proximity, and builds the feature vector."""
    
    # 1. Fetch Live Weather Data & Coordinates
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data for {city_name}.")
        return None
        
    weather_data = response.json()
    target_lat = weather_data['coord']['lat']
    target_lon = weather_data['coord']['lon']
    
    # Extract antecedent moisture proxy (rain in last 1h if available, else 0)
    rain_1h = weather_data.get('rain', {}).get('1h', 0.0)
    
    # 2. Load Historical Database
    try:
        hist_df = pd.read_csv(historical_db_path)
    except FileNotFoundError:
        print(f"Error: Could not find {historical_db_path}. Ensure it is in the same folder.")
        return None

    # 3. Compute Spatial Proximity Index (Process 4.2)
    # Compare target coordinates against all historical flood centroids
    hist_df['Distance_km'] = haversine_distance(
        target_lat, target_lon, 
        hist_df['Centroid_Y'], hist_df['Centroid_X']
    )
    
    # Calculate proximity metrics (e.g., floods within 100km radius)
    radius_km = 100.0
    floods_in_radius = hist_df[hist_df['Distance_km'] <= radius_km]
    
    past_flood_count = len(floods_in_radius)
    avg_past_severity = floods_in_radius['Severity__'].mean() if past_flood_count > 0 else 0
    min_distance_to_flood = hist_df['Distance_km'].min()

    # 4. Build Final Normalized Feature Vector (Process 4.3)
    feature_vector = pd.DataFrame([{
        'query_location': city_name,
        'temperature_c': weather_data['main']['temp'],
        'humidity_pct': weather_data['main']['humidity'],
        'wind_speed_ms': weather_data['wind']['speed'],
        'live_rain_mm': rain_1h,
        'past_floods_100km': past_flood_count,
        'avg_past_severity': round(avg_past_severity, 2),
        'nearest_flood_km': round(min_distance_to_flood, 2)
    }])
    
    return feature_vector

# --- Execution ---
if __name__ == "__main__":
    print("Extracting features for test location...")
    test_city = "Patiala"
    
    final_features = extract_features(test_city)
    
    if final_features is not None:
        print("\n--- Final ML Feature Vector (Process 4.3 Output) ---")
        print(final_features.to_string(index=False))