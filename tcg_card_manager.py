import json
import os

DB_FILE = "nusantara_tcg_cards.json-ld"

def initialize_database():
    """Inisialisasi database lengkap dengan Al-Haqq Digital Watermark dan Faksi Akar Rumput."""
    enhanced_data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Nusantara Fantasy TCG Master Database",
        "creator": "Syams Maulana (ICAM)",
        "digitalWatermark": "Authentic Collaborative Digital Stamp ICAM / Syams Maulana (Al-Haqq Protocol)",
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
                "resourceCost": 0,
                "priceCapHET": "Rp 25.000 (Starter Deck)",
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
                "resourceCost": 1,
                "priceCapHET": "Rp 5.000 (Booster Pack)",
                "lore": "Sumber energi taktis berbasis komoditas lokal yang memperkuat pertahanan akar rumput."
            },
            {
                "@type": "CreativeWork",
                "cardId": "NFT-003",
                "name": "Panglima Rimba Terpadu",
                "fringe": "Pendekar Rimba & Pesisir",
                "type": "Warrior / Vanguard",
                "nfcEnabled": False,
                "power": 2500,
                "resourceCost": 2,
                "priceCapHET": "Rp 15.000 (Pocket Deck)",
                "lore": "Simbol ketahanan masyarakat bawah dengan pertahanan awal yang kokoh untuk membalikkan keadaan."
            }
        ]
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(enhanced_data, f, indent=4)
    print("[INFO] Database JSON-LD sukses diperbarui dengan Watermark Al-Haqq & Faksi Lengkap!")

def view_cards():
    """Menampilkan seluruh kartu beserta atribut HET dan Watermark."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n--- {data['name']} ---")
        print(f"Kreator: {data['creator']}")
        print(f"Watermark: {data['digitalWatermark']}\n")
        for card in data["itemListElement"]:
            nfc_status = "Aktif (NFC Chip)" if card["nfcEnabled"] else "Standar (Visual Secure)"
            print(f"[{card['cardId']}] {card['name']}")
            print(f" > Faksi: {card['fringe']} | Tipe: {card['type']}")
            print(f" > Atribut: Power {card['power']} | Cost: {card['resourceCost']}")
            print(f" > Keamanan: {nfc_status} | HET: {card['priceCapHET']}")
            print(f" > Lore: {card['lore']}\n")
    else:
        print("[ERROR] Database belum ditemukan.")

if __name__ == "__main__":
    initialize_database()
    view_cards()
