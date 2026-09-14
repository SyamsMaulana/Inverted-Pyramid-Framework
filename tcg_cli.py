import json
import os

DB_FILE = "nusantara_tcg_cards.json-ld"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def list_cards():
    data = load_data()
    if not data or not data["itemListElement"]:
        print("\n[!] Belum ada kartu di dalam database.")
        return
    print(f"\n=== DAFTAR KARTU: {data['name']} ===")
    for card in data["itemListElement"]:
        nfc = "Aktif (NFC)" if card["nfcEnabled"] else "Standar (Visual)"
        print(f"[{card['cardId']}] {card['name']} ({card['fringe']})")
        print(f"    Tipe: {card['type']} | Power: {card['power']} | HET: {card['priceCapHET']}")
        print(f"    Keamanan: {nfc} | Cost: {card['resourceCost']}")
        print(f"    Lore: {card['lore']}\n")

def add_card():
    data = load_data()
    if not data:
        print("[!] Database belum diinisialisasi.")
        return
    
    print("\n--- TAMBAH KARTU BARU NUSANTARA FANTASY TCG ---")
    card_id = input("Masukkan ID Kartu (cth: NFT-004): ")
    name = input("Nama Kartu: ")
    fringe = input("Faksi (Kesultanan Maritim / Aliansi Rempah / Pendekar Rimba): ")
    c_type = input("Tipe Kartu (Commander / Spell / Warrior): ")
    nfc_input = input("Gunakan Stiker NFC? (y/n): ").lower()
    nfc_enabled = True if nfc_input == 'y' else False
    power = int(input("Atribut Power (Angka, cth: 2000): "))
    cost = int(input("Resource Cost (Angka, cth: 1): "))
    het = input("Harga Eceran Tertinggi / HET (cth: Rp 15.000): ")
    lore = input("Deskripsi / Lore Kartu: ")

    new_card = {
        "@type": "CreativeWork",
        "cardId": card_id,
        "name": name,
        "fringe": fringe,
        "type": c_type,
        "nfcEnabled": nfc_enabled,
        "power": power,
        "resourceCost": cost,
        "priceCapHET": het,
        "lore": lore
    }

    data["itemListElement"].append(new_card)
    save_data(data)
    print(f"\n[INFO] Kartu '{name}' berhasil ditambahkan ke database!")

def main():
    while True:
        print("\n=== NUSANTARA FANTASY TCG CLI ===")
        print("1. Lihat Semua Kartu")
        print("2. Tambah Kartu Baru")
        print("3. Keluar")
        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            list_cards()
        elif choice == '2':
            add_card()
        elif choice == '3':
            print("\nTerima kasih, teruskan karya gemilang ini, ICAM!")
            break
        else:
            print("[!] Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
