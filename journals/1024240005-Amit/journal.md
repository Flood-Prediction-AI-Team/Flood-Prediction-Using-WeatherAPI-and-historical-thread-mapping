# Weekly Progress Journal — Amit Bishnoi (Roll No: 1024240005)

**Project Name:** Real-Time Flood Risk AI Prediction System
**Role:** Project Lead, ML Engineer, API & Frontend Developer

---

## Week 1 (Aug 3 - Aug 9): Project Inception & Research
- Guided initial brainstorming sessions with Diksha to finalize the concept of an AI-driven, real-time flood prediction system.
- Conducted preliminary research on defining the problem statement, specifically focusing on the gap between static historical models and live meteorological data.
- Explored potential tech stacks and decided on a Flask/Python backend coupled with a Scikit-Learn Random Forest model.

## Week 2 (Aug 10 - Aug 16): Git Repository Setup & Initial Structure
- Initialized the team's GitHub repository (`Flood-Prediction-Using-WeatherAPI-and-historical-thread-mapping`).
- Set up local git environments, established branching workflows, and created the primary project folder structure (`Code`, `Docs`, `Merged_dataset`).
- Configured the initial MkDocs environment for our documentation site using the Material theme.

## Week 3 (Aug 17 - Aug 23): Historical Data Collection & API Prototyping
- Led the primary data collection phase, scouring open-source databases for global historical flood centroids, severity indices, and past occurrence counts.
- Investigated the OpenWeatherMap REST API to understand JSON response structures for temperature, humidity, wind speed, and precipitation.
- Built a minimal Python script to verify live API ingestion and test rate limits.

## Week 4 (Aug 24 - Aug 30): UML Use Case Design & Documentation
- Designed and engineered the standalone **UML Use Case Diagram** using draw.io, mapping out end-user interactions against the system backend and external APIs.
- Pushed updates to the MkDocs documentation site (`index.md`), detailing the proposed system architecture and pipeline stages.
- Supported Diksha in refining the Pitch Slide Deck materials.

## Week 5 (Aug 31 - Sep 6): Feature Engineering & ML Pipeline Setup
- Developed the `feature_engineering.py` logic to normalize live API metrics alongside the historical proximity counts.
- Created the core ML Jupyter Notebook (`train_model.ipynb`) to handle data ingestion for the training phase.
- Began drafting the logic for synthetic overlapping training data (introducing Gaussian noise) to prevent model overfitting.

## Week 6 (Sep 7 - Sep 13): Frontend Dashboard Implementation
- Architected the frontend UI layout for the prediction dashboard using HTML5 and CSS3.
- Engineered the responsive search bar and dynamic risk status indicator cards (Low, Medium, High).
- Started integrating vanilla JavaScript logic to handle asynchronous fetch requests from the UI to our Flask backend.