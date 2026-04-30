from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_cliente


# dicionario em mémoria para guardar os clientes
clientes = {}


def criar_cliente(nome, telefone, nif, iban, morada, email):
    # valida se os campos obrigatorios foram preenchidos
    if (
        campo_vazio(nome)
        or campo_vazio(telefone)
        or campo_vazio(nif)
        or campo_vazio(iban)
        or campo_vazio(morada)
        or campo_vazio(email)
    ):
        return 401, "Nao pode deixar campos vazios."

    if not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas números."
    if not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    if not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."

    # gera um ID sequencial no formato C001, C002, ...
    id_cliente = gerar_id_cliente()
    cliente = {
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
    }
    clientes[id_cliente] = cliente

    return 201, cliente


def listar_clientes():
    if not clientes:
        return 404, "Não existem clientes registados."

    return 200, clientes


def consultar_cliente(id_cliente):
    # verifica se o ID pedido existe antes de mostrar
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    return 200, clientes[id_cliente]


def atualizar_cliente(id_cliente, nome=None, telefone=None, nif=None, iban=None, morada=None, email=None):
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    # se o utilizador escrever apenas espaços, devolve erro
    if (
        (nome is not None and campo_vazio(nome))
        or (telefone is not None and campo_vazio(telefone))
        or (nif is not None and campo_vazio(nif))
        or (iban is not None and campo_vazio(iban))
        or (morada is not None and campo_vazio(morada))
        or (email is not None and campo_vazio(email))
    ):
        return 401, "Nao pode deixar campos vazios."

    if nome is not None and not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if morada is not None and not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if telefone is not None and not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas numeros."
    if nif is not None and not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    if iban is not None and not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."

    # so atualiza os campos que o utilizador preencher
    if nome:
        clientes[id_cliente]["nome"] = nome.strip()
    if telefone:
        clientes[id_cliente]["telefone"] = telefone.strip()
    if nif:
        clientes[id_cliente]["nif"] = nif.strip()
    if iban:
        clientes[id_cliente]["iban"] = iban.strip()
    if morada:
        clientes[id_cliente]["morada"] = morada.strip()
    if email:
        clientes[id_cliente]["email"] = email.strip()

    return 200, clientes[id_cliente]


def remover_cliente(id_cliente):
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    # apaga o registo do cliente do dicionario
    cliente_removido = clientes[id_cliente]
    del clientes[id_cliente]
    return 200, cliente_removido
