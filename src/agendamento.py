import json
import os

from barbeiro import consultar_barbeiro
from cliente import consultar_cliente
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora


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
        return 401, "Nao pode deixar campos vazios."

    if not validar_data_hora(data_hora):
        return 500, "Data e hora invalidas. Utilize formato YYYY-MM-DD HH:MM"

    codigo_cliente, cliente = consultar_cliente(id_cliente)
    if codigo_cliente != 200:
        return 404, "Cliente nao encontrado."

    codigo_barbeiro, barbeiro = consultar_barbeiro(id_barbeiro)
    if codigo_barbeiro != 200:
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

    return 201, agendamento


# ==========================
# READ ALL
# ==========================
def listar_agendamentos():
    carregar_agendamentos()

    if not agendamentos:
        return 404, "Nao existem agendamentos registados."

    return 200, agendamentos


# ==========================
# READ ONE
# ==========================
def consultar_agendamento(id_agendamento):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    return 200, agendamentos[id_agendamento]


# ==========================
# UPDATE
# ==========================
def atualizar_status(id_agendamento, novo_status):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    if campo_vazio(novo_status):
        return 401, "Nao pode deixar campos vazios."

    agendamentos[id_agendamento]["status"] = novo_status.strip()
    guardar_agendamentos()

    return 200, agendamentos[id_agendamento]


# ==========================
# DELETE
# ==========================
def eliminar_agendamento(id_agendamento):
    carregar_agendamentos()

    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    agendamento_removido = agendamentos[id_agendamento]
    del agendamentos[id_agendamento]
    guardar_agendamentos()

    return 200, agendamento_removido
