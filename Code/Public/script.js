document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize Leaflet Map (Centered near Patiala, Zoom Controls moved to top-right)
    const map = L.map('map', {
        zoomControl: false
    }).setView([30.3398, 76.3869], 5); 

    L.control.zoom({
        position: 'topright'
    }).addTo(map);

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
            const response = await fetch(`/predict?city=${encodeURIComponent(city)}`);
            
            if (response.ok) {
                const data = await response.json();
                renderResults(data, city);
            } else {
                const errData = await response.json().catch(() => ({}));
                alert(errData.error || "City not found or server error.");
            }
        } catch (err) {
            console.error("Fetch failed:", err);
            alert("Failed to connect to the prediction service.");
        } finally {
            searchBtn.innerText = "SEARCH";
            searchBtn.disabled = false;
        }
    }

    // 4. Update UI & Risk Styling
    function renderResults(data, cityName) {
        humidityVal.innerText = `${data.live_weather.humidity_pct}%`;
        windVal.innerText = `${data.live_weather.wind_speed_ms} m/s`;
        rainVal.innerText = `${data.live_weather.live_rain_mm} mm`;
        
        if (tempVal) {
            tempVal.innerText = data.live_weather.temp_c !== undefined ? `${data.live_weather.temp_c} °C` : "--";
        }

        floodCountVal.innerText = data.historical_floods_nearby;
        proximityVal.innerText = `${data.nearest_historical_flood_km} km`;
        
        if (severityVal) severityVal.innerText = "ML Optimized";
        if (durationVal) durationVal.innerText = "ML Optimized";

        const risk = data.risk_level.toUpperCase();
        riskLevelText.innerText = risk;

        if (risk.includes("HIGH")) {
            applyRiskTheme("risk-high", "#ef4444", "Historical + extreme weather threshold met");
        } else if (risk.includes("MEDIUM")) {
            applyRiskTheme("risk-medium", "#f59e0b", "Elevated rainfall near historical flood zone");
        } else {
            applyRiskTheme("risk-low", "#22c55e", "Atmospheric metrics within normal safety bounds");
        }

        if (data.latitude && data.longitude) {
            updateMap(data.latitude, data.longitude, cityName.toUpperCase(), risk);
        }
    }

    function applyRiskTheme(className, textColor, subtitle) {
        if(predCard) {
            predCard.classList.remove("risk-high", "risk-medium", "risk-low");
            predCard.classList.add(className);
        }
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
            radius: 50000
        }).addTo(map);
    }

    searchBtn.addEventListener("click", handleSearch);
    locationInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleSearch();
    });
});