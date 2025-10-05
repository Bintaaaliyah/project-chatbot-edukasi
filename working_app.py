import streamlit as st
import requests
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="Your Personal Code Cheatsheet",
    page_icon="💻",
    layout="wide"
)

# Styling sederhana
st.markdown("""
<style>
    .main-title { text-align: center; color: #0A84FF; font-size: 2.8rem; font-weight: 700;  margin-bottom: 1.5rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.15);  }
    .response-box { background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #1f77b4; }
    .sidebar-box { background-color: #e7f3ff; padding: 15px; border-radius: 8px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">💻 Cheatsheet Coding Cerdas</div>', unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; margin-bottom: 2rem;'>🚀 Siap bantu Anda menulis kode lebih cepat</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔑 Konfigurasi API")
    
    api_key = st.text_input("**Masukkan Kunci API Gemini Anda:**", 
                           type="password",
                           placeholder="Tempel kunci API di sini...")
    
   if not api_key:
        st.markdown("""
        <div style="
            background-color: #eaf4fc; 
            padding: 15px; 
            border-radius: 12px; 
            border-left: 6px solid #1f77b4;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-top: 10px;
        ">
            <h4 style="color: #1f77b4; margin-bottom: 8px;">🔐 Cara Mendapatkan Kunci API</h4>
            <ol style="color: #333; line-height: 1.6; font-size: 16px; padding-left: 20px;">
                <li>Kunjungi <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color:#1f77b4; font-weight:600;">Google AI Studio</a></li>
                <li>Login menggunakan akun Google kamu</li>
                <li>Klik tombol <b>"Create API Key"</b></li>
                <li>Salin dan tempel kunci tersebut ke kolom di atas</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

else:
        st.success("✅ Kunci API Siap!")

# Fungsi untuk memanggil API Gemini langsung
def panggil_api_gemini(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Error: Tidak ada respons dari API"
            
    except requests.exceptions.RequestException as e:
        return f"Error API: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Konten utama
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Apa yang Anda Butuhkan?")
    
    bahasa_pemrograman = st.selectbox(
        "**Bahasa Pemrograman**",
        ["Python", "JavaScript", "Java", "C++", "SQL", "HTML/CSS", "TypeScript", "Go", "Rust"],
        index=0
    )
    
    jenis_bantuan = st.selectbox(
        "**Jenis Bantuan**",
        ["Sintaks Kode", "Fungsi/Method", "Struktur Data", "Algoritma", "Best Practices", "Debugging", "Library/Framework"],
        index=0
    )

with col2:
    st.markdown("### 📝 Pertanyaan Anda")
    
    pertanyaan = st.text_area(
        "**Jelaskan apa yang ingin Anda pelajari:**",
        placeholder=f"Contoh:\n• Cara membaca file di {bahasa_pemrograman}?\n• Contoh method array di {bahasa_pemrograman}\n• Cara terbaik menangani error di {bahasa_pemrograman}",
        height=120
    )

# Generate respons
if st.button("🚀 Dapatkan Solusi Kode", type="primary", use_container_width=True):
    if pertanyaan and pertanyaan.strip():
        with st.spinner("🤖 Membuat solusi kode Anda..."):
            # Buat prompt yang ditingkatkan
            prompt = f"""
            Buatlah cheatsheet kode yang komprehensif dan ramah untuk pemula untuk {bahasa_pemrograman} dengan fokus pada {jenis_bantuan}.
            
            Permintaan spesifik pengguna: {pertanyaan}
            
            Tolong struktur respons Anda dengan:
            
            🎯 **Gambaran Konsep**: Penjelasan singkat
            💻 **Contoh Kode**: Kode bersih dengan komentar
            📝 **Penjelasan**: Bagaimana cara kerjanya
            💡 **Best Practices**: Tips penting
            ⚠️ **Kesalahan Umum**: Hal yang perlu dihindari
            
            Buatlah praktis dan mudah dipahami untuk pemula.
            Gunakan emoji untuk membuatnya menarik.
            """
            
            teks_respons = panggil_api_gemini(api_key, prompt)
            
            # Tampilkan respons
            st.markdown("---")
            st.markdown("## 📋 Solusi Kode Anda")
            st.markdown(f"*Untuk {bahasa_pemrograman} - {jenis_bantuan}*")
            
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(teks_respons)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Feedback
            st.markdown("---")
            st.markdown("### Apakah ini membantu?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Ya!", use_container_width=True):
                    st.success("🎉 Bagus! Selamat coding!")
            with col2:
                if st.button("👎 Bisa lebih baik", use_container_width=True):
                    st.info("💡 Coba lebih spesifik dalam pertanyaan Anda!")
            with col3:
                if st.button("🔄 Coba Lagi", use_container_width=True):
                    st.rerun()
    else:
        st.warning("⚠️ Silakan masukkan pertanyaan Anda!")

# Contoh cepat
with st.expander("🚀 **Butuh Inspirasi? Coba Ini:**", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🐍 Contoh Python**")
        st.markdown("- Penanganan file dengan manajemen error")
        st.markdown("- List comprehension vs loops")
        st.markdown("- Dekorator dijelaskan secara sederhana")
        
    with col2:
        st.markdown("**🌐 Pengembangan Web**")
        st.markdown("- Pola JavaScript async/await")
        st.markdown("- Contoh React hooks")
        st.markdown("- Layout CSS Grid/Flexbox")
        
    with col3:
        st.markdown("**💾 Data & API**")
        st.markdown("- Query SQL JOIN dijelaskan")
        st.markdown("- Best practices REST API")
        st.markdown("- Contoh parsing JSON")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Dibuat dengan menggunakan Streamlit & Google Gemini API • "
    "Asisten Belajar Kode Pribadi Anda"
    "</div>",
    unsafe_allow_html=True
)
