<!DOCTYPE html>
<html>
<head>
    <title>Prediksi Kualitas Udara - Sistem Multi Agen</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #006699; }
        table { border-collapse: collapse; width: 70%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #f0f0f0; }
        .button {
            padding: 10px 20px;
            background-color: #006699;
            color: white;
            border: none;
            cursor: pointer;
        }
        .button:hover { background-color: #004466; }
        .keterangan {
            margin-top: 30px;
            border: 1px solid #ccc;
            padding: 15px;
            background-color: #f9f9f9;
            width: 70%;
        }
    </style>
</head>
<body>

<h1>Prediksi Kualitas Udara - Sistem Multi Agen</h1>

<form method="post">
    <button class="button" type="submit" name="prediksi">Jalankan Prediksi</button>
</form>

<?php
function baca_json($file) {
    if (!file_exists($file)) return null;
    $json = file_get_contents($file);
    return json_decode($json, true);
}

$files = [
    "Jakarta" => "hasil/jakarta_output.json",
    "Yogyakarta" => "hasil/jogja_output.json",
    "Tangerang Selatan" => "hasil/tangerang_output.json"
];

$semua_hasil = [];

if (isset($_POST['prediksi'])) {
    // Jalankan skrip Python tanpa menampilkan output
    shell_exec("python main.py 2>&1");

    // Ambil hasil JSON dari semua kota
    foreach ($files as $kota => $file) {
        $data = baca_json($file);
        if ($data) $semua_hasil[] = $data;
    }
}

if (!empty($semua_hasil)) {
    echo "<h2>Hasil Prediksi Tiap Kota</h2>";
    echo "<table>
            <tr>
                <th>Kota</th>
                <th>PM2.5</th>
                <th>PM10</th>
                <th>Status</th>
            </tr>";
    foreach ($semua_hasil as $hasil) {
        echo "<tr>
                <td>{$hasil['kota']}</td>
                <td>{$hasil['pm2.5']}</td>
                <td>{$hasil['pm10']}</td>
                <td>{$hasil['status']}</td>
              </tr>";
    }
    echo "</table>";

    // Kesimpulan nasional
    $status_akhir = "Baik";
    foreach ($semua_hasil as $hasil) {
        if ($hasil['status'] === "Buruk") {
            $status_akhir = "Buruk";
            break;
        } elseif ($hasil['status'] === "Sedang") {
            $status_akhir = ($status_akhir !== "Buruk") ? "Sedang" : $status_akhir;
        }
    }

    echo "<h2>Kesimpulan Kualitas Udara Nasional: <span style='color: red;'>$status_akhir</span></h2>";

    // Keterangan PM
    echo "
    <div class='keterangan'>
        <p><strong>Keterangan:</strong></p>
        <ul>
            <li><strong>PM2.5</strong>: Partikulat udara dengan diameter ≤ 2.5 mikrometer. Dapat masuk hingga ke paru-paru dan berbahaya bagi kesehatan.</li>
            <li><strong>PM10</strong>: Partikulat udara dengan diameter ≤ 10 mikrometer. Dapat menyebabkan gangguan pernapasan.</li>
        </ul>
    </div>
    ";
}
?>

</body>
</html>
