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

The **Real-Time Flood Risk AI Prediction System** is a full-stack engineering platform that bridges this gap. It creatively fuses static historical disaster centroids with live meteorological data to compute dynamic, localized flood risks. By coupling live OpenWeatherMap API ingestion with geospatial proximity queries (Haversine formula), the platform constructs normalized feature vectors to perform multi-class risk classification using a trained **Random Forest** model.

👉 **[View Full Project Documentation & System Architecture Here](https://Flood-Prediction-AI-Team.github.io/Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping/)**

---

## ✨ Key Features

* **Real-Time Data Ingestion:** Asynchronous REST API integration fetching live temperature, humidity, wind speed, and precipitation data.
* **Geospatial Threat Indexing:** Real-time Haversine distance evaluation connecting queried coordinates to the nearest recorded flood epicenters within a 100km radius.
* **Machine Learning Inference:** A Random Forest classification model trained on engineered multi-variable weather distributions with synthetic overlapping thresholds to prevent overfitting.
* **Dynamic Visualization:** Interactive HTML/JS dashboard featuring a responsive Leaflet.js map displaying threat radii and geolocated risk zones.
* **Reliability Architecture:** Automatic graceful fallback handling that generates localized mock weather data to ensure continuous operation during third-party API rate limits.

---

## 🛠️ Tech Stack

* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
* **Backend:** Python, Flask, Flask-CORS, python-dotenv
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Leaflet.js
* **APIs:** OpenWeatherMap API, OpenStreetMap Nominatim
* **Documentation:** MkDocs (Material Theme), Mermaid.js (Draw.io)

---

## 📂 Repository Structure

```text
.
├── Code/                          # Core application source code
│   ├── Merged_dataset/            # Raw and fused historical CSV datasets
│   ├── backend.py                 # Flask server and API ingestion routing
│   ├── feature_engineering.py     # Data fusion and preprocessing scripts
│   ├── index.html                 # Frontend user dashboard
│   ├── script.js                  # Frontend logic and Leaflet map rendering
│   ├── style.css                  # UI styling and responsive design
│   ├── train_model.ipynb          # ML training, data synthesis, and evaluation
│   └── .env                       # Environment variables (API Keys)
├── Docs/                          # Markdown documentation for MkDocs
│   ├── assets/                    # Images, logos, and stylesheets
│   └── index.md                   # Documentation homepage
├── mkdocs.yml                     # Static site generator configuration
├── README.md                      # Repository overview (You are here)
└── .gitignore                     # Git tracking exclusions