import logging
import os
from datetime import datetime

def configurar_logging(nome_logger=__name__, nivel=logging.INFO):
    """Configuração centralizada de logging para o Gestor de Barbearia"""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    data_atual = datetime.now().strftime("%Y-%m-%d")
    ficheiro_log = f"logs/gestor_barbearia_{data_atual}.log"

    logging.basicConfig(
        level=nivel,
        format='%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(ficheiro_log, encoding="utf-8", mode='a'),
            logging.StreamHandler()
        ],
        force=True
    )

    logger = logging.getLogger(nome_logger)
    logger.info("=" * 85)
    logger.info("GESTOR DE BARBEARIA - Sistema Iniciado")
    logger.info(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Log: {ficheiro_log}")
    logger.info("=" * 85)
    
    return logger


def get_logger(nome=""):
    return logging.getLogger(nome if nome else __name__)

