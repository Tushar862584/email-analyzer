# core/email_handler.py (Final Version for Live Report Update)

from imapclient import IMAPClient
from email import message_from_bytes
import os
import tempfile
import zipfile
import yaml
from pathlib import Path
import csv # <-- Add this import
from ai.extractor import extract_data_from_file
from core.normalizer import normalize_and_write_csv
from core.ftp_uploader import upload_to_ftp, download_from_ftp # <-- Update this import
from core.logger import setup_logger

logger = setup_logger()

# Load configuration safely
current_dir = Path(__file__).parent
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
    CONFIG = yaml.safe_load(f)

def process_emails():
    """
    Downloads an existing report, adds new data from emails, and uploads it back.
    """
    # 1. DEFINE a fixed name and path for your live report
    report_filename = "live_report.csv"
    local_path = os.path.join(CONFIG['output']['dir'], report_filename)
    remote_path = os.path.join(CONFIG['ftp']['target_dir'], report_filename)

    # 2. DOWNLOAD and READ existing data from the report
    all_data = []
    if download_from_ftp(remote_path, local_path):
        try:
            with open(local_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                all_data = list(reader)
            logger.info(f"Read {len(all_data)} existing records from {report_filename}")
        except Exception as e:
            logger.error(f"Could not read downloaded report file '{local_path}'. Starting fresh. Error: {e}")
    
    # 3. PROCESS new emails and add to our data list
    try:
        with IMAPClient(CONFIG['email']['server']) as server:
            server.login(CONFIG['email']['username'], CONFIG['email']['password'])
            server.select_folder(CONFIG['email']['folder'])
            logger.info(f"Successfully connected and selected folder '{CONFIG['email']['folder']}'.")
            
            messages = server.search('UNSEEN')
            logger.info(f"Found {len(messages)} unread emails.")

            for uid in messages:
                msg_data = server.fetch(uid, ['RFC822'])
                msg = message_from_bytes(msg_data[uid][b'RFC822'])

                if msg.is_multipart():
                    for part in msg.walk():
                        filename = part.get_filename()
                        if filename:
                            temp_filepath = None
                            try:
                                with tempfile.NamedTemporaryFile(delete=False) as temp_f:
                                    temp_filepath = temp_f.name
                                    temp_f.write(part.get_payload(decode=True))
                                
                                extracted_data = process_file(temp_filepath, filename)
                                if extracted_data:
                                    all_data.extend(extracted_data) # Add new data to the list
                            finally:
                                if temp_filepath and os.path.exists(temp_filepath):
                                    os.unlink(temp_filepath)
        
        # 4. WRITE and UPLOAD the combined data
        if all_data:
            # Pass the fixed local_path to the writer function
            normalize_and_write_csv(all_data, local_path)
            upload_to_ftp(local_path)
        else:
            logger.info("No data to process or upload.")

    except Exception as e:
        logger.error(f"An error occurred in process_emails: {e}", exc_info=True)


def process_file(file_path, filename):
    """
    Processes a single file and RETURNS the extracted data.
    This function does not need to change.
    """
    logger.info(f"Processing file: {filename} at path: {file_path}")
    # ... (the rest of this function is correct and does not need to be changed) ...
    extracted_data = extract_data_from_file(file_path, filename)
    if extracted_data:
        logger.info(f"Successfully extracted data from {filename}.")
        return extracted_data
    else:
        logger.warning(f"No data was extracted from {filename}.")
        return None


def process_file_from_text(text):
    """
    Placeholder for processing data found directly in an email body.
    """
    logger.info("Parsing inline text (not implemented in detail).")
    pass