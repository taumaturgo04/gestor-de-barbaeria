import json
import os

from barbeiro import consultar_barbeiro
from cliente import consultar_cliente
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora
from logger import get_logger

logger = get_logger(__name__)

FICHEIRO_AGENDAMENTOS = "agendamentos.json"

agendamentos = {}


# ==========================
# Persistência
# ==========================
def guardar_agendamentos():
    with open(FICHEIRO_AGENDAMENTOS, "w", encoding="utf-8") as ficheiro:
        json.dump(agendamentos, ficheiro, indent=4, ensure_ascii=False)


def carregar_agendamentos():
    global agendamentos
    if os.path.exists(FICHEIRO_AGENDAMENTOS):
        with open(FICHEIRO_AGENDAMENTOS, "r", encoding="utf-8") as ficheiro:
            agendamentos = json.load(ficheiro)
    else:
        agendamentos = {}


# ==========================
# CREATE
# ==========================
def criar_agendamento(data_hora, id_cliente, id_barbeiro, servico, id_barbearia):
    carregar_agendamentos()

    if campo_vazio(data_hora) or campo_vazio(id_cliente) or campo_vazio(id_barbeiro) or campo_vazio(servico) or campo_vazio(id_barbearia):
        logger.error("Tentativa de criar agendamento com campos vazios")
        return 401, "Nao pode deixar campos vazios."

    if not validar_data_hora(data_hora):
        logger.error(f"Data e hora inválidas: {data_hora}")
        return 500, "Data e hora invalidas. Utilize formato YYYY-MM-DD HH:MM"

    # CORRIGIDO: consultar_cliente devolve (code, {id: dict}) — extrair o dict interior
    codigo_cliente, resultado_cliente = consultar_cliente(id_cliente)
    if codigo_cliente != 200:
        logger.error(f"Cliente não encontrado: {id_cliente}")
        return 404, "Cliente nao encontrado."
    cliente = list(resultado_cliente.values())[0]

    # CORRIGIDO: consultar_barbeiro devolve (code, dict) directamente
    codigo_barbeiro, barbeiro = consultar_barbeiro(id_barbeiro)
    if codigo_barbeiro != 200:
        logger.error(f"Barbeiro não encontrado: {id_barbeiro}")
        return 404, "Barbeiro nao encontrado."

    id_agendamento = gerar_id_agendamento()
    agendamento = {
        "data_hora": data_hora.strip(),
        "id_cliente": id_cliente.strip(),
        "cliente": cliente["nome"],
        "id_barbeiro": id_barbeiro.strip(),
        "barbeiro": barbeiro["nome"],
        "servico": servico.strip(),
        "id_barbearia": id_barbearia.strip(),
        "status": "Pendente",
    }
    agendamentos[id_agendamento] = agendamento
    guardar_agendamentos()

    logger.info(f"Agendamento criado: {id_agendamento}")
    return 201, agendamento


# ==========================
# READ ALL
# ==========================
def listar_agendamentos():
    carregar_agendamentos()
    logger.info("Listagem de agendamentos solicitada. Total: %d", len(agendamentos))

    if not agendamentos:
        return 404, "Nao existem agendamentos registados."

    return 200, agendamentos


# ==========================
# READ ONE
# ==========================
def consultar_agendamento(id_agendamento):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        logger.warning("Agendamento não encontrado: %s", id_agendamento)
        return 404, "Agendamento nao encontrado."

    logger.info("Agendamento consultado: %s", id_agendamento)
    return 200, agendamentos[id_agendamento]


# ==========================
# UPDATE STATUS
# ==========================
def atualizar_status(id_agendamento, novo_status):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        logger.warning("Agendamento não encontrado para atualização: %s", id_agendamento)
        return 404, "Agendamento nao encontrado."

    if campo_vazio(novo_status):
        return 401, "O status nao pode estar vazio."

    agendamentos[id_agendamento]["status"] = novo_status.strip()
    guardar_agendamentos()

    logger.info("Status do agendamento %s atualizado para: %s", id_agendamento, novo_status)
    return 200, agendamentos[id_agendamento]


# ==========================
# DELETE
# ==========================
def eliminar_agendamento(id_agendamento):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        logger.warning("Agendamento não encontrado para eliminação: %s", id_agendamento)
        return 404, "Agendamento nao encontrado."

    agendamento_removido = agendamentos.pop(id_agendamento)
    guardar_agendamentos()

    logger.info("Agendamento eliminado: %s", id_agendamento)
    return 200, agendamento_removido
