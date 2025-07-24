# Logger setup placeholder
import logging
import yaml

def setup_logger():
    CONFIG = yaml.safe_load(open("config/settings.yaml"))
    logging.basicConfig(
        filename=CONFIG['log']['path'],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    return logging.getLogger("ElizaLogger")