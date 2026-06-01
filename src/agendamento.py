import json
import os
import logging
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora
from cliente import consultar_cliente, adicionar_ao_historico
from barbeiro import consultar_barbeiro

FICHEIRO_AGENDAMENTOS = "agendamentos.json"
agendamentos = {}

def carregar_agendamentos():
    global agendamentos
    if os.path.exists(FICHEIRO_AGENDAMENTOS):
        try:
            with open(FICHEIRO_AGENDAMENTOS, "r", encoding="utf-8") as f:
                agendamentos = json.load(f)
        except Exception:
            agendamentos = {}

def guardar_agendamentos():
    with open(FICHEIRO_AGENDAMENTOS, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=4, ensure_ascii=False)

def criar_agendamento(data_hora, id_cliente, id_barbeiro, servico, id_barbearia="BR001"):
    carregar_agendamentos()
    if not validar_data_hora(data_hora):
        return 400, "Formato de Data/Hora inválido. Use YYYY-MM-DD HH:MM"
    
    c_code, c_info = consultar_cliente(id_cliente)
    if c_code != 200:
        return 404, f"Erro Cliente: {c_info}"
        
    b_code, b_info = consultar_barbeiro(id_barbeiro)
    if b_code != 200:
        return 404, f"Erro Barbeiro: {b_info}"

    id_a = gerar_id_agendamento()
    agendamentos[id_a] = {
        "data_hora": data_hora.strip(),
        "id_cliente": id_cliente.strip(),
        "cliente": c_info.get("nome"),
        "id_barbeiro": id_barbeiro.strip(),
        "barbeiro": b_info.get("nome"),
        "servico": servico.strip(),
        "id_barbearia": id_barbearia.strip() if id_barbearia else "BR001",
        "status": "Pendente"
    }
    guardar_agendamentos()
    
    # Adiciona a referência do agendamento à lista histórica do Cliente
    adicionar_ao_historico(id_cliente, id_a)
    
    return 201, id_a

def listar_agendamentos():
    carregar_agendamentos()
    return 200, agendamentos

def atualizar_status(id_agendamento, novo_status):
    carregar_agendamentos()
    if id_agendamento not in agendamentos:
        return 404, "Agendamento não encontrado."
    agendamentos[id_agendamento]["status"] = novo_status.strip()
    guardar_agendamentos()
    return 200, "Status modificado."

def eliminar_agendamento(id_agendamento):
    carregar_agendamentos()
    if id_agendamento not in agendamentos:
        return 404, "Agendamento não localizado."
    del agendamentos[id_agendamento]
    guardar_agendamentos()
    return 200, "Agendamento eliminado."
