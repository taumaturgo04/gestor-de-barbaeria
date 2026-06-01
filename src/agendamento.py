import json
import os
import logging
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora
from cliente import consultar_cliente
from barbeiro import consultar_barbeiro

FICHEIRO_AGENDAMENTOS = "agendamentos.json"
agendamentos = {}

logger = logging.getLogger(__name__)

def guardar_agendamentos():
    try:
        with open(FICHEIRO_AGENDAMENTOS, "w", encoding="utf-8") as f:
            json.dump(agendamentos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Erro ao guardar agendamentos: %s", str(e))

def carregar_agendamentos():
    global agendamentos
    if os.path.exists(FICHEIRO_AGENDAMENTOS):
        try:
            with open(FICHEIRO_AGENDAMENTOS, "r", encoding="utf-8") as f:
                agendamentos = json.load(f)
        except Exception:
            agendamentos = {}

def criar_agendamento(data_hora, id_cliente, id_barbeiro, servico, id_barbearia):
    carregar_agendamentos()
    if not validar_data_hora(data_hora):
        return 401, "Formato de data inválido. Use YYYY-MM-DD HH:MM"
    if campo_vazio(id_cliente) or campo_vazio(id_barbeiro) or campo_vazio(id_barbearia):
        return 401, "ID Cliente, ID Barbeiro e ID Barbearia são obrigatórios."

    code_c, res_c = consultar_cliente(id_cliente)
    nome_cliente = res_c.get("nome", "Desconhecido") if code_c == 200 else "Desconhecido"

    code_b, res_b = consultar_barbeiro(id_barbeiro)
    nome_barbeiro = res_b.get("nome", "Desconhecido") if code_b == 200 else "Desconhecido"

    id_a = gerar_id_agendamento()
    agendamentos[id_a] = {
        "data_hora": data_hora.strip(),
        "id_cliente": id_cliente.strip(),
        "cliente": nome_cliente,
        "id_barbeiro": id_barbeiro.strip(),
        "barbeiro": nome_barbeiro,
        "servico": servico.strip(),
        "id_barbearia": id_barbearia.strip(),
        "status": "Pendente"
    }
    guardar_agendamentos()
    return 201, agendamentos[id_a]

def listar_agendamentos():
    carregar_agendamentos()
    return 200, agendamentos

def atualizar_status(id_agendamento, novo_status):
    carregar_agendamentos()
    if id_agendamento not in agendamentos:
        return 404, "Agendamento não encontrado."
    if campo_vazio(novo_status):
        return 401, "O status não pode estar vazio."

    agendamentos[id_agendamento]["status"] = novo_status.strip()
    guardar_agendamentos()
    return 200, agendamentos[id_agendamento]

def eliminar_agendamento(id_agendamento):
    carregar_agendamentos()
    if id_agendamento not in agendamentos:
        return 404, "Agendamento não encontrado."
    removido = agendamentos.pop(id_agendamento)
    guardar_agendamentos()
    return 200, removido