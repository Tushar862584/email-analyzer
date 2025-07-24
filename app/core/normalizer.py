# Data normalization logic placeholder
import csv, os
from datetime import datetime
from core.logger import setup_logger
import yaml

logger = setup_logger()
CONFIG = yaml.safe_load(open("config/settings.yaml"))

def normalize_and_write_csv(data):
    output_file = os.path.join(CONFIG['output']['dir'], f"advice_{datetime.now().isoformat()}.csv")
    os.makedirs(CONFIG['output']['dir'], exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CONFIG['output']['schema'])
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"CSV file written: {output_file}")
    return output_file