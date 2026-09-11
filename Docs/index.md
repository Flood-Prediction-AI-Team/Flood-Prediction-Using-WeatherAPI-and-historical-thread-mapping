**UCS503: Software Engineering (Project)**  **TIET Patiala**

# Real-Time Flood Risk AI Prediction System

**A Machine Learning & Data Fusion Pipeline for Dynamic Disaster Threat Mapping**

### Course & Instructor Details

| | |
|---|---|
| **Course** | UCS503 — Software Engineering (UCS503P, 2026–27 ODD) |
| **Institute** | Thapar Institute of Engineering and Technology |
| **Instructor** | Dr. Jeelani Asif |
| **Repository** | [Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping](https://github.com/Flood-Prediction-AI-Team/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping) |

### Author

| Name | Roll No. |
|---|---|
| Amit Bishnoi | 1024240005 |
| Diksha Garg | 1024240015 |

---

## Overview
Traditional flood prediction models often rely entirely on static geographical data, while modern weather APIs provide real-time atmospheric metrics but lack historical context. This disconnect makes localized, real-time threat assessment difficult and slow for end-users and emergency responders. 

The Real-Time Flood Risk AI Prediction System bridges this gap by creatively fusing static historical disaster datasets with live meteorological data. Rather than relying on rigid rules, the system:
1. Ingests live atmospheric data via the OpenWeatherMap API.
2. Cross-references the user's location against a historical disaster database using geospatial calculations (Haversine formula).
3. Evaluates the fused data using a trained Random Forest classifier to output a dynamic **Low, Medium, or High Risk** verdict, visualized instantly on a web dashboard.

## Problem Statement
* **Lack of Real-Time Context in Static Models**: Traditional geospatial threat maps do not adapt to sudden, severe weather changes.
* **Lack of Historical Context in Weather APIs**: 80mm of rain might be harmless in one city but cause severe flooding in another with a history of saturated ground and poor drainage.
* **Overfitting in Naive ML Implementations**: Standard models often learn rigid, perfect boundaries for weather metrics, failing to account for the overlapping complexities of real-world climates.

## Proposed Solution

### Pipeline Stages

| Stage | Description |
|---|---|
| **Ingestion** | User coordinates trigger an asynchronous REST API call to OpenWeatherMap to fetch live temperature, humidity, wind speed, and precipitation (1h). |
| **Spatial Indexing** | Calculates the geodesic distance (Haversine formula) between the queried city and the centroids of all historical floods, identifying threat counts within a 100km radius. |
| **Feature Fusion** | Normalizes live API metrics and historical proximity counts into a single formatted Feature Vector DataFrame. |
| **Prediction** | A Scikit-Learn Random Forest model evaluates the vector to classify the immediate threat level (Match, Deviation, or Missing equivalents are mapped to Low/Medium/High Risk). |
| **Visualization** | A Flask backend serves the structured JSON response to a responsive HTML/JS dashboard, automatically flying a Leaflet.js map to the target coordinates and drawing a 50km threat radius. |

### Core Workflow
1. End-user queries a city name in the frontend dashboard.
2. The backend fetches live weather; if the API rate limits are hit, it gracefully falls back to mock weather generation to ensure continuous operation.
3. Spatial indexing calculates proximity to past disasters.
4. The Random Forest model executes inference on the fused data.
5. Results are compiled and rendered visually via interactive UI cards and threat maps.

## Dataset
* **Historical Threat Database**: Fused CSV dataset containing global disaster centroids, severity indices, and past occurrence counts.
* **Synthetic Overlapping Training Data**: Custom-engineered baseline datasets introducing Gaussian noise across weather thresholds to prevent model overfitting and force reliance on multi-variable patterns.

## Tech Stack
* **Machine Learning**: Scikit-Learn (Random Forest), Joblib
* **Data Processing**: Pandas, NumPy
* **Backend Framework**: Python, Flask, Flask-CORS, python-dotenv
* **Frontend/UI**: HTML5, CSS3, JavaScript, Leaflet.js
* **APIs**: OpenWeatherMap REST API, OpenStreetMap Nominatim
* **Documentation**: Markdown, MkDocs (Material Theme), Mermaid.js

## Evaluation Criteria

| Metric | What it measures | Ground truth |
|---|---|---|
| **Classification Accuracy (Primary)** | Agreement between pipeline predictions and test splits | ~88-92% accuracy targeting overlapping environmental variables |
| **API Resiliency** | System uptime during third-party service outages | Successful fallback to mock data generation without UI crashing |
| **Geospatial Precision** | Accuracy of the Haversine distance indexing | Manual validation against known map coordinate distances |

## Project Structure

```text
.
├── Code/                          # Source code for the application
│   ├── Merged_dataset/            # Raw and fused historical CSV datasets
│   ├── backend.py                 # Flask server and API ingestion logic
│   ├── feature_engineering.py     # Data fusion and preprocessing scripts
│   ├── index.html                 # Frontend dashboard
│   ├── script.js                  # UI logic and Leaflet.js map handling
│   ├── style.css                  # Responsive UI styling
│   └── train_model.ipynb          # ML training, data synthesis, and evaluation
├── Docs/                          # Markdown documentation, built via MkDocs
│   └── index.md                   # Project homepage
├── mkdocs.yml                     # Site configuration and theme settings
├── README.md                      # Standard repository overview
└── .gitignore                     # Tracks excluded files and /site build outputs