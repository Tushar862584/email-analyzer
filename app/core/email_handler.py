# core/email_handler.py (Final Corrected Version)

from imapclient import IMAPClient
from email import message_from_bytes
import os
import tempfile
import zipfile
import yaml
from pathlib import Path
from ai.extractor import extract_data_from_file
from core.normalizer import normalize_and_write_csv
from core.ftp_uploader import upload_to_ftp
from core.logger import setup_logger

logger = setup_logger()

# Load configuration safely
current_dir = Path(__file__).parent
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
    CONFIG = yaml.safe_load(f)

def process_emails():
    """
    Connects to the email server, finds unread emails, and processes their attachments.
    """
    try:
        with IMAPClient(CONFIG['email']['server']) as server:
            server.login(CONFIG['email']['username'], CONFIG['email']['password'])
            server.select_folder(CONFIG['email']['folder'])
            logger.info(f"Successfully connected to email server and selected folder '{CONFIG['email']['folder']}'.")
            
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
                                # Create a temporary file to save the attachment safely
                                with tempfile.NamedTemporaryFile(delete=False) as temp_f:
                                    temp_filepath = temp_f.name
                                    temp_f.write(part.get_payload(decode=True))
                                
                                # Now that the file is fully written and closed, process it
                                logger.info(f"Attachment '{filename}' saved, now processing.")
                                process_file(temp_filepath, filename)
                            finally:
                                # Make sure the temporary file is always deleted
                                if temp_filepath and os.path.exists(temp_filepath):
                                    os.unlink(temp_filepath)
                                    logger.info(f"Cleaned up temp file: {temp_filepath}")
                else:
                    # Handle non-multipart emails if necessary
                    logger.info("Email is not multipart, checking for body text.")
                    if 'text/plain' in msg.get_content_type():
                         body = msg.get_payload(decode=True).decode()
                         process_file_from_text(body)

    except Exception as e:
        logger.error(f"An error occurred in process_emails: {e}", exc_info=True)


def process_file(file_path, filename):
    """
    Processes a single file: if it's a ZIP, extract and recurse; otherwise, extract data.
    """
    logger.info(f"Processing file: {filename} at path: {file_path}")
    ext = filename.split('.')[-1].lower()
    if ext == "zip":
        try:
            # Use a temporary directory that cleans itself up for ZIP extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(file_path, 'r') as zf:
                    zf.extractall(path=temp_dir)
                    logger.info(f"Extracted ZIP contents to temporary directory {temp_dir}")
                    for f_name in zf.namelist():
                        full_path = os.path.join(temp_dir, f_name)
                        if os.path.isfile(full_path):
                            process_file(full_path, f_name)
        except zipfile.BadZipFile:
            logger.error(f"File {filename} is not a valid ZIP file or is corrupted.")
        except Exception as e:
            logger.error(f"Failed to process ZIP file {filename}. Error: {e}", exc_info=True)
    else:
        # Pass both the temporary file path AND the original filename to the extractor
        extracted_data = extract_data_from_file(file_path, filename)
        if extracted_data:
            logger.info(f"Successfully extracted data from {filename}.")
            csv_path = normalize_and_write_csv(extracted_data)
            if csv_path:
                upload_to_ftp(csv_path)
        else:
            logger.warning(f"No data was extracted from {filename}.")


def process_file_from_text(text):
    """
    Placeholder for processing data found directly in an email body.
    """
    logger.info("Parsing inline text (not implemented in detail).")
    # Future logic could go here to extract data from email body text
    pass