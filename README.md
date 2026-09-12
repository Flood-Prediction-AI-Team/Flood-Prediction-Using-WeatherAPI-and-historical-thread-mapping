# Real-Time Flood Risk AI Prediction System 🌊

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikit-learn)
![HTML5/CSS3/JS](https://img.shields.io/badge/Frontend-HTML%2FJS-green)
![MkDocs](https://img.shields.io/badge/Docs-MkDocs-indigo)

**Course Project for UCS503 — Software Engineering**  
**Thapar Institute of Engineering and Technology (TIET), Patiala**

---

## 📖 Project Overview

Traditional flood prediction models often rely solely on static geographical data, while modern weather APIs provide real-time atmospheric metrics but lack historical context. 

The **Real-Time Flood Risk AI Prediction System** is a full-stack engineering platform that bridges this gap. It creatively fuses static historical disaster centroids with live meteorological data to compute dynamic, localized flood risks in real-time.

👉 **[View Full Project Documentation Here](https://Flood-Prediction-AI-Team.github.io/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/)**

---

## 🏗️ Architecture Pipeline

The system follows a decoupled 3-tier architecture utilizing a sequential data fusion pipeline:

1. **Ingestion (Live API):** The user inputs a city into the frontend, triggering a REST API call to OpenWeatherMap to fetch live temperature, humidity, wind speed, and precipitation.
2. **Spatial Indexing (Haversine Logic):** The backend calculates the geodesic distance between the queried coordinates and the centroids of all historical floods, determining the number of past threats within a 100km radius.
3. **Feature Fusion:** Live weather metrics and historical proximity counts are normalized into a single structured Feature Vector.
4. **Prediction Engine (Machine Learning):** A Scikit-Learn Random Forest model evaluates the vector to classify the immediate threat level (Low, Medium, or High Risk).
5. **Visualization (Frontend):** The Flask backend serves the structured JSON response back to the UI, automatically flying a Leaflet.js map to the target coordinates and visualizing the threat radius.

---

## 📊 Datasets Used

The machine learning model is trained on a hybrid data approach to ensure realistic, non-rigid predictions:

* **Historical Threat Database (`fused_historical_database.csv`):** A consolidated dataset containing global disaster centroids, severity indices, and historical occurrence counts used for spatial proximity queries.
* **Synthetic Overlapping Training Data:** Custom-engineered baseline datasets introducing Gaussian noise across weather thresholds. By intentionally overlapping parameters (e.g., mixing high rain with low humidity), the model is forced to rely on complex multi-variable patterns rather than memorizing rigid boundaries, successfully preventing overfitting.

---

## 📂 Repository Structure

```text
.
├── .github/                       # GitHub Actions and workflows
├── .vscode/                       # Local editor configurations
├── assets/                        # Global assets, themes, and logos
├── Code/                          # Core application source code
│   ├── Frontend/                  # User interface files
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── Merged_dataset/            # Raw and fused historical CSV datasets
│   ├── .env                       # Environment variables (API Keys)
│   ├── backend.py                 # Flask server and API ingestion routing
│   ├── feature_engineering.py     # Data fusion and preprocessing scripts
│   ├── train_model.ipynb          # ML training, data synthesis, and evaluation
│   └── README.md                  # Code directory documentation
├── Docs/                          # Markdown documentation for MkDocs
│   ├── Diagrams/                  # Project architecture and workflow diagrams
│   ├── assets/                    # MkDocs specific assets 
│   ├── Flood_Prediction_System.pptx.pdf # Academic presentation slides
│   ├── index.md                   # Documentation homepage
│   └── README.md                  # Docs directory documentation
├── Research Proposal/             # Academic proposal documents
├── site/                          # Compiled MkDocs static site (Git ignored)
├── .gitignore                     # Git tracking exclusions
├── mkdocs.yml                     # Static site generator configuration
└── README.md                      # Repository overview (You are here)