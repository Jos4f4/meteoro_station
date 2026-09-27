/**
 * Fetches the latest readings from the local API and updates the DOM.
 */
async function fetchReadings() {
    try {
        const response = await fetch('/api');
        if (!response.ok) throw new Error('Falha na rede');
        
        const data = await response.json();
        
        // Atualiza a tela com os valores lidos (RF05)
        document.getElementById('temp-val').textContent = data.temperature ? data.temperature.toFixed(1) : '--';
        document.getElementById('hum-val').textContent = data.humidity ? data.humidity.toFixed(1) : '--';
        
        const gasEl = document.getElementById('gas-val');
        const gasStatusEl = document.getElementById('gas-status');
        
        // Tratamento visual para o estado do sensor (RF09)
        if (data.gas_state === 'heating') {
            gasEl.textContent = 'Aquecendo...';
            gasStatusEl.className = 'status heating';
            gasStatusEl.textContent = 'Aquecendo';
        } else {
            gasEl.textContent = data.air_quality_index ? data.air_quality_index.toFixed(1) : '--';
            gasStatusEl.className = 'status valid';
            gasStatusEl.textContent = 'Online';
        }

        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        document.getElementById('last-update').textContent = `Atualizado às ${time}`;
        
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
    }
}

// Polling local para manter a tela atualizada sem recarregar (RF06)
setInterval(fetchReadings, 5000);
fetchReadings();