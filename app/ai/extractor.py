# ai/extractor.py (Corrected Version)

import pytesseract
import fitz
from core.logger import setup_logger
import pandas as pd
from docx import Document

logger = setup_logger()

def extract_data_from_file(filepath, original_filename):
    """
    Extracts data from a file using the original filename to determine the type.
    """
    # Use the original filename to get the correct extension
    ext = original_filename.split('.')[-1].lower()
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
            # Fallback for image files
            text = pytesseract.image_to_string(filepath)

        # This is still a placeholder for real data extraction
        # It will add dummy data if the word "Invoice" is found in the text
        if text:
            for line in text.splitlines():
                if "invoice" in line.lower():
                    # Appending placeholder data for demonstration
                    data.append({
                        "Invoice No": "INV123",
                        "Amount": 1000,
                        "Date": "2025-07-20",
                        "UTR": "UTR001",
                        "Customer": "CustomerA"
                    })
                    break # Assuming one invoice per document for this example
        return data
        
    except Exception as e:
        logger.error(f"Error extracting data from '{original_filename}': {e}", exc_info=True)
        return None