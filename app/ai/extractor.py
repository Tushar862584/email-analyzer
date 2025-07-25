# ai/extractor.py (Final Corrected Version)

import pytesseract
import fitz
from core.logger import setup_logger
import pandas as pd
from docx import Document
import re # <-- Make sure this import is at the top of your file

logger = setup_logger()

def extract_data_from_file(filepath, original_filename):
    """
    Extracts data using new, more precise regex patterns tailored to your documents.
    """
    ext = original_filename.split('.')[-1].lower()
    text = ""
    try:
        # This section to read the file and get 'text' is correct and unchanged
        if ext == "pdf":
            doc = fitz.open(filepath)
            text = "".join([page.get_text() for page in doc])
        elif ext in ["xlsx", "csv"]:
            df = pd.read_excel(filepath) if ext == "xlsx" else pd.read_csv(filepath)
            return df.to_dict('records')
        elif ext == "docx":
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            text = pytesseract.image_to_string(filepath)

        if not text:
            logger.warning(f"Could not extract any text from {original_filename}")
            return []

        # --- UPDATED AND MORE PRECISE PATTERNS ---
        
        # 1. These patterns are tailored to the invoice format you last shared.
        patterns = {
            'Invoice No': r"Invoice No:\s*(INV-\d{4}-\d{3})",
            'Amount': r"Amount[:\s]+[I₹]?\s*([\d,]+\.\d{2})",
            'Date': r"Date[:\s]+(\d{2}-\d{2}-\d{4})",
            'UTR': r"UTR No[:\s]+(\w+)",
            'Customer': r"(?:Billed To|Bill To)[:\s]+([\s\S]+?)(?=Contact:|S\.No|$)"
        }

        extracted_data = {}
        # 2. Search for each pattern in the text
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                found_text = match.group(1).strip()
                # Clean up all newlines and extra spaces for a proper single-line CSV
                cleaned_text = ' '.join(found_text.split())
                extracted_data[key] = cleaned_text
            else:
                extracted_data[key] = "Not Found"

        # 3. Return the real, extracted data
        if any(value != "Not Found" for value in extracted_data.values()):
            return [extracted_data]
        else:
            logger.warning(f"Could not find any invoice data patterns in {original_filename}")
            return []

    except Exception as e:
        logger.error(f"Error extracting data from '{original_filename}': {e}", exc_info=True)
        return None