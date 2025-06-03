# agen_kota.py
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class AgenKota:
    def __init__(self, nama, path_data, path_output):
        self.nama = nama
        self.path_data = path_data
        self.path_output = path_output

    def muat_data(self):
        df = pd.read_csv(self.path_data)
        df.columns = [col.lower().strip().replace(".", "").replace(" ", "") for col in df.columns]
        df = df[["co", "no2", "pm10", "so2", "pm25"]]
        df.columns = ["co", "no2", "pm10", "so2", "pm2.5"]
        df.dropna(inplace=True)
        return df

    def prediksi(self):
        df = self.muat_data()
        X = df[["co", "no2", "so2"]]
        y = df[["pm2.5", "pm10"]]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        X_sample = X_test.sample(n=10)
        prediksi = model.predict(X_sample)

        pm25_avg = np.mean([x[0] for x in prediksi])
        pm10_avg = np.mean([x[1] for x in prediksi])
        return pm25_avg, pm10_avg

    def klasifikasi(self, pm25, pm10):
        if pm25 > 100 or pm10 > 350:
            return "Buruk"
        elif pm25 > 50 or pm10 > 150:
            return "Sedang"
        else:
            return "Baik"

    def kirim_hasil(self):
        pm25, pm10 = self.prediksi()
        status = self.klasifikasi(pm25, pm10)
        hasil = {
            "kota": self.nama,
            "pm2.5": round(pm25, 2),
            "pm10": round(pm10, 2),
            "status": status
        }
        with open(self.path_output, "w") as f:
            json.dump(hasil, f)
        print(f"[{self.nama}] Hasil dikirim ke {self.path_output}")
