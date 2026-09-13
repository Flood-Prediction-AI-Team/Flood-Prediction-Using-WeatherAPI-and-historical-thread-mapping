# Weekly Progress Journal — Diksha Garg (Roll No: 1024240015)

**Project Name:** Real-Time Flood Risk AI Prediction System
**Role:** Data Engineer, System Architect, Spatial Logic Developer

---

## Week 1 (Aug 3 - Aug 9): Architecture & Tech Stack Definition
- Participated in project selection meetings and brainstorming sessions.
- Defined the decoupled 3-tier system architecture: Presentation Tier (HTML/JS), Application Tier (Flask API), and Machine Learning Tier (Scikit-Learn).
- Evaluated Leaflet.js for interactive geospatial mapping capabilities.

## Week 2 (Aug 10 - Aug 16): Presentation Materials & Proposal Drafts
- Designed and structured the project pitch presentation slide deck, focusing on clear visual communication of our proposed data fusion approach.
- Handled the drafting of the formal project proposal document, detailing the problem statement, proposed solution, and evaluation criteria.
- Organized the master Gantt Chart tracking template to manage our semester schedule.

## Week 3 (Aug 17 - Aug 23): Data Cleaning & Dataset Merging
- Took ownership of the raw historical datasets collected by Amit.
- Conducted extensive data cleaning in Pandas (handling missing values, standardizing coordinate formats, and removing duplicate entries).
- Successfully merged multiple raw CSV files into the unified `fused_historical_database.csv` used as the ground truth for our spatial indexing.

## Week 4 (Aug 24 - Aug 30): DFD & ER Diagram Engineering
- Drafted and finalized the **Data Flow Diagrams (DFD Level 0, 1, 2)**, visualizing the flow of coordinates to the API, through the fusion engine, and back to the client.
- Designed the **Entity-Relationship (ER) Diagram** outlining the structure of our fused historical database and the feature vector schemas.
- Ensured all diagrams were properly exported and integrated into the MkDocs project structure.

## Week 5 (Aug 31 - Sep 6): Spatial Indexing & Haversine Logic
- Researched and implemented the geospatial mathematics required for threat indexing.
- Coded the Haversine formula logic in Python to calculate the geodesic distance between the user's queried city and the centroids of all historical floods.
- Tested the spatial query algorithm to ensure it accurately returns threat counts within a 100km radius.

## Week 6 (Sep 7 - Sep 13): UI Mapping Integration & Fallback Logic
- Collaborated with Amit to integrate Leaflet.js into the frontend dashboard (`script.js`).
- Programmed the dynamic fly-to animations and the rendering of the 50km geospatial threat radius circles on the map.
- Designed the architectural logic for the "Mock Weather Fallback" system to ensure UI stability if the OpenWeatherMap API rate limits are exceeded.