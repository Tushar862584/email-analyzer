# Logger setup placeholder
import logging
import yaml
from pathlib import Path

def setup_logger():
    #CONFIG = yaml.safe_load(open("config/settings.yaml"))
    current_dir = Path(__file__).parent 
    config_path = current_dir.parent / "config" / "settings.yaml"
    with open(config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)
    logging.basicConfig( 
        filename=CONFIG['log']['path'],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    return logging.getLogger("ElizaLogger")