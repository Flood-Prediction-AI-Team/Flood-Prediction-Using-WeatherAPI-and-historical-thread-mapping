# Real-Time Flood Risk AI Prediction System 🌊

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-orange?logo=scikit-learn)
![Leaflet](https://img.shields.io/badge/GIS-Leaflet.js-199900?logo=leaflet)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-black?logo=vercel)
![MkDocs](https://img.shields.io/badge/Docs-MkDocs%20Material-indigo)

**Course Project for UCS503 — Software Engineering**  
**Thapar Institute of Engineering and Technology (TIET), Patiala**

🌐 **[Launch Live Web Dashboard (Vercel)](https://flood-risk-ai-chi.vercel.app/)**  
📖 **[View Full Project Documentation (GitHub Pages)](https://Flood-Prediction-AI-Team.github.io/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/)**

---

## 📖 Project Overview

Traditional flood prediction models often rely solely on static geographical records, while modern weather APIs provide real-time atmospheric metrics without historical disaster context.

The **Real-Time Flood Risk AI Prediction System** is a deployed full-stack machine learning application that bridges this gap. It dynamically fuses live meteorological telemetry with spatial proximity analysis of historical flood centroids to classify localized flood risk in real time.

### Key Capabilities
- **Real-Time Telemetry & Geocoding:** Resolves any global city or region and fetches live temperature (`°C`), humidity (`%`), wind speed (`m/s`), and 1-hour precipitation (`mm`) via OpenWeatherMap APIs (with automatic fallback resilience).
- **100 km Haversine Spatial Threat Indexing:** Computes geodesic distances against historical disaster records to quantify past flood occurrences within a `100 km` radius and pinpoint the nearest historical flood epicenter.
- **ML Risk Classification:** Uses a trained **Random Forest Classifier** (`flood_model.pkl`) cached in memory for low-latency serverless inference across **Low Risk**, **Medium Risk**, and **High Risk** tiers.
- **Interactive GIS Visualization:** Features a dark glassmorphism HUD overlaid on an interactive **Leaflet.js** map that flies to searched coordinates and renders a color-coded `50 km` threat radius indicator.

---

## 🏗️ Architecture Pipeline

The system follows a decoupled 3-tier architecture deployed on **Vercel's serverless Python runtime**:

1. **Geocoding & Ingestion (`LocationQuery` & `WeatherAPIService`):** The frontend sends a relative `/predict?city=<query>` request to Flask. The backend resolves coordinates via the OpenWeatherMap Geocoding API (falling back to OpenStreetMap Nominatim) and retrieves live atmospheric conditions.
2. **Spatial Indexing (`HistoricalDatabase`):** Using the Haversine formula, the backend calculates distances from the target coordinates to all centroids in `fused_historical_database.csv`, returning the `100 km` historical flood count and nearest epicenter distance (`km`).
3. **Feature Fusion (`DataFusionEngine`):** Combines live meteorological inputs and historical spatial metrics into a 5-feature vector (`live_rain_mm`, `humidity_pct`, `wind_speed_ms`, `past_floods_100km`, `nearest_flood_km`), while passing live temperature (`temp_c`) directly to the UI telemetry panel.
4. **ML Inference (`MLPredictor`):** Evaluates the fused feature vector using the preloaded Scikit-Learn Random Forest model (`flood_model.pkl`) to output the risk classification.
5. **Interactive Frontend (`templates/index.html` & `static/`):** Flask renders the dashboard and returns JSON telemetry to `script.js`, updating the weather cards, historical threat metrics, risk status badge, and Leaflet map marker/radius.

---

## 📊 Datasets & Model Training

- **Historical Threat Database (`fused_historical_database.csv`):** Consolidated geospatial flood records derived from the **Dartmouth Flood Observatory (DFO)** master list, storing verified flood centroids (`Centroid_X`, `Centroid_Y`) for real-time Haversine proximity queries.
- **Balanced & Synthetic Overlapping Training Data (`fused_historical_database_balanced.csv`):** Combines historical flood events with baseline normal weather observations (`daily_weather.parquet`) and Gaussian-noise boundary overlap so the Random Forest classifier learns multi-variable meteorological + spatial interactions rather than memorizing rigid thresholds.

---

## 📂 Repository Structure

```text
.
├── .github/                                       # GitHub Actions & MkDocs CI/CD workflows
├── .vscode/                                       # Local VS Code workspace configurations
├── assets/                                        # Global project assets, banners, and logos
├── Code/                                          # Production application & ML source code (Vercel Root)
│   ├── Frontend/                                  # Standalone frontend reference files
│   ├── Merged_dataset/                            # Historical & balanced flood datasets
│   │   ├── normal_dataset/                        # Baseline city, country, and parquet weather data
│   │   ├── dataset_fusion.ipynb                   # Spatial-temporal dataset merging notebook
│   │   ├── dfo_masterlist.csv                     # Dartmouth Flood Observatory (DFO) records
│   │   ├── fused_historical_database.csv          # Production spatial lookup database
│   │   ├── fused_historical_database_balanced.csv # Class-balanced training dataset
│   │   └── historical_dataset.csv                 # Consolidated historical flood archive
│   ├── public/                                    # Static mirror assets
│   ├── static/                                    # Production CSS & JS served by Flask
│   │   ├── script.js                              # Relative /predict API client & Leaflet map logic
│   │   └── style.css                              # Glassmorphism HUD & responsive dashboard styling
│   ├── templates/                                 # Flask HTML templates
│   │   └── index.html                             # Main real-time prediction dashboard UI
│   ├── .env                                       # Local API credentials (Git ignored)
│   ├── .vercelignore                              # Excludes heavy training datasets & notebooks from deploy
│   ├── app.py                                     # Vercel WSGI serverless entrypoint
│   ├── backend.py                                 # 3-Tier Flask API, OpenWeather service & ML inference
│   ├── flood_model.pkl                            # Trained Random Forest classifier (scikit-learn 1.9.0)
│   ├── requirements.txt                           # Pinned Python dependencies for Vercel
│   └── train_model.ipynb                          # Model training, synthetic noise & evaluation notebook
├── Docs/                                          # Complete UCS503 documentation & submission artifacts
│   ├── Diagrams/                                  # 8 UML & system architecture diagrams (dedicated folders)
│   ├── Gantt Chart/                               # Project schedule & milestone tracker (.xlsx)
│   ├── journals/                                  # Individual weekly progress journals (Markdown)
│   ├── project-report-final/                      # Final project report (LaTeX & PDF)
│   ├── project-report-prototype-stage/            # Prototype stage report & slides (LaTeX & PDF)
│   ├── Flood_Prediction_System.pptx.pdf           # Project presentation slides (PDF)
│   ├── Flood_Risk_AI_Test_Cases.pdf               # Software verification & test cases suite
│   └── index.md                                   # MkDocs documentation homepage
├── Research Proposal/                             # Academic proposal document & slides (LaTeX & PDF)
├── site/                                          # Compiled MkDocs static site (Git ignored)
├── .gitattributes                                 # Git line-ending attributes
├── .gitignore                                     # Git tracking exclusions (.env, __pycache__, site/)
├── mkdocs.yml                                     # MkDocs Material static site configuration
└── README.md                                      # Repository overview (You are here)
```

---

## 🚀 Running Locally

1. **Clone the repository and navigate to `Code/`:**
   ```bash
   git clone [https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping.git](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping.git)
   cd Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/Code
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your OpenWeatherMap API key:**
   Create a `.env` file inside `Code/`:
   ```env
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```

4. **Start the Flask server:**
   ```bash
   python backend.py
   ```
   Open **`http://127.0.0.1:5000`** in your browser to use the dashboard locally.

---

## 👥 Project Team

| Name | Roll Number | Contributions |
| :--- | :--- | :--- |
| **Amit Bishnoi** | `1024240005` | Backend Architecture (`backend.py`, `app.py`), ML Training (`flood_model.pkl`), Frontend Dashboard, MkDocs Portal & Vercel Deployment |
| **Diksha Garg** | `1024240015` | Data Cleaning & Fusion (`Merged_dataset/`), Haversine Spatial Indexing, UML & Architecture Diagrams, LaTeX Reports, Gantt Chart & Leaflet Integration |