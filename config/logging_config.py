import logging
import logging.config
import os

def setup_logging(
    default_level=logging.INFO,
):
    """Setup logging configuration"""
    base_path = os.path.abspath(__file__)
    config_path = os.path.join(base_path, 'config', 'logging.yaml')
        
    import yaml
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
                    
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)