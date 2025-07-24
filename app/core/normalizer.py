# Data normalization logic placeholder
import csv, os
from datetime import datetime
from core.logger import setup_logger
import yaml
from pathlib import Path

logger = setup_logger()
current_dir = Path(__file__).parent 
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)

def normalize_and_write_csv(data):
    output_file = os.path.join(CONFIG['output']['dir'], f"advice_{datetime.now().isoformat()}.csv")
    os.makedirs(CONFIG['output']['dir'], exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CONFIG['output']['schema'])
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"CSV file written: {output_file}")
    return output_file