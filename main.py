# main.py
import subprocess
from agen_koordinator import AgenKoordinator
import time

# Jalankan agen-agen kota
subprocess.run(["python", "jakarta.py"])
subprocess.run(["python", "jogja.py"])
subprocess.run(["python", "tangerang.py"])

# Tunggu file tersedia
time.sleep(1)

# Jalankan agen koordinator
koordinator = AgenKoordinator([
    "hasil/jakarta_output.json",
    "hasil/jogja_output.json",
    "hasil/tangerang_output.json"
])
koordinator.tampilkan()
