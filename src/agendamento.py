import json
import os
import logging
from barbeiro import consultar_barbeiro
from cliente import consultar_cliente
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora

FICHEIRO_AGENDAMENTOS = "agendamentos.json"
agendamentos = {}

logger = get_logger(__name__)

# ==========================
# Persistência
# ==========================
def guardar_agendamentos():
    try:
        with open(FICHEIRO_AGENDAMENTOS, "w", encoding="utf-8") as ficheiro:
            json.dump(agendamentos, ficheiro, indent=4, ensure_ascii=False)
        logger.info("Agendamentos guardados com sucesso. Total: %d", len(agendamentos))
    except Exception as e:
        logger.error("Erro ao guardar agendamentos: %s", str(e))
        raise


def carregar_agendamentos():
    global agendamentos
    try:
        if os.path.exists(FICHEIRO_AGENDAMENTOS):
            with open(FICHEIRO_AGENDAMENTOS, "r", encoding="utf-8") as ficheiro:
                agendamentos = json.load(ficheiro)
            logger.info("Agendamentos carregados. Total: %d", len(agendamentos))
        else:
            agendamentos = {}
            logger.info("Ficheiro de agendamentos não existe. Iniciado novo dicionário.")
    except Exception as e:
        logger.error("Erro ao carregar agendamentos: %s", str(e))
        agendamentos = {}


# ==========================
# CREATE
# ==========================
def criar_agendamento(data_hora, id_cliente, id_barbeiro, servico, id_barbearia):
    logger.info("Criando agendamento - Cliente: %s | Barbeiro: %s | Data: %s", 
                id_cliente, id_barbeiro, data_hora)
    
    carregar_agendamentos()
    
    if campo_vazio(data_hora) or campo_vazio(id_cliente) or campo_vazio(id_barbeiro) or campo_vazio(servico) or campo_vazio(id_barbearia):
        logger.warning("Tentativa de criar agendamento com campos vazios")
        return 401, "Nao pode deixar campos vazios."
    
    if not validar_data_hora(data_hora):
        logger.warning("Data/hora inválida: %s", data_hora)
        return 500, "Data e hora invalidas. Utilize formato YYYY-MM-DD HH:MM"
    
    codigo_cliente, cliente = consultar_cliente(id_cliente)
    if codigo_cliente != 200:
        logger.warning("Cliente não encontrado: %s", id_cliente)
        return 404, "Cliente nao encontrado."
    
    codigo_barbeiro, barbeiro = consultar_barbeiro(id_barbeiro)
    if codigo_barbeiro != 200:
        logger.warning("Barbeiro não encontrado: %s", id_barbeiro)
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
    
    logger.info("Agendamento criado com sucesso! ID: %s", id_agendamento)
    return 201, agendamento


# ==========================
# READ ALL
# ==========================
def listar_agendamentos():
    carregar_agendamentos()
    logger.info("Listagem de agendamentos solicitada. Total: %d", len(agendamentos))
    
    if not agendamentos:
        logger.info("Nenhum agendamento encontrado")
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
# UPDATE
# ==========================
def atualizar_status(id_agendamento, novo_status):
    logger.info("Atualizando status do agendamento %s para: %s", id_agendamento, novo_status)
    
    carregar_agendamentos()
    
    if id_agendamento not in agendamentos:
        logger.warning("Agendamento não encontrado para atualização: %s", id_agendamento)
        return 404, "Agendamento nao encontrado."
    
    if campo_vazio(novo_status):
        logger.warning("Tentativa de atualizar com status vazio")
        return 401, "Nao pode deixar campos vazios."
    
    agendamentos[id_agendamento]["status"] = novo_status.strip()
    guardar_agendamentos()
    
    logger.info("Status atualizado com sucesso para agendamento %s", id_agendamento)
    return 200, agendamentos[id_agendamento]


# ==========================
# DELETE
# ==========================
def eliminar_agendamento(id_agendamento):
    logger.info("Tentativa de eliminar agendamento: %s", id_agendamento)
    
    carregar_agendamentos()
    
    if id_agendamento not in agendamentos:
        logger.warning("Agendamento não encontrado para eliminação: %s", id_agendamento)
        return 404, "Agendamento nao encontrado."
    
    agendamento_removido = agendamentos[id_agendamento]
    del agendamentos[id_agendamento]
    guardar_agendamentos()
    
    logger.info("Agendamento eliminado com sucesso: %s", id_agendamento)
    return 200, agendamento_removido

