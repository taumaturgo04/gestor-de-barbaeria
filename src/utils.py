import json
import logging
import os
from datetime import datetime

# ==========================
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("utils.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


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
# Geradores de ID — com persistência para evitar colisões entre sessões
# CORRIGIDO: os contadores são inicializados a partir dos dados já guardados,
#            evitando IDs duplicados quando o programa é reiniciado.
# ==========================
def _calcular_proximo_id(ficheiro, prefixo):
    """Lê o ficheiro JSON e devolve o próximo ID numérico disponível."""
    if not os.path.exists(ficheiro):
        return 1
    try:
        with open(ficheiro, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if not dados:
            return 1
        # Extrai a parte numérica de cada chave e devolve o máximo + 1
        numeros = []
        for chave in dados.keys():
            parte_num = chave.lstrip(prefixo)
            if parte_num.isdigit():
                numeros.append(int(parte_num))
        return max(numeros) + 1 if numeros else 1
    except Exception:
        return 1


def gerar_id_cliente():
    n = _calcular_proximo_id("clientes.json", "C")
    id_cliente = f"C{n:03d}"
    logger.debug("Gerado ID Cliente: %s", id_cliente)
    return id_cliente


def gerar_id_barbeiro():
    n = _calcular_proximo_id("barbeiros.json", "B")
    id_barbeiro = f"B{n:03d}"
    logger.debug("Gerado ID Barbeiro: %s", id_barbeiro)
    return id_barbeiro


def gerar_id_utilizador():
    n = _calcular_proximo_id("utilizadores.json", "U")
    id_utilizador = f"U{n:03d}"
    logger.debug("Gerado ID Utilizador: %s", id_utilizador)
    return id_utilizador


def gerar_id_agendamento():
    n = _calcular_proximo_id("agendamentos.json", "A")
    id_agendamento = f"A{n:03d}"
    logger.debug("Gerado ID Agendamento: %s", id_agendamento)
    return id_agendamento


def gerar_id_produto():
    n = _calcular_proximo_id("produtos.json", "P")
    id_produto = f"P{n:03d}"
    logger.debug("Gerado ID Produto: %s", id_produto)
    return id_produto


def gerar_id_barbearia():
    n = _calcular_proximo_id("barbearias.json", "BR")
    id_barbearia = f"BR{n:03d}"
    logger.debug("Gerado ID Barbearia: %s", id_barbearia)
    return id_barbearia

