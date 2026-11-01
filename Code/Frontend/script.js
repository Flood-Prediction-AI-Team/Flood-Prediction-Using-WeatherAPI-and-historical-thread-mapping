document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize Leaflet Map (Centered near Patiala)
    const map = L.map('map').setView([30.3398, 76.3869], 5); 

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let activeMarker = null;
    let floodCircle = null;

    // 2. Element Selectors
    const searchBtn = document.getElementById("searchBtn");
    const locationInput = document.getElementById("locationInput");

    const tempVal = document.getElementById("tempVal");
    const humidityVal = document.getElementById("humidityVal");
    const windVal = document.getElementById("windVal");
    const rainVal = document.getElementById("rainVal");

    const floodCountVal = document.getElementById("floodCountVal");
    const severityVal = document.getElementById("severityVal");
    const durationVal = document.getElementById("durationVal");
    const proximityVal = document.getElementById("proximityVal");

    const predCard = document.getElementById("predCard");
    const predCardTitle = document.getElementById("predCardTitle");
    const predHr = document.getElementById("predHr");
    const riskLevelText = document.getElementById("riskLevelText");
    const riskSubtitle = document.getElementById("riskSubtitle");

    // 3. Search Action
    async function handleSearch() {
        const city = locationInput.value.trim();
        if (!city) {
            alert("Please enter a city or location name.");
            return;
        }

        searchBtn.innerText = "QUERYING...";
        searchBtn.disabled = true;

        try {
            const response = await fetch(`http://127.0.0.1:5000/predict?city=${encodeURIComponent(city)}`);
            
            if (response.ok) {
                const data = await response.json();
                renderResults(data, city);
            } else {
                alert("Backend Error: Ensure Flask is running and CORS is enabled.");
            }
        } catch (err) {
            console.error("Fetch failed:", err);
            alert("Failed to connect to the backend. Is the Flask server running?");
        } finally {
            searchBtn.innerText = "SEARCH";
            searchBtn.disabled = false;
        }
    }

    // 4. Update UI & Risk Styling
    function renderResults(data, cityName) {
        // Map nested live weather data
        humidityVal.innerText = `${data.live_weather.humidity_pct}%`;
        windVal.innerText = `${data.live_weather.wind_speed_ms} m/s`;
        rainVal.innerText = `${data.live_weather.live_rain_mm} mm`;
        
        // Temperature was pruned from the ML model, marking as N/A
        if (tempVal) tempVal.innerText = "N/A (Pruned)"; 

        // Map historical API data
        floodCountVal.innerText = data.historical_floods_nearby;
        proximityVal.innerText = `${data.nearest_historical_flood_km} km`;
        
        // Severity and Casualties were pruned for generalization
        if (severityVal) severityVal.innerText = "ML Optimized";
        if (durationVal) durationVal.innerText = "ML Optimized";

        // Display Prediction
        const risk = data.risk_level.toUpperCase();
        riskLevelText.innerText = risk;

        // Apply theme color based on Random Forest output
        if (risk.includes("HIGH")) {
            applyRiskTheme("#dc2626", "#fef2f2", "#fca5a5", "Historical + extreme weather threshold met");
        } else if (risk.includes("MEDIUM")) {
            applyRiskTheme("#d97706", "#fffbeb", "#fcd34d", "Elevated rainfall near historical flood zone");
        } else {
            applyRiskTheme("#16a34a", "#f0fdf4", "#86efac", "Atmospheric metrics within normal safety bounds");
        }

        // Update Leaflet Map Pin
        if (data.latitude && data.longitude) {
            updateMap(data.latitude, data.longitude, cityName.toUpperCase(), risk);
        }
    }

    function applyRiskTheme(textColor, bgColor, borderColor, subtitle) {
        if(predCard) predCard.style.backgroundColor = bgColor;
        if(predCard) predCard.style.borderColor = borderColor;
        if(predCardTitle) predCardTitle.style.color = textColor;
        if(predHr) predHr.style.borderColor = borderColor;
        if(riskLevelText) riskLevelText.style.color = textColor;
        if(riskSubtitle) {
            riskSubtitle.style.color = textColor;
            riskSubtitle.innerText = subtitle;
        }
    }

    function updateMap(lat, lon, label, risk) {
        map.flyTo([lat, lon], 9, { duration: 1.5 });

        if (activeMarker) map.removeLayer(activeMarker);
        if (floodCircle) map.removeLayer(floodCircle);

        activeMarker = L.marker([lat, lon]).addTo(map)
            .bindPopup(`<b>${label}</b><br>Assessed Threat: ${risk}`)
            .openPopup();

        const circleColor = risk.includes("HIGH") ? '#ef4444' : risk.includes("MEDIUM") ? '#f59e0b' : '#22c55e';
        floodCircle = L.circle([lat, lon], {
            color: circleColor,
            fillColor: circleColor,
            fillOpacity: 0.15,
            radius: 50000 // 50 km radius indicator
        }).addTo(map);
    }

    // Event Listeners
    searchBtn.addEventListener("click", handleSearch);
    locationInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleSearch();
    });
});