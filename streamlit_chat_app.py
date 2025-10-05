# FILE: streamlit_chat_app.py
# FUNGSI: GALERI FITUR DEBUGGING, QUIZ, DAN QUICK ASK (TANPA MEMORI SESI)

import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import pandas as pd
import numpy as np # Untuk data dummy quiz
import matplotlib.pyplot as plt # Untuk chart

# =============================================================
# 🔐 KONFIGURASI & CLIENT
# =============================================================

st.set_page_config(page_title="Galeri Fitur AI", page_icon="🧩", layout="wide")
st.title("🧩 Galeri Fitur Pembelajaran (Sekali Tembak)")
st.caption("Uji fitur kuis dan debugging AI tanpa mempertahankan riwayat percakapan.")

st.sidebar.title("🔑 API Key")
api_key = st.sidebar.text_input("Masukkan Google API Key", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        MODEL_NAME = "gemini-2.5-flash"
    except Exception as e:
        st.error(f"🚨 Error: Gagal menginisialisasi Gemini Client. {e}")
        st.stop()
else:
    st.info("Masukkan API Key di sidebar untuk mengaktifkan fitur.")
    st.stop()

# System Instruction Sederhana untuk Quick Ask
QUICK_INSTRUCTION = "Anda adalah asisten yang ahli di bidang pemrograman dan tata bahasa. Jawab pertanyaan pengguna secara ringkas dan lugas."

# =============================================================
# 💻 TAB 1: Debugging & Analisis Kode (Tanpa Memori)
# =============================================================
def coding_tab():
    st.header("💻 Debugging & Analisis Kode")
    st.write("Tempelkan kode Python Anda. AI akan menganalisisnya, mencari *bug*, dan memberikan saran.")
    
    user_code = st.text_area("Tempelkan kode Python kamu di sini:", height=200, key="code_input")

    if st.button("Analisis Kode", type="primary"):
        if user_code.strip():
            with st.spinner("Menganalisis kode..."):
                prompt = f"Analisis, temukan bug, dan koreksi kode Python berikut dengan penjelasan yang membangun:\n```python\n{user_code}\n```"
                
                try:
                    # Menggunakan generate_content (sekali tembak)
                    response = client.models.generate_content(
                        model=MODEL_NAME, 
                        contents=prompt,
                        config=types.GenerateContentConfig(system_instruction=QUICK_INSTRUCTION)
                    )
                    st.markdown("### 📋 Hasil Analisis:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error saat analisis: {e}")
        else:
            st.warning("Masukkan kode Python terlebih dahulu.")

# =============================================================
# 📝 TAB 2: Quiz Sederhana (Demo Widget)
# =============================================================
def quiz_tab():
    st.header("📝 Quiz Pembelajaran (Demo Widget)")
    st.write("Ini adalah contoh Quiz yang dibuat menggunakan widget Streamlit.")

    # Data Quiz
    soal = "Apa fungsi utama dari 'st.session_state' di Streamlit?"
    pilihan = [
        "A. Menyimpan data ke database",
        "B. Membuat tata letak aplikasi",
        "C. Mempertahankan variabel antar re-run (memori)",
        "D. Menjalankan skrip Python dari server"
    ]
    jawaban_benar = "C. Mempertahankan variabel antar re-run (memori)"

    st.markdown(f"**Soal:** {soal}")
    jawaban = st.radio("Pilih jawabanmu:", pilihan)

    if st.button("Cek Jawaban"):
        if jawaban == jawaban_benar:
            st.success("✅ Benar! Itu penting untuk membuat aplikasi interaktif.")
        else:
            st.error(f"❌ Salah. Jawaban yang benar adalah: {jawaban_benar}.")

# =============================================================
# ⚡ TAB 3: Tanya Cepat (Quick Ask)
# =============================================================
def quick_tab():
    st.header("⚡ Tanya Cepat AI")
    st.write("Ketik pertanyaan singkat dan dapatkan jawaban instan.")
    
    q = st.text_input("Pertanyaanmu (Tanpa Memori):")
    if st.button("Jawab Sekarang"):
        if q.strip():
            with st.spinner("Menjawab..."):
                try:
                    # Panggilan GENERATE_CONTENT (Tanpa Memori)
                    response = client.models.generate_content(
                        model=MODEL_NAME, 
                        contents=q,
                        config=types.GenerateContentConfig(system_instruction=QUICK_INSTRUCTION)
                    )
                    st.markdown("### Jawaban:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error saat menjawab: {e}")
        else:
            st.warning("Masukkan pertanyaan terlebih dahulu.")

# =============================================================
# 🏁 MAIN APP EXECUTION
# =============================================================
def main():
    tab1, tab2, tab3 = st.tabs(["💻 Debugging", "📝 Quiz Demo", "⚡ Tanya Cepat"])
    with tab1:
        coding_tab()
    with tab2:
        quiz_tab()
    with tab3:
        quick_tab()

if __name__ == "__main__":
    main()