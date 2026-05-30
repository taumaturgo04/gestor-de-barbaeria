import logging
import os

def get_logger(name):
    logger = logging.getLogger(name)
    
    # Evita duplicar handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Ficheiro de log
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/barbearia.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

