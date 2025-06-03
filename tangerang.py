#tangerang.py
from agen_kota import AgenKota

tangerang = AgenKota(
    nama="Tangerang",
    path_data=r"C:\xampp\htdocs\multi_agen_new\data\Tangerang-2020-2022.csv",
    path_output="hasil/tangerang_output.json"
)
tangerang.kirim_hasil()
