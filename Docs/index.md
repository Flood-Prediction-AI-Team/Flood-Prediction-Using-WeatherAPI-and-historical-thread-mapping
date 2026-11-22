<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
  <img src="https://raw.githubusercontent.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/main/assets/tiet-logo.png" alt="TIET Logo" style="height: 46px; width: auto; margin: 0;">
  <div style="line-height: 1.4;">
    <strong>UCS503: Software Engineering (Project)</strong><br>
    <strong>Thapar Institute of Engineering &amp; Technology, Patiala</strong>
  </div>
</div>

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
```

Open your browser and navigate to: **`http://127.0.0.1:5500/Code/Frontend/index.html`**

### 2. Live Evaluation Demonstration Scenarios

=== "🟢 Scenario 1: Clear Weather & Low Historical Proximity"
    * **Test Target:** `Delhi` or `Patiala` (During dry atmospheric conditions)
    * **Live Telemetry:** Low precipitation (`0 mm`), moderate humidity (`~38%`), normal wind speed (`~1.1 m/s`).
    * **Spatial Context:** Few or distant historical epicenters (`> 100 km`).
    * **Flood-Risk AI Output:** Classifies as **LOW RISK** (Green HUD theme + 50 km green map perimeter), confirming atmospheric metrics remain within normal safety bounds.

=== "🟡 Scenario 2: Elevated Rainfall in Moderate-Risk Basin"
    * **Test Target:** Regional monsoon belt cities (e.g., `Guwahati` or `Patna`)
    * **Live Telemetry:** Moderate rainfall (`15–45 mm/hr`) with high relative humidity (`> 80%`).
    * **Spatial Context:** Multiple historical DFO flood events recorded within the 100 km radius.
    * **Flood-Risk AI Output:** Elevates alert status to **MEDIUM RISK** (Amber HUD theme + 50 km amber map zone) due to compound precipitation and historical terrain vulnerability.

=== "🔴 Scenario 3: Extreme Precipitation Near Historical Epicenter"
    * **Test Target:** High-severity flood zones during heavy storm activity (e.g., `Sylhet` or `Koshi Basin, Nepal`)
    * **Live Telemetry:** Heavy rainfall (`> 50 mm/hr`), saturated humidity (`> 85%`), high wind velocity.
    * **Spatial Context:** High count of past floods within 100 km and close epicenter proximity (`< 50 km`).
    * **Flood-Risk AI Output:** Flags **HIGH RISK** (Red HUD theme + 50 km red threat ring), warning of high probability of flash or riverine flooding.

=== "🌐 Scenario 4: Global City & Coordinate Querying"
    * Enter any city name worldwide into the top-left glassmorphic search bar and press **SEARCH** (or hit `Enter`).
    * Watch Leaflet.js smoothly fly to the target coordinates, drop an interactive threat popup, and populate both **Live Weather (API)** and **Historical Threat (DFO)** panels in real time.

---

## 📐 Formal Software Engineering & Architectural Deliverables

All project documentation, research proposals, and prototype reports are maintained in the repository:

| Deliverable | Description | Format & Access Link |
| :--- | :--- | :--- |
| **Research Proposal** | Problem formulation, literature review, and dual-source data fusion methodology | [:material-folder-open: View Research Proposal](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/tree/main/Research%20Proposal) |
| **Mid-Semester Prototype Report** | System architecture, data cleaning pipeline, and initial Random Forest evaluation | [:material-folder-open: View Prototype Deliverables](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/tree/main/project-report-prototype-stage) |
| **Final Project Report** | Comprehensive software engineering documentation, UML models, and final benchmarks | [:material-folder-open: View Final Report](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/tree/main/project-report-final) |
| **Data Fusion Notebook (`dataset_fusion.ipynb`)** | DFO + EM-DAT relational merging and memory-safe PyArrow Parquet weather balancing | [:material-notebook: View Fusion Notebook](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/blob/main/Code/Merged_dataset/dataset_fusion.ipynb) |
| **ML Training Pipeline (`train_model.ipynb`)** | Feature engineering, Random Forest training, validation, and `.pkl` serialization | [:material-notebook: View Training Notebook](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/blob/main/Code/train_model.ipynb) |
| **Flask Inference API (`backend.py`)** | Live OpenWeatherMap integration, Haversine spatial indexing, and `/predict` endpoint | [:material-language-python: View Backend Code](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/blob/main/Code/backend.py) |

---

## 📅 Project Roadmap & Development Phases

| Phase | Milestone / Engineering Objectives | Timeline | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1: Inception & Research** | Problem Definition, DFO & EM-DAT Dataset Acquisition, Repository & Git Workflow Setup | Aug 2026 | **Completed** |
| **Phase 2: Data Fusion & Balancing** | Country/Date Normalization, Inner-Join Merging (`1,548` events), PyArrow Parquet Normal Weather Balancing (`2,548` rows) | Sep 2026 | **Completed** |
| **Phase 3: ML Modeling & Backend API** | Random Forest Classifier Training (`flood_model.pkl`), Flask REST API, Haversine 100 km Spatial Indexing | Oct 2026 | **Completed** |
| **Phase 4: GIS Dashboard & UI Polish** | Leaflet.js Full-Screen Map, Compact Glassmorphism Cards, Live OpenWeather Telemetry Integration | Nov 2026 | **Completed** |
| **Phase 5: Cloud Deployment & Final Defense** | Render.com Gunicorn Production Hosting, MkDocs GitHub Pages Portal, Final Report & Defense | Nov 2026 | **Active Milestone** |

---

<p align="center">
  <b>Flood-Risk AI</b> • Real-Time Flood Prediction & Threat Mapping System • Academic Year 2026–27<br>
  <i>Thapar Institute of Engineering and Technology, Patiala</i>
</p>