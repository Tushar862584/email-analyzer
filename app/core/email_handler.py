# Email handling logic placeholder
from imapclient import IMAPClient
from email import message_from_bytes
import os, tempfile, zipfile
import yaml
from pathlib import Path
from ai.extractor import extract_data_from_file
from core.normalizer import normalize_and_write_csv
from core.ftp_uploader import upload_to_ftp
from core.logger import setup_logger

logger = setup_logger()

#CONFIG = yaml.safe_load(open("config/settings.yaml"))
current_dir = Path(__file__).parent 
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)

def process_emails():
    with IMAPClient(CONFIG['email']['server']) as server:
        server.login(CONFIG['email']['username'], CONFIG['email']['password'])
        server.select_folder(CONFIG['email']['folder'])
        messages = server.search('UNSEEN')
        for uid in messages:
            msg_data = server.fetch(uid, ['RFC822'])
            msg = message_from_bytes(msg_data[uid][b'RFC822'])

            if msg.is_multipart():
                for part in msg.walk():
                    filename = part.get_filename()
                    if filename:
                        with tempfile.NamedTemporaryFile(delete=False) as f:
                            f.write(part.get_payload(decode=True))
                            process_file(f.name, filename)
            else:
                logger.info("Email body text found. Extracting...")
                body = msg.get_payload(decode=True).decode()
                process_file_from_text(body)

def process_file(file_path, filename):
    ext = filename.split('.')[-1].lower()
    if ext == "zip":
        with zipfile.ZipFile(file_path) as zf:
            zf.extractall(path="temp")
            for f in zf.namelist():
                full_path = os.path.join("temp", f)
                process_file(full_path, f)
    else:
        extracted_data = extract_data_from_file(file_path)
        if extracted_data:
            csv_path = normalize_and_write_csv(extracted_data)
            upload_to_ftp(csv_path)

def process_file_from_text(text):
    # Simple parsing logic for inline text (can use regex/AI if needed)
    logger.info("Parsing inline text (not implemented in detail)")