







import streamlit as st
import json
import os

PROTOCOL_STATE_FILE = "al_haqq_protocol_state.json"

st.set_page_config(page_title="Al-Haqq Protocol Monitor", layout="centered")

st.title("🌐 Al-Haqq Protocol Monitoring Dashboard")
st.markdown("**Operator:** ICAM (Syams Maulana)")
st.markdown("---")

if os.path.exists(PROTOCOL_STATE_FILE):
    with open(PROTOCOL_STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    st.subheader(f"Versi Protokol: {data.get('version', 'N/A')}")
    st.text(f"Pembaruan Terakhir: {data.get('last_updated', 'N/A')}")
    st.info(f"**Tujuan Utama:** {data.get('objective', '')}")
    
    st.markdown("### Status Modul Sistem")
    modules = data.get("modules", {})
    for mod_name, details in modules.items():
        st.write(f"**{mod_name.replace('_', ' ').title()}** — Status: *{details['status']}*")
        st.progress(details["progress"] / 100.0)
        st.text(f"Progress: {details['progress']}%")
        
    st.markdown("---")
    st.caption(f"🔒 {data.get('watermark_signature', '')}")
else:
    st.warning("File status protokol belum ditemukan. Jalankan skrip sinkronisasi terlebih dahulu.")
