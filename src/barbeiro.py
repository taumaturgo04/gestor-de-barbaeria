import json
import os
import logging
from utils import campo_vazio, gerar_id_barbeiro

FICHEIRO_BARBEIROS = "barbeiros.json"
barbeiros = {}

logger = logging.getLogger(__name__)

def guardar_barbeiros():
    try:
        with open(FICHEIRO_BARBEIROS, "w", encoding="utf-8") as f:
            json.dump(barbeiros, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Erro ao guardar barbeiros: %s", str(e))

def carregar_barbeiros():
    global barbeiros
    if os.path.exists(FICHEIRO_BARBEIROS):
        try:
            with open(FICHEIRO_BARBEIROS, "r", encoding="utf-8") as f:
                barbeiros = json.load(f)
        except Exception:
            barbeiros = {}

def criar_barbeiro(nome, especialidade, telefone, nif, iban, morada, email, id_barbearia):
    carregar_barbeiros()
    if campo_vazio(nome) or campo_vazio(id_barbearia):
        return 401, "Nome e ID Barbearia são obrigatórios."

    id_b = gerar_id_barbeiro()
    barbeiros[id_b] = {
        "nome": nome.strip(),
        "especialidade": especialidade.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
        "id_barbearia": str(id_barbearia).strip()
    }
    guardar_barbeiros()
    return 201, barbeiros[id_b]

def listar_barbeiros():
    carregar_barbeiros()
    return 200, barbeiros

def consultar_barbeiro(id_barbeiro):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."
    return 200, barbeiros[id_barbeiro]

def atualizar_barbeiro(id_barbeiro, nome, especialidade, telefone, nif, iban, morada, email, id_barbearia):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."
    if campo_vazio(nome) or campo_vazio(id_barbearia):
        return 401, "Nome e ID Barbearia são obrigatórios."

    barbeiros[id_barbeiro] = {
        "nome": nome.strip(),
        "especialidade": especialidade.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
        "id_barbearia": str(id_barbearia).strip()
    }
    guardar_barbeiros()
    return 200, barbeiros[id_barbeiro]

def remover_barbeiro(id_barbeiro):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."
    removido = barbeiros.pop(id_barbeiro)
    guardar_barbeiros()
    return 200, removido
