import streamlit as st
from app.downloader import download_audio
from app.transcriber import transcribe_audio
from app.summarizer import summarize_text
from app.pdf_generator import save_to_pdf

# Inisialisasi session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""

st.title("🎥 YouTube Summarizer AI Pro")
url = st.text_input("Masukkan link YouTube:")

if st.button("Proses") or st.session_state.processed:
    if not st.session_state.processed:
        with st.spinner("Mengunduh audio..."):
            audio_path = download_audio(url)
        
        with st.spinner("Mentranskripsi audio..."):
            st.session_state.transcript = transcribe_audio(audio_path)
            st.session_state.processed = True
    
    # Tampilkan transkrip
    st.subheader("📝 Transkrip Lengkap")
    clean_transcript = "\n\n".join([p.strip() for p in st.session_state.transcript.split("\n") if p.strip()])
    st.text_area("Transkrip", clean_transcript, height=300, key="transcript_area")
    
    if len(st.session_state.transcript.split()) < 50:
        st.error("Transkrip terlalu pendek")
    else:
        output_format = st.radio(
            "Format Output:",
            ("Poin-poin penting", "Paragraf penuh"),
            index=0 if not st.session_state.processed else 1,
            key="output_format"
        )
        
        if not st.session_state.summary or st.button("Generate Ulang Rangkuman"):
            with st.spinner("Merangkum konten..."):
                st.session_state.summary = summarize_text(
                    st.session_state.transcript,
                    mode="bullet_points" if output_format == "Poin-poin penting" else "paragraph"
                )
        
        st.subheader("📌 Hasil Rangkuman")
        st.text_area("Rangkuman", st.session_state.summary, height=300, key="summary_area")
        
        # Sistem download
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner("Menyiapkan PDF Rangkuman..."):
                pdf_summary_path = save_to_pdf(st.session_state.summary, "summary.pdf")
                with open(pdf_summary_path, "rb") as f:
                    st.download_button(
                        "💾 Unduh Rangkuman (PDF)",
                        f,
                        file_name="rangkuman.pdf",
                        key="dl_summary"
                    )
        
        with col2:
            with st.spinner("Menyiapkan PDF Transkrip..."):
                pdf_transcript_path = save_to_pdf(clean_transcript, "transcript.pdf")
                with open(pdf_transcript_path, "rb") as f:
                    st.download_button(
                        "📄 Unduh Transkrip Lengkap (PDF)",
                        f,
                        file_name="transkrip_lengkap.pdf",
                        key="dl_transcript"
                    )

# Tombol reset
if st.session_state.processed and st.button("🔄 Proses Video Baru"):
    st.session_state.processed = False
    st.session_state.transcript = ""
    st.session_state.summary = ""
    st.experimental_rerun()