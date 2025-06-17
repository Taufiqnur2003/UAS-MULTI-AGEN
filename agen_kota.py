# agen_kota.py
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

class AgenKota:
    def __init__(self, nama, path_data, path_output):
        self.nama = nama
        self.path_data = path_data
        self.path_output = path_output
        os.makedirs("hasil/plots", exist_ok=True)

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

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Inisialisasi model dengan OOB score
        model = RandomForestRegressor(
            n_estimators=100,
            oob_score=True,
            warm_start=True,  # Untuk incremental training
            random_state=42
        )
        
        # Tracking error
        train_errors_pm25 = []
        test_errors_pm25 = []
        train_errors_pm10 = []
        test_errors_pm10 = []
        
        # Training incremental
        for n in range(1, 101):
            model.n_estimators = n
            model.fit(X_train, y_train)
            
            # Prediksi training dan test
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            # Hitung MSE
            train_errors_pm25.append(mean_squared_error(y_train['pm2.5'], train_pred[:,0]))
            test_errors_pm25.append(mean_squared_error(y_test['pm2.5'], test_pred[:,0]))
            train_errors_pm10.append(mean_squared_error(y_train['pm10'], train_pred[:,1]))
            test_errors_pm10.append(mean_squared_error(y_test['pm10'], test_pred[:,1]))
        
        # Plot training loss
        self.plot_training_loss(
            train_errors_pm25, test_errors_pm25,
            train_errors_pm10, test_errors_pm10
        )
        
        # Prediksi final
        X_sample = X_test.sample(n=10)
        prediksi = model.predict(X_sample)
        
        pm25_avg = np.mean([x[0] for x in prediksi])
        pm10_avg = np.mean([x[1] for x in prediksi])
        return pm25_avg, pm10_avg

    def plot_training_loss(self, train_pm25, test_pm25, train_pm10, test_pm10):
        plt.figure(figsize=(12, 6))
        
        # Plot PM2.5
        plt.subplot(1, 2, 1)
        plt.plot(train_pm25, label='Training Loss (PM2.5)', color='blue')
        plt.plot(test_pm25, label='Validation Loss (PM2.5)', color='red')
        plt.xlabel('Number of Trees')
        plt.ylabel('Mean Squared Error')
        plt.title(f'PM2.5 Learning Curve\n({self.nama})')
        plt.legend()
        plt.grid()
        
        # Plot PM10
        plt.subplot(1, 2, 2)
        plt.plot(train_pm10, label='Training Loss (PM10)', color='blue')
        plt.plot(test_pm10, label='Validation Loss (PM10)', color='red')
        plt.xlabel('Number of Trees')
        plt.ylabel('Mean Squared Error')
        plt.title(f'PM10 Learning Curve\n({self.nama})')
        plt.legend()
        plt.grid()
        
        plt.tight_layout()
        plot_path = f"hasil/plots/{self.nama.lower()}_training_loss.png"
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f"[{self.nama}] Training loss plot disimpan di {plot_path}")

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
        
