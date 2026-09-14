import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="GOD•MauL Hub Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ GOD•MauL Hub & TCG Command Center")
st.markdown("Kedaulatan Narasi Digital & Manajemen Turnamen Terpadu")

API_BASE = "http://127.0.0.1:5001/api"

def load_json(file_path, default):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

tab1, tab2 = st.tabs(["🏆 TCG Tournament", "📚 Content Archive & Publisher"])

with tab1:
    st.header("Manajemen Turnamen TCG")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daftar Peserta Baru")
        with st.form("add_player_form"):
            new_player = st.text_input("Nama Peserta / Duelist")
            submitted_player = st.form_submit_button("Daftarkan")
            if submitted_player and new_player:
                res = requests.post(f"{API_BASE}/tourney/add", json={"name": new_player})
                if res.status_code == 200:
                    st.success(res.json().get("message"))
                    st.rerun()
                else:
                    st.error(res.json().get("message"))
    
    with col2:
        st.subheader("Generate Pairing")
        if st.button("Buat Pairing Babak"):
            res = requests.get(f"{API_BASE}/tourney/pair")
            if res.status_code == 200:
                pair_data = res.json()
                st.success("Pairing berhasil dibuat!")
                for p in pair_data.get("pairings", []):
                    st.write(f"Meja {p['table']}: **{p['p1']}** VS **{p['p2']}**")
            else:
                st.error("Gagal membuat pairing.")

    st.markdown("---")
    t_data = load_json("tournament_data.json", {"name": "GOD•MauL TCG Championship", "players": []})
    players = t_data.get("players", [])

    if players:
        st.subheader("Catat Hasil Pertandingan")
        player_names = [p["name"] for p in players]
        with st.form("record_match_form"):
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                p1_select = st.selectbox("Pemain 1 (P1)", player_names)
            with col_m2:
                p2_options = player_names + ["BYE (Free Win)"]
                p2_select = st.selectbox("Pemain 2 (P2)", p2_options)
            with col_m3:
                result_select = st.selectbox(
                    "Hasil", 
                    options=["p1", "p2", "draw"], 
                    format_func=lambda x: "P1 Menang" if x=="p1" else ("P2 Menang" if x=="p2" else "Seri (Draw)")
                )
            
            submitted_match = st.form_submit_button("Simpan Hasil")
            if submitted_match:
                payload = {"p1": p1_select, "p2": p2_select, "result": result_select}
                res = requests.post(f"{API_BASE}/tourney/record", json=payload)
                if res.status_code == 200:
                    st.success("Hasil pertandingan berhasil dicatat ke sistem!")
                    st.rerun()
                else:
                    st.error(res.json().get("message", "Gagal mencatat hasil."))

    st.markdown("---")
    st.subheader(f"Klasemen: {t_data.get('name', 'Championship')}")
    if players:
        sorted_players = sorted(players, key=lambda x: x["points"], reverse=True)
        for idx, p in enumerate(sorted_players, 1):
            st.write(f"**{idx}. {p['name']}** — {p['points']} Poin")
    else:
        st.info("Belum ada peserta terdaftar.")

with tab2:
    st.header("Publikasi & Arsip Konten")
    
    with st.expander("📝 Tulis & Publikasikan Konten Baru"):
        with st.form("publish_form"):
            pub_title = st.text_input("Judul Narasi")
            pub_desc = st.text_input("Deskripsi Singkat")
            pub_content = st.text_area("Isi Konten / Artikel")
            submitted_pub = st.form_submit_button("Publikasikan ke Hub")
            if submitted_pub and pub_title:
                payload = {"title": pub_title, "description": pub_desc, "content": pub_content}
                res = requests.post(f"{API_BASE}/publish", json=payload)
                if res.status_code == 200:
                    st.success("Konten berhasil diarsipkan dan diberi cap digital!")
                    st.rerun()
                else:
                    st.error("Gagal mempublikasikan konten.")

    st.markdown("---")
    archive = load_json("hub_archive.json", [])
    if archive:
        for item in reversed(archive):
            with st.expander(f"{item.get('title')} ({item.get('timestamp')})"):
                st.write(f"**Deskripsi:** {item.get('description')}")
                st.markdown("---")
                st.text(item.get('processed_content'))
    else:
        st.info("Belum ada arsip konten tersimpan.")
