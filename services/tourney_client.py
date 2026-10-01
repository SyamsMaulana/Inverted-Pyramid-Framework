import sys
import requests
import json

BASE_URL = "http://127.0.0.1:5001/api/tourney"

def get_standings():
    res = requests.get(f"{BASE_URL}/standings")
    if res.status_code == 200:
        data = res.json()
        print(f"\n=== KLASEMEN: {data['tournament']} ===")
        for idx, p in enumerate(data['standings'], 1):
            print(f"{idx}. {p['name']} — {p['points']} Poin")
        print("===================================\n")
    else:
        print(f"[ERROR] Gagal mengambil klasemen: {res.text}")

def add_player(name):
    res = requests.post(f"{BASE_URL}/add", json={"name": name})
    print(res.json().get("message", res.text))

def get_pairings():
    res = requests.get(f"{BASE_URL}/pair")
    if res.status_code == 200:
        data = res.json()
        print(f"\n--- PAIRING: {data['tournament']} ---")
        for p in data['pairings']:
            print(f"Meja {p['table']}: {p['p1']} VS {p['p2']}")
        print("------------------------------------\n")
    else:
        print(f"[ERROR] Gagal membuat pairing: {res.text}")

def record_match(p1, p2, result):
    payload = {"p1": p1, "p2": p2, "result": result}
    res = requests.post(f"{BASE_URL}/record", json=payload)
    print(res.json().get("message", res.text))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "standings":
            get_standings()
        elif cmd == "add" and len(sys.argv) > 2:
            add_player(sys.argv[2])
        elif cmd == "pair":
            get_pairings()
        elif cmd == "record" and len(sys.argv) > 4:
            record_match(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Gunakan perintah: python3 tourney_client.py [standings | add <nama> | pair | record <p1> <p2> <p1/p2/draw>]")
    else:
        get_standings()
