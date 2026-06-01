import json
import os
import logging
from utils import campo_vazio, gerar_id_barbearia

FICHEIRO_BARBEARIAS = "barbearias.json"
barbearias = {}

logger = logging.getLogger(__name__)


def guardar_barbearias():
    try:
        with open(FICHEIRO_BARBEARIAS, "w", encoding="utf-8") as f:
            json.dump(barbearias, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Erro ao guardar barbearias: %s", str(e))


def carregar_barbearias():
    global barbearias
    if os.path.exists(FICHEIRO_BARBEARIAS):
        try:
            with open(FICHEIRO_BARBEARIAS, "r", encoding="utf-8") as f:
                barbearias = json.load(f)
        except Exception:
            barbearias = {}


def criar_barbearia(nome, morada, nif):
    carregar_barbearias()
    if campo_vazio(nome) or campo_vazio(morada) or campo_vazio(nif):
        return 401, "Não pode deixar campos vazios."

    id_br = gerar_id_barbearia()
    barbearias[id_br] = {
        "nome": nome.strip(),
        "morada": morada.strip(),
        "nif": nif.strip()
    }
    guardar_barbearias()
    return 201, barbearias[id_br]


def listar_barbearias():
    carregar_barbearias()
    return 200, barbearias


def consultar_barbearia(id_barbearia):
    carregar_barbearias()
    if id_barbearia not in barbearias:
        return 404, "Barbearia não encontrada."
    return 200, barbearias[id_barbearia]


def atualizar_barbearia(id_barbearia, nome, morada, nif):
    carregar_barbearias()
    if id_barbearia not in barbearias:
        return 404, "Barbearia não encontrada."
    if campo_vazio(nome) or campo_vazio(morada) or campo_vazio(nif):
        return 401, "Campos não podem ficar vazios."

    barbearias[id_barbearia] = {
        "nome": nome.strip(),
        "morada": morada.strip(),
        "nif": nif.strip()
    }
    guardar_barbearias()
    return 200, barbearias[id_barbearia]


def remover_barbearia(id_barbearia):
    carregar_barbearias()
    if id_barbearia not in barbearias:
        return 404, "Barbearia não encontrada."
    removido = barbearias.pop(id_barbearia)
    guardar_barbearias()
    return 200, removido