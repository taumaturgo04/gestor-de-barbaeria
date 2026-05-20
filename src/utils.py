import logging
from datetime import datetime

# ==========================
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("utils.log", encoding="utf-8"),
        logging.StreamHandler()  # Mostra também no terminal
    ]
)

logger = logging.getLogger(__name__)

# Variáveis globais para controlo de IDs
proximo_id_cliente = 1
proximo_id_barbeiro = 1
proximo_id_utilizador = 1
proximo_id_agendamento = 1
proximo_id_produto = 1
proximo_id_barbearia = 1


# ==========================
# Funções de Validação
# ==========================
def campo_vazio(texto):
    resultado = texto is None or texto.strip() == ""
    if resultado:
        logger.debug("campo_vazio: Campo vazio ou None detectado")
    return resultado


def campo_numerico(texto):
    resultado = texto is not None and texto.strip().isdigit()
    if not resultado and texto is not None:
        logger.warning("campo_numerico falhou: '%s'", texto)
    return resultado


def campo_apenas_letras(texto):
    valor = texto.strip() if texto else ""
    resultado = valor != "" and all(caractere.isalpha() or caractere.isspace() for caractere in valor)
    if not resultado and texto is not None:
        logger.warning("campo_apenas_letras falhou: '%s'", texto)
    return resultado


def campo_decimal_positivo(texto):
    try:
        resultado = float(str(texto).strip()) > 0
    except (TypeError, ValueError):
        resultado = False
    
    if not resultado and texto is not None:
        logger.warning("campo_decimal_positivo falhou: '%s'", texto)
    return resultado


def campo_inteiro_positivo(texto):
    try:
        resultado = int(str(texto).strip()) > 0
    except (TypeError, ValueError):
        resultado = False
    
    if not resultado and texto is not None:
        logger.warning("campo_inteiro_positivo falhou: '%s'", texto)
    return resultado


def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        logger.warning("validar_data falhou: '%s'", data_texto)
        return False


def validar_data_hora(data_hora_texto):
    try:
        datetime.strptime(data_hora_texto, "%Y-%m-%d %H:%M")
        return True
    except (TypeError, ValueError):
        logger.warning("validar_data_hora falhou: '%s'", data_hora_texto)
        return False


# ==========================
# Geradores de ID
# ==========================
def gerar_id_cliente():
    global proximo_id_cliente
    id_cliente = f"C{proximo_id_cliente:03d}"
    proximo_id_cliente += 1
    logger.debug("Gerado ID Cliente: %s", id_cliente)
    return id_cliente


def gerar_id_barbeiro():
    global proximo_id_barbeiro
    id_barbeiro = f"B{proximo_id_barbeiro:03d}"
    proximo_id_barbeiro += 1
    logger.debug("Gerado ID Barbeiro: %s", id_barbeiro)
    return id_barbeiro


def gerar_id_utilizador():
    global proximo_id_utilizador
    id_utilizador = f"U{proximo_id_utilizador:03d}"
    proximo_id_utilizador += 1
    logger.debug("Gerado ID Utilizador: %s", id_utilizador)
    return id_utilizador


def gerar_id_agendamento():
    global proximo_id_agendamento
    id_agendamento = f"A{proximo_id_agendamento:03d}"
    proximo_id_agendamento += 1
    logger.debug("Gerado ID Agendamento: %s", id_agendamento)
    return id_agendamento


def gerar_id_produto():
    global proximo_id_produto
    id_produto = f"P{proximo_id_produto:03d}"
    proximo_id_produto += 1
    logger.debug("Gerado ID Produto: %s", id_produto)
    return id_produto


def gerar_id_barbearia():
    global proximo_id_barbearia
    id_barbearia = f"BR{proximo_id_barbearia:03d}"
    proximo_id_barbearia += 1
    logger.debug("Gerado ID Barbearia: %s", id_barbearia)
    return id_barbearia
