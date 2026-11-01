function getAirQualityCategory(index) {
    if (index <= 500) return { text: "Boa", class: "aq-good" };
    if (index <= 1000) return { text: "Moderada", class: "aq-moderate" };
    if (index <= 1500) return { text: "Ruim", class: "aq-bad" };
    if (index <= 2000) return { text: "Muito Ruim", class: "aq-very-bad" };
    return { text: "Péssima", class: "aq-terrible" };
}

async function updateData() {
    try {
        const response = await fetch('/api');
        if (!response.ok) return;
        const data = await response.json();

        // Temperature and Humidity
        const tempVal = typeof data.temperature === 'object' ? data.temperature.value : data.temperature;
        const humVal = typeof data.humidity === 'object' ? data.humidity.value : data.humidity;
        
        document.getElementById('temp-value').innerText = `${Number(tempVal).toFixed(1)} °C`;
        document.getElementById('hum-value').innerText = `${Number(humVal).toFixed(1)} % UR`;
        
        // Air Quality Index (supports both object and direct number formats)
        let airIndex = 450; // default fallback
        if (data.air_quality_index !== undefined) {
            airIndex = typeof data.air_quality_index === 'object' ? data.air_quality_index.value : data.air_quality_index;
        } else if (data.gas !== undefined) {
            airIndex = typeof data.gas === 'object' ? data.gas.value : data.gas;
        }

        const category = getAirQualityCategory(airIndex);
        
        document.getElementById('air-value').innerText = `${Number(airIndex).toFixed(1)} Índice`;
        const badge = document.getElementById('air-category');
        badge.innerText = category.text;
        badge.className = `category-badge ${category.class}`;

        const now = new Date();
        document.getElementById('status-time').innerText = `Atualizado às ${now.toLocaleTimeString()}`;
    } catch (error) {
        console.error("Erro ao atualizar dados:", error);
    }
}

setInterval(updateData, 3000);
updateData();