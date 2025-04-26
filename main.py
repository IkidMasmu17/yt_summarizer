import streamlit as st
from app.downloader import download_audio
from app.transcriber import transcribe_audio
from app.summarizer import summarize_text
from app.pdf_generator import save_to_pdf

st.title("🎥 YouTube Summarizer AI Pro")
url = st.text_input("Masukkan link YouTube:")

if st.button("Proses"):
    with st.spinner("Mengunduh audio..."):
        audio_path = download_audio(url)
    
    with st.spinner("Mentranskripsi audio..."):
        transcript = transcribe_audio(audio_path)
        
        # Tampilkan transkrip lengkap
        st.subheader("📝 Transkrip Lengkap")
        clean_transcript = "\n\n".join([p.strip() for p in transcript.split("\n") if p.strip()])
        st.text_area("", clean_transcript, height=300, key="transcript")
    
    if not transcript or len(transcript.split()) < 50:
        st.error("Transkrip terlalu pendek atau kosong. Coba video lain.")
    else:
        # Pilihan output format
        output_format = st.radio(
            "Format Output:",
            ("Poin-poin penting", "Paragraf penuh"),
            horizontal=True
        )
        
        with st.spinner("Merangkum konten..."):
            summary = summarize_text(
                transcript,
                mode="bullet_points" if output_format == "Poin-poin penting" else "paragraph"
            )
            
            st.subheader("📌 Hasil Rangkuman")
            st.text_area("", summary, height=300, key="summary")
            
            # Pilihan download
            col1, col2 = st.columns(2)
            with col1:
                pdf_path = save_to_pdf(summary, "summary.pdf")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "💾 Unduh Rangkuman (PDF)",
                        f,
                        file_name="rangkuman.pdf"
                    )
            
            with col2:
                transcript_path = save_to_pdf(clean_transcript, "transcript.pdf")
                with open(transcript_path, "rb") as f:
                    st.download_button(
                        "📄 Unduh Transkrip Lengkap (PDF)",
                        f,
                        file_name="transkrip_lengkap.pdf"
                    )