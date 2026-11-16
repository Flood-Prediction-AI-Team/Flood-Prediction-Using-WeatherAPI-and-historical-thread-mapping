![TIET Logo](assets/tiet-logo.svg){ .tiet-logo }

**UCS503: Software Engineering (Project)**  
**Thapar Institute of Engineering & Technology, Patiala**

# 🌊 Flood-Risk AI: Real-Time Flood Prediction & Threat Mapping System
### *Dual-Source Meteorological Ingestion, Geospatial Haversine Indexing & Random Forest Inference Platform*

<div class="badges" markdown>
[![Prototype Status](https://img.shields.io/badge/Prototype-Active-brightgreen?style=flat-square)](#interactive-prototype-demonstration)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3%20%2F%20Leaflet.js-199900?style=flat-square&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Backend](https://img.shields.io/badge/Backend-Python%20%2F%20Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![ML Engine](https://img.shields.io/badge/ML%20Engine-Scikit--Learn%20%2F%20Random%20Forest-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Data Fusion](https://img.shields.io/badge/Data%20Fusion-DFO%20%2B%20EM--DAT%20%2B%20OpenWeather-09A3D5?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping)
</div>

---

## 👥 Academic & Team Profile

| Role | Team Member | Roll Number | Department |
| :--- | :--- | :--- | :--- |
| **ML Pipeline, Data Fusion & Backend Lead** | **Amit Bishnoi** | `1024240005` | Computer Science & Engineering (AIML) |
| **Frontend GIS Visualization & Documentation Lead** | **Diksha Garg** | `1024240015` | Computer Science & Engineering (AIML) |

- **Academic Supervisor & Lab Instructor:** **Dr. Jeelani Asif** (Department of Computer Science & Engineering, TIET Patiala)
- **Course Code:** UCS503P — Software Engineering Project (Academic Year 2026–27 ODD)
- **GitHub Repository:** [Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping)

---

## 📌 Executive Overview

Traditional flood risk assessment models rely almost exclusively on static topographical and historical datasets, failing to adapt when sudden extreme precipitation events occur. Conversely, modern meteorological APIs provide live atmospheric telemetry (temperature, humidity, wind speed, rainfall) but lack awareness of whether a region has historically saturated terrain, vulnerable river basins, or recurring flood epicenters.

!!! abstract "The Real-Time Threat Assessment Problem"
    There is a critical operational gap between **live meteorological telemetry** and **historical geospatial vulnerability**. Identical rainfall volumes (e.g., 80 mm/hr) may cause zero disruption in well-drained arid regions while triggering catastrophic flash flooding in historically flood-prone basins.

**Flood-Risk AI** bridges this gap through an automated, real-time geospatial inference pipeline:
1. **Live Meteorological Ingestion:** Queries the OpenWeatherMap REST API in real time for target city coordinates, temperature, humidity, wind velocity, and 1-hour precipitation volume.
2. **Geospatial Haversine Indexing:** Computes exact great-circle distances between the queried location and fused historical disaster centroids (Dartmouth Flood Observatory & EM-DAT) to count past floods within a **100 km radius** and locate the nearest epicenter.
3. **Random Forest Risk Classification:** Evaluates the fused live-and-historical feature vector via a balanced **Scikit-Learn Random Forest Classifier** to output an actionable **LOW RISK, MEDIUM RISK, or HIGH RISK** classification rendered on an interactive Leaflet.js map.

---

## ✨ Key Platform Capabilities

<div class="grid cards" markdown>

-   :material-weather-pouring: **Live OpenWeatherMap API Telemetry**

    ---

    Fetches real-time atmospheric parameters (`temp_c`, `humidity_pct`, `wind_speed_ms`, `live_rain_mm`) and geocoded coordinates for any queried city or region worldwide, with graceful error handling and fallback resilience.

-   :material-map-marker-radius: **Geospatial Haversine Threat Indexing**

    ---

    Executes geodesic distance calculations across fused historical flood records to quantify localized flood frequency within a **100 km buffer zone** and pinpoint the exact distance (in km) to the nearest historical flood epicenter.

-   :material-database-sync: **Multi-Source Historical & Normal Weather Fusion**

    ---

    Combines **DFO (Dartmouth Flood Observatory)** spatial centroids with **EM-DAT** disaster records and balanced baseline daily weather observations (`fused_historical_database_balanced.csv`) to prevent class imbalance and boundary overfitting.

-   :material-forest: **Balanced Random Forest Risk Classifier**

    ---

    Trains an ensemble decision-tree classifier across 5 core environmental and spatial features (`live_rain_mm`, `humidity_pct`, `wind_speed_ms`, `past_floods_100km`, `nearest_flood_km`) to distinguish safe weather from compound flood threats.

-   :material-map-search: **Interactive Glassmorphism GIS Dashboard**

    ---

    Features a full-viewport **Leaflet.js** map with automated `flyTo` camera transitions, dynamic 50 km color-coded threat radius overlays, and compact frosted-glass HUD cards displaying live weather, historical threat metrics, and ML verdicts.

-   :material-cloud-check: **Cloud-Ready REST API Architecture**

    ---

    Decoupled Flask + Gunicorn REST backend (`/predict?city=<name>`) with CORS enabled, engineered for zero-downtime deployment on Render.com and seamless integration with static frontends.

</div>

---

## 🏗️ System Architecture & Layered Decomposition

Flood-Risk AI decouples geospatial map visualization, REST API orchestration, spatial indexing, and machine learning inference across 4 modular layers:

<div class="grid cards" markdown>

-   :material-monitor-dashboard: **Presentation & GIS Layer (HTML5 / CSS3 / Leaflet.js)**

    ---

    - Full-screen OpenStreetMap tile viewport with top-right zoom controls and dynamic 50 km risk radius rings.
    - Compact glassmorphism HUD cards displaying Live Weather, Historical Threat (DFO), and ML Risk Prediction.
    - Asynchronous `fetch` client with keyboard (`Enter`) trigger and real-time status feedback.

-   :material-server-network: **API Gateway & Orchestration Core (Python / Flask / CORS)**

    ---

    - Stateless `/predict` GET endpoint accepting URL-encoded city queries and returning structured JSON payloads.
    - Coordinates external OpenWeatherMap HTTP requests, Pandas spatial filtering, and serialized `.pkl` model inference.
    - Production-ready WSGI entry point configured for Gunicorn deployment.

-   :material-compass-rose: **Geospatial & Feature Fusion Engine (Pandas / NumPy / Math)**

    ---

    - Vectorized Haversine distance computation against historical flood coordinates (`Centroid_X`, `Centroid_Y`).
    - Extracts 100 km regional flood count, average past severity, recorded casualties, and minimum epicenter proximity.
    - Assembles normalized 5-feature input vectors matching training schema order.

-   :material-brain: **Offline Data Engineering & ML Training Pipeline (Jupyter / Scikit-Learn)**

    ---

    - Inner-joins DFO and EM-DAT datasets on standardized country names, year, and month (`1,548` matched flood events).
    - Integrates `1,000` memory-optimized PyArrow Parquet normal-weather samples (`2,548` total balanced rows).
    - Serializes the trained 100-tree `RandomForestClassifier` into `flood_model.pkl`.

</div>

---

## 📊 Engineering Benchmarks & Verification Metrics

Flood-Risk AI has been evaluated across data fusion integrity, predictive accuracy, and API responsiveness:

| Evaluation Metric | Target Engineering Specification | Achieved Prototype Benchmark | Verification Scope |
| :--- | :--- | :--- | :--- |
| **Classification Accuracy** | ≥ 88.0% | **~90% – 94%** | Stratified 80/20 train-test split across 2,548 fused flood & normal records |
| **End-to-End Inference Latency** | ≤ 2.5 s | **0.8 – 1.9 s** | Live OpenWeatherMap API fetch, Haversine scan, and Random Forest prediction |
| **Fused Dataset Scale** | ≥ 2,000 Records | **2,548 Records** | 1,548 DFO/EM-DAT flood events + 1,000 balanced normal weather samples |
| **Geospatial Indexing Radius** | 100 km Threat Buffer | **Exact Haversine (km)** | Great-circle distance computation across global flood centroids |
| **Parquet Ingestion Memory Footprint** | < 256 MB RAM | **Predicate Pushdown** | Column-pruned & pre-filtered PyArrow loading preventing `ArrowMemoryError` |
| **API Resiliency & CORS** | Zero Cross-Origin Drops | **100% Verified** | Cross-origin JSON delivery between frontend client and Flask/Gunicorn server |

---

## 🚀 Interactive Prototype Demonstration

The Flood-Risk AI dashboard is fully functional and executable locally or via cloud deployment.

### 1. Running the Full-Stack Application Locally

```bash
# 1. Clone the repository
git clone [https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping.git](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping.git)
cd Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/Code

# 2. Install Python backend dependencies
pip install flask flask-cors pandas numpy scikit-learn requests gunicorn

# 3. Start the Flask inference server (Port 5000)
python backend.py

# 4. Launch Frontend
# Open Code/Frontend/index.html using VS Code Live Server (Port 5500)