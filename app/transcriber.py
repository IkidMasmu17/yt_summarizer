import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path, fp16=False)  # Nonaktifkan FP16 jika pakai CPU
    print(f"Panjang transkrip: {len(result['text'].split())} kata")  # Debug
    return result["text"]