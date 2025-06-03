# jogja.py
from agen_kota import AgenKota

jogja = AgenKota(
    nama="Jogja",
    path_data=r"C:\xampp\htdocs\multi_agen_new\data\Jogja-2021.csv",
    path_output="hasil/jogja_output.json"
)
jogja.kirim_hasil()
