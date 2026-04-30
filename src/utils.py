from datetime import datetime


proximo_id_cliente = 1
proximo_id_barbeiro = 1
proximo_id_utilizador = 1
proximo_id_agendamento = 1
proximo_id_produto = 1
proximo_id_barbearia = 1


def campo_vazio(texto):
    return texto is None or texto.strip() == ""


def campo_numerico(texto):
    return texto is not None and texto.strip().isdigit()


def campo_apenas_letras(texto):
    valor = texto.strip()
    return valor != "" and all(caractere.isalpha() or caractere.isspace() for caractere in valor)


def campo_decimal_positivo(texto):
    try:
        return float(str(texto).strip()) > 0
    except (TypeError, ValueError):
        return False


def campo_inteiro_positivo(texto):
    try:
        return int(str(texto).strip()) > 0
    except (TypeError, ValueError):
        return False


def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def validar_data_hora(data_hora_texto):
    try:
        datetime.strptime(data_hora_texto, "%Y-%m-%d %H:%M")
        return True
    except (TypeError, ValueError):
        return False


def gerar_id_cliente():
    global proximo_id_cliente
    id_cliente = f"C{proximo_id_cliente:03d}"
    proximo_id_cliente += 1
    return id_cliente


def gerar_id_barbeiro():
    global proximo_id_barbeiro
    id_barbeiro = f"B{proximo_id_barbeiro:03d}"
    proximo_id_barbeiro += 1
    return id_barbeiro


def gerar_id_utilizador():
    global proximo_id_utilizador
    id_utilizador = f"U{proximo_id_utilizador:03d}"
    proximo_id_utilizador += 1
    return id_utilizador


def gerar_id_agendamento():
    global proximo_id_agendamento
    id_agendamento = f"A{proximo_id_agendamento:03d}"
    proximo_id_agendamento += 1
    return id_agendamento


def gerar_id_produto():
    global proximo_id_produto
    id_produto = f"P{proximo_id_produto:03d}"
    proximo_id_produto += 1
    return id_produto


def gerar_id_barbearia():
    global proximo_id_barbearia
    id_barbearia = f"BR{proximo_id_barbearia:03d}"
    proximo_id_barbearia += 1
    return id_barbearia