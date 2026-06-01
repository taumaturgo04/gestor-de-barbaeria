import json
import logging
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("utils.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def campo_vazio(texto):
    return texto is None or str(texto).strip() == ""

def campo_numerico(texto):
    return texto is not None and str(texto).strip().isdigit()

def campo_apenas_letras(texto):
    valor = str(texto).strip() if texto else ""
    return valor != "" and all(caractere.isalpha() or caractere.isspace() for caractere in valor)

def campo_decimal_positivo(texto):
    try:
        return float(str(texto).strip()) > 0
    except (TypeError, ValueError):
        return False

def campo_inteiro_positivo(texto):
    try:
        return int(str(texto).strip()) >= 0
    except (TypeError, ValueError):
        return False

def validar_data_hora(texto):
    try:
        datetime.strptime(str(texto).strip(), "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def _calcular_proximo_id(nome_ficheiro, prefixo):
    if not os.path.exists(nome_ficheiro):
        return 1
    try:
        with open(nome_ficheiro, "r", encoding="utf-8") as f:
            dados = json.load(f)
        numeros = []
        for chave in dados.keys():
            parte_num = chave.lstrip(prefixo)
            if parte_num.isdigit():
                numeros.append(int(parte_num))
        return max(numeros) + 1 if numeros else 1
    except Exception:
        return 1

def gerar_id_barbearia():
    n = _calcular_proximo_id("barbearias.json", "BR")
    return f"BR{n:03d}"

def gerar_id_cliente():
    n = _calcular_proximo_id("clientes.json", "C")
    return f"C{n:03d}"

def gerar_id_barbeiro():
    n = _calcular_proximo_id("barbeiros.json", "B")
    return f"B{n:03d}"

def gerar_id_agendamento():
    n = _calcular_proximo_id("agendamentos.json", "A")
    return f"A{n:03d}"

def gerar_id_produto():
    n = _calcular_proximo_id("produtos.json", "P")
    return f"P{n:03d}"

