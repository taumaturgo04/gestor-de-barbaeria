from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_barbeiro


# dicionario em mémoria para guardar os barbeiros
barbeiros = {}

def criar_barbeiro(nome, especialidade, telefone, nif, iban, morada, email, id_barbearia):
    # valida se os campos obrigatorios foram preenchidos
    if (
        campo_vazio(nome)
        or campo_vazio(especialidade)
        or campo_vazio(telefone)
        or campo_vazio(nif)
        or campo_vazio(iban)
        or campo_vazio(morada)
        or campo_vazio(email)
        or campo_vazio(id_barbearia)
    ):
        return 401, "Não pode deixar campos vazios."

    if not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if not campo_apenas_letras(especialidade):
        return 401, "A especialidade deve conter apenas letras."
    if not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas números."
    if not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    if not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."

    # gera um ID sequencial no formato B001, B002, ...
    id_barbeiro = gerar_id_barbeiro()
    barbeiro = {
        "nome": nome.strip(),
        "especialidade": especialidade.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
        "id_barbearia": id_barbearia.strip(),
    }
    barbeiros[id_barbeiro] = barbeiro

    return 201, barbeiro

def listar_barbeiros():
    if not barbeiros:
        return 404, "Não existem barbeiros registados."

    return 200, barbeiros

def consultar_barbeiro(id_barbeiro):
    # verifica se o ID pedido existe antes de mostrar
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro nao encontrado."

    return 200, barbeiros[id_barbeiro]

def atualizar_barbeiro(id_barbeiro, nome=None, especialidade=None, telefone=None, nif=None, iban=None, morada=None, email=None, id_barbearia=None):
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro nao encontrado."

    # se o utilizador escrever apenas espaços, devolve erro
    if (
        (nome is not None and campo_vazio(nome))
        or (especialidade is not None and campo_vazio(especialidade))
        or (telefone is not None and campo_vazio(telefone))
        or (nif is not None and campo_vazio(nif))
        or (iban is not None and campo_vazio(iban))
        or (morada is not None and campo_vazio(morada))
        or (email is not None and campo_vazio(email))
        or (id_barbearia is not None and campo_vazio(id_barbearia))
    ):
        return 401, "Não pode deixar campos vazios."

    if nome is not None and not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if especialidade is not None and not campo_apenas_letras(especialidade):
        return 401, "A especialidade deve conter apenas letras."
    if morada is not None and not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if telefone is not None and not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas números."
    if nif is not None and not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    if iban is not None and not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."

    # so atualiza os campos que o utilizador preencher
    if nome:
        barbeiros[id_barbeiro]["nome"] = nome.strip()
    if especialidade:
        barbeiros[id_barbeiro]["especialidade"] = especialidade.strip()
    if telefone:
        barbeiros[id_barbeiro]["telefone"] = telefone.strip()
    if nif:
        barbeiros[id_barbeiro]["nif"] = nif.strip()
    if iban:
        barbeiros[id_barbeiro]["iban"] = iban.strip()
    if morada:
        barbeiros[id_barbeiro]["morada"] = morada.strip()
    if email:
        barbeiros[id_barbeiro]["email"] = email.strip()
    if id_barbearia:
        barbeiros[id_barbeiro]["id_barbearia"] = id_barbearia.strip()

    return 200, barbeiros[id_barbeiro]

def remover_barbeiro(id_barbeiro):
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."

    # apaga o registo do barbeiro do dicionario
    barbeiro_removido = barbeiros[id_barbeiro]
    del barbeiros[id_barbeiro]
    return 200, barbeiro_removido
