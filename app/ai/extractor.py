# AI Extraction logic placeholder
import pytesseract
import fitz
from core.logger import setup_logger
import pandas as pd
from docx import Document

logger = setup_logger()

def extract_data_from_file(filepath):
    ext = filepath.split('.')[-1].lower()
    data = []
    try:
        if ext == "pdf":
            doc = fitz.open(filepath)
            text = "".join([page.get_text() for page in doc])
        elif ext in ["xlsx", "csv"]:
           
            df = pd.read_excel(filepath) if ext == "xlsx" else pd.read_csv(filepath)
            data = df.to_dict('records')
            return data
        elif ext == "docx":
            
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            text = pytesseract.image_to_string(filepath)

        # Simulated parsing (replace with AI model inference)
        for line in text.splitlines():
            if "Invoice" in line:
                data.append({
                    "Invoice No": "INV123",
                    "Amount": 1000,
                    "Date": "2025-07-20",
                    "UTR": "UTR001",
                    "Customer": "CustomerA"
                })
        return data
    except Exception as e:
        logger.error(f"Error extracting data: {e}")
        return None