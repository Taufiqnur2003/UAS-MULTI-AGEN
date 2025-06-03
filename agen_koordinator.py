# agen_koordinator.py
import json

class AgenKoordinator:
    def __init__(self, file_outputs):
        self.file_outputs = file_outputs

    def baca_hasil(self):
        data = []
        for path in self.file_outputs:
            try:
                with open(path, "r") as f:
                    hasil = json.load(f)
                    data.append(hasil)
            except:
                print(f"Gagal membaca: {path}")
        return data

    def kesimpulan_umum(self, data):
        counts = {"Baik": 0, "Sedang": 0, "Buruk": 0}
        for item in data:
            counts[item["status"]] += 1

        if counts["Buruk"] > 0:
            return "Buruk"
        elif counts["Sedang"] > 0:
            return "Sedang"
        else:
            return "Baik"

    def tampilkan(self):
        data = self.baca_hasil()
        for item in data:
            print(f"{item['kota']}: PM2.5 = {item['pm2.5']}, PM10 = {item['pm10']}, Status = {item['status']}")
        kesimpulan = self.kesimpulan_umum(data)
        print(f"\n>>> Kesimpulan kualitas udara nasional: {kesimpulan}")
