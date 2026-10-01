import json
import os
import streamlit as st

st.set_page_config(
    page_title="Nusantara Fantasy TCG Portal",
    page_icon="🃏",
    layout="wide"
)

DB_FILE = "nusantara_tcg_cards.json-ld"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    st.title("🃏 Nusantara Fantasy TCG (NFT)")
    st.markdown("### *Inverted-Pyramid-Framework & Al-Haqq Protocol*")
    st.markdown("Portal kurasi kartu kerakyatan yang transparan, adil, dan ramah pelajar tanpa celah monopoli pasar.")
    
    data = load_data()
    if not data:
        st.error("[!] Database kartu belum ditemukan. Jalankan inisialisasi terlebih dahulu.")
        return

    # Informasi Kreator & Watermark
    with st.sidebar:
        st.header("Informasi Sistem")
        st.text(f"Kreator: {data.get('creator', 'ICAM')}")
        st.info(f"Watermark:\n{data.get('digitalWatermark', 'Al-Haqq Protocol')}")
        st.markdown("---")
        st.markdown("**Filter Faksi:**")
        selected_fringe = st.selectbox(
            "Pilih Faksi", 
            ["Semua Faksi", "Kesultanan Maritim", "Aliansi Rempah Nusantara", "Pendekar Rimba & Pesisir"]
        )

    cards = data.get("itemListElement", [])
    
    # Filter logika faksi
    if selected_fringe != "Semua Faksi":
        cards = [c for c in cards if c.get("fringe") == selected_fringe]

    st.markdown(f"### Menampilkan {len(cards)} Kartu Terdaftar")
    
    # Tata letak grid kartu menggunakan kolom
    cols = st.columns(2)
    for idx, card in enumerate(cards):
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"[{card.get('cardId')}] {card.get('name')}")
                st.caption(f"Faksi: **{card.get('fringe')}** | Tipe: *{card.get('type')}*")
                
                # Atribut & Keamanan
                nfc_badge = "🟢 Aktif (NFC Chip)" if card.get('nfcEnabled') else "⚪ Standar (Visual Secure)"
                st.markdown(f"**Atribut Power:** {card.get('power')} | **Cost:** {card.get('resourceCost')}")
                st.markdown(f"**Keamanan:** {nfc_badge}")
                st.markdown(f"**HET (Harga Rakyat):** `{card.get('priceCapHET')}`")
                
                st.markdown(f"> *\"{card.get('lore')}\"*")

if __name__ == "__main__":
    main()
