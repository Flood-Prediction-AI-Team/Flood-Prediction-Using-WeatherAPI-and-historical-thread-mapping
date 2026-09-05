document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("searchBtn");
    const locationInput = document.getElementById("locationInput");

    searchBtn.addEventListener("click", () => {
        const city = locationInput.value.trim();
        
        if (city !== "") {
            // Later, we will replace this alert with an actual fetch() call to your Python API
            console.log(`Sending request to ML backend for location: ${city}`);
            alert(`Fetching live data and ML prediction for: ${city}`);
        } else {
            alert("Please enter a location.");
        }
    });
});