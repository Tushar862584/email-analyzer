# FTP upload logic placeholder
import paramiko
import os
from core.logger import setup_logger
import yaml

logger = setup_logger()
CONFIG = yaml.safe_load(open("config/settings.yaml"))

def upload_to_ftp(local_path):
    transport = paramiko.Transport((CONFIG['ftp']['host'], CONFIG['ftp']['port']))
    transport.connect(username=CONFIG['ftp']['username'], password=CONFIG['ftp']['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    remote_path = os.path.join(CONFIG['ftp']['target_dir'], os.path.basename(local_path))
    sftp.put(local_path, remote_path)
    logger.info(f"File uploaded to FTP: {remote_path}")
    sftp.close()
    transport.close()