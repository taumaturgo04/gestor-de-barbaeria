import json
import os
import logging
from utils import campo_vazio, gerar_id_cliente

FICHEIRO_CLIENTES = "clientes.json"
clientes = {}

logger = logging.getLogger(__name__)

def guardar_clientes():
    try:
        with open(FICHEIRO_CLIENTES, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Erro ao guardar clientes: %s", str(e))

def carregar_clientes():
    global clientes
    if os.path.exists(FICHEIRO_CLIENTES):
        try:
            with open(FICHEIRO_CLIENTES, "r", encoding="utf-8") as f:
                clientes = json.load(f)
        except Exception:
            clientes = {}

def criar_cliente(id_barbearia, nome, telefone, nif, iban, morada, email):
    carregar_clientes()
    if campo_vazio(nome) or campo_vazio(id_barbearia):
        return 401, "Nome e ID Barbearia são obrigatórios."

    id_c = gerar_id_cliente()
    clientes[id_c] = {
        "id_barbearia": str(id_barbearia).strip(),
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip()
    }
    guardar_clientes()
    return 201, clientes[id_c]

def listar_clientes():
    carregar_clientes()
    return 200, clientes

def consultar_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    return 200, clientes[id_cliente]

def atualizar_cliente(id_cliente, id_barbearia, nome, telefone, nif, iban, morada, email):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    if campo_vazio(nome) or campo_vazio(id_barbearia):
        return 401, "Nome e ID Barbearia são obrigatórios."

    clientes[id_cliente] = {
        "id_barbearia": str(id_barbearia).strip(),
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip()
    }
    guardar_clientes()
    return 200, clientes[id_cliente]

def remover_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    removido = clientes.pop(id_cliente)
    guardar_clientes()
    return 200, removido
