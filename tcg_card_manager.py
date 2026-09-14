import json
import os

DB_FILE = "nusantara_tcg_cards.json-ld"

def initialize_database():
    """Inisialisasi database awal dengan struktur JSON-LD dan faksi dasar."""
    if not os.path.exists(DB_FILE):
        initial_data = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Nusantara Fantasy TCG Card Database",
            "creator": "Syams Maulana (ICAM)",
            "framework": "Inverted-Pyramid-Framework",
            "itemListElement": [
                {
                    "@type": "CreativeWork",
                    "cardId": "NFT-001",
                    "name": "Laksamana Bahari",
                    "fringe": "Kesultanan Maritim",
                    "type": "Commander / Hero",
                    "nfcEnabled": True,
                    "power": 3000,
                    "lore": "Penguasa jalur sutra maritim yang memimpin armada dengan strategi taktis tinggi."
                },
                {
                    "@type": "CreativeWork",
                    "cardId": "NFT-002",
                    "name": "Penjaga Rempah Pala",
                    "fringe": "Aliansi Rempah Nusantara",
                    "type": "Resource / Spell",
                    "nfcEnabled": False,
                    "power": 1200,
                    "lore": "Sumber energi taktis berbasis komoditas lokal yang memperkuat pertahanan akar rumput."
                }
            ]
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=4)
        print("[INFO] Database JSON-LD berhasil diinisialisasi!")

def view_cards():
    """Menampilkan seluruh kartu yang terdaftar dalam database."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n--- {data['name']} ---")
        print(f"Kreator: {data['creator']} | Framework: {data['framework']}\n")
        for card in data["itemListElement"]:
            # Perbaikan operator terner Python
            nfc_status = "Aktif (NFC Chip)" if card["nfcEnabled"] else "Standar (Visual Secure)"
            print(f"[{card['cardId']}] {card['name']}")
            print(f" > Faksi: {card['fringe']} | Tipe: {card['type']}")
            print(f" > Atribut: Power {card['power']} | Pengaman: {nfc_status}")
            print(f" > Lore: {card['lore']}\n")
    else:
        print("[ERROR] Database belum ditemukan. Jalankan inisialisasi.")

if __name__ == "__main__":
    initialize_database()
    view_cards()
