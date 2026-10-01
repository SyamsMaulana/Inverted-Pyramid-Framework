import requests
import json

url = "http://127.0.0.1:5001/api/publish"
payload = {
    "title": "Ekspansi Ekosistem GOD•MauL Hub",
    "description": "Integrasi klien CLI dengan API Al-Haqq Protocol untuk otomasi penerbitan.",
    "content": "Kedaulatan narasi digital dibangun melalui sinkronisasi sistem lokal yang tangguh dan kolaborasi pemikiran yang otentik."
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
if response.status_code == 200:
    res_data = response.json()
    print("[SUCCESS] Respon API Diterima:\n")
    print(res_data["processed_content"])
    print("\n--- JSON-LD --- \n", res_data["json_ld_schema"])
else:
    print(f"[ERROR] Gagal terhubung: {response.status_code}")
