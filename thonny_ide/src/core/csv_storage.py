import os
import time


class CSVManager:
    def __init__(self, filepath="history.csv"):
        self.filepath = filepath
        self._init_file()

    def _init_file(self):
        try:
            if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    f.write("Timestamp,Temperatura (°C),Umidade (%),Pressao (hPa),Qualidade do Ar (Indice),Classificacao Ar,Estado Gas\n")
        except Exception as e:  # noqa: BLE001
            print("Error initializing CSV:", e)

    def _get_formatted_time(self):
        try:
            t = time.localtime()
            return f"{t[2]:02d}/{t[1]:02d}/{t[0]} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
        except:  # noqa: E722
            return "01/01/2026 00:00:00"

    def _get_air_category(self, index):
        if index is None: return "Indefinido"
        if index <= 500: return "Boa"
        if index <= 1000: return "Moderada"
        if index <= 1500: return "Ruim"
        if index <= 2000: return "Muito Ruim"
        return "Péssima"

    def append(self, data):
        try:
            timestamp = self._get_formatted_time()
            
            # Suporta tanto valores numéricos diretos quanto dicionários com chave 'value'
            temp_raw = data.get("temperature", 0.0)
            temp = temp_raw.get("value", 0.0) if isinstance(temp_raw, dict) else float(temp_raw or 0.0)
            
            hum_raw = data.get("humidity", 0.0)
            hum = hum_raw.get("value", 0.0) if isinstance(hum_raw, dict) else float(hum_raw or 0.0)
            
            pres_raw = data.get("pressure", 0.0)
            pres = pres_raw.get("value", 0.0) if isinstance(pres_raw, dict) else float(pres_raw or 0.0)
            
            aqi_raw = data.get("air_quality_index", 0.0)
            aqi = aqi_raw.get("value", 0.0) if isinstance(aqi_raw, dict) else float(aqi_raw or 0.0)
            
            gas_state = data.get("gas_state", "normal")
            category = self._get_air_category(aqi)

            line = f"{timestamp},{temp:.1f},{hum:.1f},{pres:.1f},{aqi:.1f},{category},{gas_state}\n"
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:  # noqa: BLE001
            print("Error writing to CSV:", e)

    def append_reading(self, data):
        return self.append(data)