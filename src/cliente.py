# dicionario em memoria para guardar os clientes
clientes = {}
# contador simples para IDs automaticos
proximo_id_cliente = 1


def campo_vazio(texto):
    return texto is None or texto.strip() == ""


def campo_numerico(texto):
    return texto is not None and texto.strip().isdigit()


def campo_apenas_letras(texto):
    valor = texto.strip()
    return valor != "" and all(caractere.isalpha() or caractere.isspace() for caractere in valor)


def criar_cliente(nome, telefone, nif, iban, morada, email):
    global proximo_id_cliente

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
        return 401, "O telefone deve conter apenas numeros."
    if not campo_numerico(nif):
        return 401, "O NIF deve conter apenas numeros."
    if not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas numeros."

    # gera um ID sequencial no formato C001, C002, ...
    id_cliente = f"C{proximo_id_cliente:03d}"
    clientes[id_cliente] = {
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
    }
    proximo_id_cliente += 1

    return 201, f"Cliente criado com ID {id_cliente}"


def listar_clientes():
    if not clientes:
        return 404, "Nao existem clientes registados."

    # percorre todos os clientes guardados no dicionario
    for id_cliente, dados in clientes.items():
        print(
            f"ID: {id_cliente} | Nome: {dados['nome']} | Telefone: {dados['telefone']} | "
            f"NIF: {dados['nif']} | IBAN: {dados['iban']} | Morada: {dados['morada']} | "
            f"Email: {dados['email']}"
        )
    return 200, "Sucesso"


def consultar_cliente(id_cliente):
    # verifica se o ID pedido existe antes de mostrar
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    dados = clientes[id_cliente]
    print(
        f"ID: {id_cliente} | Nome: {dados['nome']} | Telefone: {dados['telefone']} | "
        f"NIF: {dados['nif']} | IBAN: {dados['iban']} | Morada: {dados['morada']} | "
        f"Email: {dados['email']}"
    )
    return 200, "Sucesso"


def atualizar_cliente(id_cliente, nome=None, telefone=None, nif=None, iban=None, morada=None, email=None):
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    # se o utilizador escrever apenas espacos, devolve erro
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
        return 401, "O NIF deve conter apenas numeros."
    if iban is not None and not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas numeros."

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

    return 200, "Cliente atualizado com sucesso."


def remover_cliente(id_cliente):
    if id_cliente not in clientes:
        return 404, "Cliente nao encontrado."

    # apaga o registo do cliente do dicionario
    del clientes[id_cliente]
    return 200, "Cliente removido com sucesso."
