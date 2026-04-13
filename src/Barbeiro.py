# dicionario em memoria para guardar os barbeiros
barbeiros = {}
# contador simples para IDs automaticos
proximo_id_barbeiro = 1


def campo_vazio(texto):
    return texto is None or texto.strip() == ""


def criar_barbeiro(nome, especialidade, telefone, nif, iban, morada, email):
    global proximo_id_barbeiro

    # valida se os campos obrigatorios foram preenchidos
    if (
        campo_vazio(nome)
        or campo_vazio(especialidade)
        or campo_vazio(telefone)
        or campo_vazio(nif)
        or campo_vazio(iban)
        or campo_vazio(morada)
        or campo_vazio(email)
    ):
        return 401, "Nao pode deixar campos vazios."

    # gera um ID sequencial no formato B001, B002, ...
    id_barbeiro = f"B{proximo_id_barbeiro:03d}"
    barbeiros[id_barbeiro] = {
        "nome": nome.strip(),
        "especialidade": especialidade.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
    }
    proximo_id_barbeiro += 1

    return 201, f"Barbeiro criado com ID {id_barbeiro}"


def listar_barbeiros():
    if not barbeiros:
        return 404, "Nao existem barbeiros registados."

    # percorre todos os barbeiros guardados no dicionario
    for id_barbeiro, dados in barbeiros.items():
        print(
            f"ID: {id_barbeiro} | Nome: {dados['nome']} | "
            f"Especialidade: {dados['especialidade']} | Telefone: {dados['telefone']} | "
            f"NIF: {dados['nif']} | IBAN: {dados['iban']} | Morada: {dados['morada']} | "
            f"Email: {dados['email']}"
        )
    return 200, "Sucesso"


def consultar_barbeiro(id_barbeiro):
    # verifica se o ID pedido existe antes de mostrar
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro nao encontrado."

    dados = barbeiros[id_barbeiro]
    print(
        f"ID: {id_barbeiro} | Nome: {dados['nome']} | "
        f"Especialidade: {dados['especialidade']} | Telefone: {dados['telefone']} | "
        f"NIF: {dados['nif']} | IBAN: {dados['iban']} | Morada: {dados['morada']} | "
        f"Email: {dados['email']}"
    )
    return 200, "Sucesso"


def atualizar_barbeiro(id_barbeiro, nome=None, especialidade=None, telefone=None, nif=None, iban=None, morada=None, email=None):
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro nao encontrado."

    # se o utilizador escrever apenas espacos, devolve erro
    if (
        (nome is not None and campo_vazio(nome))
        or (especialidade is not None and campo_vazio(especialidade))
        or (telefone is not None and campo_vazio(telefone))
        or (nif is not None and campo_vazio(nif))
        or (iban is not None and campo_vazio(iban))
        or (morada is not None and campo_vazio(morada))
        or (email is not None and campo_vazio(email))
    ):
        return 401, "Nao pode deixar campos vazios."

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

    return 200, "Barbeiro atualizado com sucesso."


def remover_barbeiro(id_barbeiro):
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro nao encontrado."

    # apaga o registo do barbeiro do dicionario
    del barbeiros[id_barbeiro]
    return 200, "Barbeiro removido com sucesso."
