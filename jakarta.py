# jakarta.py
from agen_kota import AgenKota

jakarta = AgenKota(
    nama="Jakarta",
    path_data=r"C:\xampp\htdocs\multi_agen_new\data\Jakarta.csv",
    path_output="hasil/jakarta_output.json"
)
jakarta.kirim_hasil()
