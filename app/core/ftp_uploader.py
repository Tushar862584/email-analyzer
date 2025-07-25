# core/ftp_uploader.py (Final Version with Download/Upload)

import paramiko
import os
from core.logger import setup_logger
import yaml
from pathlib import Path

logger = setup_logger()

# Load configuration safely
current_dir = Path(__file__).parent 
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
    CONFIG = yaml.safe_load(f)

def upload_to_ftp(local_path):
    """
    Connects to an SFTP server and uploads a file.
    """
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=CONFIG['ftp']['host'],
                port=CONFIG['ftp']['port'],
                username=CONFIG['ftp']['username'],
                password=CONFIG['ftp']['password']
            )
            with ssh.open_sftp() as sftp:
                remote_path = os.path.join(CONFIG['ftp']['target_dir'], os.path.basename(local_path))
                sftp.put(local_path, remote_path)
                logger.info(f"File uploaded to SFTP: {remote_path}")

    except Exception as e:
        logger.error(f"Failed to upload {local_path} via SFTP. Error: {e}", exc_info=True)


def download_from_ftp(remote_path, local_path):
    """
    Downloads a file from the SFTP server.
    Returns True on success, False if the file does not exist.
    """
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=CONFIG['ftp']['host'],
                port=CONFIG['ftp']['port'],
                username=CONFIG['ftp']['username'],
                password=CONFIG['ftp']['password']
            )
            with ssh.open_sftp() as sftp:
                sftp.get(remote_path, local_path)
                logger.info(f"Successfully downloaded {remote_path} to {local_path}")
                return True
                
    except FileNotFoundError:
        logger.warning(f"Remote file not found: {remote_path}. A new one will be created.")
        return False
    except Exception as e:
        logger.error(f"Failed to download {remote_path}. Error: {e}", exc_info=True)
        return False