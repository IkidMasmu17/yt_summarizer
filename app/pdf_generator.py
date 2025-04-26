from fpdf import FPDF
import os

def save_to_pdf(content: str, filename: str) -> str:
    """Versi lebih robust dengan penanganan teks khusus"""
    try:
        # Pastikan direktori ada
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", filename)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Handle bullet points dan paragraf
        if content.startswith("•"):
            items = content.split("•")
            for item in items:
                if item.strip():
                    pdf.multi_cell(0, 10, "• " + item.strip())
                    pdf.ln(5)
        else:
            pdf.multi_cell(0, 10, content)
        
        pdf.output(path)
        return path
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        # Fallback - buat file teks biasa
        with open(path + ".txt", "w") as f:
            f.write(content)
        return path + ".txt"