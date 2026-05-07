from barbeiro import consultar_barbeiro
from cliente import consultar_cliente
from utils import campo_vazio, gerar_id_agendamento, validar_data_hora


agendamentos = {}


def criar_agendamento(data_hora, id_cliente, id_barbeiro, servico, id_barbearia):
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

    return 201, agendamento


def listar_agendamentos():
    if not agendamentos:
        return 404, "Nao existem agendamentos registados."

    return 200, agendamentos


def consultar_agendamento(id_agendamento):
    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    return 200, agendamentos[id_agendamento]


def atualizar_status(id_agendamento, novo_status):
    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    if campo_vazio(novo_status):
        return 401, "Nao pode deixar campos vazios."

    agendamentos[id_agendamento]["status"] = novo_status.strip()
    return 200, agendamentos[id_agendamento]


def eliminar_agendamento(id_agendamento):
    if id_agendamento not in agendamentos:
        return 404, "Agendamento nao encontrado."

    agendamento_removido = agendamentos[id_agendamento]
    del agendamentos[id_agendamento]
    return 200, agendamento_removido
