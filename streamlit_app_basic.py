# FILE: streamlit_app_basic.py
# FUNGSI: TUTOR AI UTAMA DENGAN MEMORI PERCAKAPAN (SESI CHAT)

import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import pandas as pd
from datetime import datetime

# =============================================================
# 🔐 KONFIGURASI & CLIENT
# =============================================================

st.set_page_config(page_title="Tutor AI Interaktif", page_icon="🧑‍💻")
st.title("🤖 Your Personal Code Cheatsheet")
st.caption("Asisten pribadi Anda dengan memori percakapan yang berkelanjutan.")

# Sidebar untuk API Key dan Pengaturan
st.sidebar.title("⚙️ Pengaturan Tutor")
api_key = st.sidebar.text_input("Masukkan Google API Key", type="password")

SYSTEM_INSTRUCTION = """
Anda adalah tutor sabar dan ahli di bidang programming (Python, Streamlit) dan bahasa asing.
Berikan penjelasan yang mudah dicerna, didukung oleh contoh kode yang ringkas atau simulasi percakapan.
Koreksi kesalahan pengguna dengan cara yang membangun. Jaga nada bicara tetap ramah dan profesional.
"""

# --- INICIALISASI CLIENT DAN SESI ---
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if "chat_session" not in st.session_state:
            config = types.GenerateContentConfig(
                temperature=0.4,
                system_instruction=SYSTEM_INSTRUCTION
            )
            # Membuat sesi chat dengan memori
            st.session_state["chat_session"] = client.chats.create(
                model="gemini-2.5-flash",
                config=config,
                history=[]
            )
            st.session_state["messages"] = [{"role": "assistant", "content": "Hai! Saya Tutor AI Anda. Apa yang ingin Anda pelajari hari ini?"}]

    except Exception as e:
        st.error(f"🚨 Error: Gagal menginisialisasi Gemini Client. Cek API Key Anda.")
        st.stop()

# =============================================================
# 💬 FUNGSI CHAT UTAMA (HANDLE INPUT)
# =============================================================

def handle_user_input():
    if not api_key:
        st.warning("Masukkan API Key di sidebar untuk memulai.")
        return

    user_input = st.session_state.user_input
    if user_input:
        # Simpan pesan pengguna ke riwayat tampilan
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.spinner("Tutor sedang berpikir..."):
            try:
                chat = st.session_state["chat_session"]
                # Kirim pesan ke sesi chat (memori terjaga)
                response = chat.send_message(user_input)
                # Simpan respons bot
                st.session_state["messages"].append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error saat mengirim pesan: {e}")
                st.session_state["messages"].append({"role": "assistant", "content": "Maaf, terjadi kesalahan teknis."})
        
        # Kosongkan input dan refresh untuk menampilkan chat terbaru
        st.session_state.user_input = ""
        st.rerun()

# =============================================================
# 🖼️ TAMPILAN DAN KONTROL
# =============================================================

# Menampilkan riwayat percakapan
for msg in st.session_state.get("messages", []):
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Area Input Teks
st.text_input(
    "Tanyakan sesuatu pada Tutor Anda:",
    key="user_input",
    on_change=handle_user_input, 
    placeholder="Contoh: Jelaskan konsep virtual environment."
)

# Kontrol di Sidebar
with st.sidebar:
    st.write("---")
    
    if st.button("🔄 Reset Chat Session"):
        st.session_state.pop("chat_session", None)
        st.session_state.pop("messages", None)
        st.rerun()

    # Ekspor Chat
    if st.session_state.get("messages"):
        df_list = [{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]
        df = pd.DataFrame(df_list)
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        st.download_button(
            label="💾 Unduh Riwayat Chat",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=filename,
            mime='text/csv'
        )