import streamlit as st
from app.downloader import download_audio
from app.transcriber import transcribe_audio
from app.summarizer import summarize_text
from app.pdf_generator import save_to_pdf

st.title("🎥 YouTube Summarizer AI")
url = st.text_input("Masukkan link YouTube:")

if st.button("Proses"):
    with st.spinner("Mengunduh audio..."):
        audio_path = download_audio(url)
    
    with st.spinner("Mentranskripsi audio..."):
        transcript = transcribe_audio(audio_path)
        st.text_area("Transkrip Lengkap:", transcript, height=200)  # Debugging
    
    if not transcript or len(transcript.split()) < 30:
        st.error("Transkrip terlalu pendek atau kosong. Coba video lain.")
    else:
        with st.spinner("Merangkum..."):
            summary = summarize_text(transcript)
            st.text_area("Hasil Rangkuman:", summary, height=200)
            
            pdf_path = save_to_pdf(summary)
            with open(pdf_path, "rb") as file:
                st.download_button("💾 Unduh PDF", file, file_name="rangkuman.pdf")