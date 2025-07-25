# core/normalizer.py (Final Version for Live Report Update)

import csv
import os
# The 'datetime' import is no longer needed here
from core.logger import setup_logger
import yaml
from pathlib import Path

logger = setup_logger()
current_dir = Path(__file__).parent 
config_path = current_dir.parent / "config" / "settings.yaml"
with open(config_path, 'r') as f:
    CONFIG = yaml.safe_load(f)

def normalize_and_write_csv(data, output_path):
    """
    Writes a list of data to a single CSV file at the specific path provided.
    """
    # Ensure the directory for the output path exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Use the 'output_path' passed from the email_handler
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CONFIG['output']['schema'])
        writer.writeheader()
        writer.writerows(data)
        
    logger.info(f"CSV file written: {output_path}")
    return output_path