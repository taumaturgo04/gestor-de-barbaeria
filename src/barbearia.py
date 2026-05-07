from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_barbearia


# dicionario em memória para guardar as barbearias
barbearias = {}


def criar_barbearia(nome, morada, nif):
    # valida se os campos obrigatorios foram preenchidos
    if campo_vazio(nome) or campo_vazio(morada) or campo_vazio(nif):
        return 401, "Nao pode deixar campos vazios."

    if not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."

    # gera um ID sequencial no formato BR001, BR002, ...
    id_barbearia = gerar_id_barbearia()
    barbearia = {
        "nome": nome.strip(),
        "morada": morada.strip(),
        "nif": nif.strip(),
    }
    barbearias[id_barbearia] = barbearia

    return 201, barbearia


def listar_barbearias():
    if not barbearias:
        return 404, "Nao existem barbearias registadas."

    return 200, barbearias


def consultar_barbearia(id_barbearia):
    # verifica se o ID pedido existe antes de mostrar
    if id_barbearia not in barbearias:
        return 404, "Barbearia nao encontrada."

    return 200, barbearias[id_barbearia]


def atualizar_barbearia(id_barbearia, nome=None, morada=None, nif=None):
    if id_barbearia not in barbearias:
        return 404, "Barbearia nao encontrada."

    # se o utilizador escrever apenas espaços, devolve erro
    if (
        (nome is not None and campo_vazio(nome))
        or (morada is not None and campo_vazio(morada))
        or (nif is not None and campo_vazio(nif))
    ):
        return 401, "Nao pode deixar campos vazios."

    if nome is not None and not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    if morada is not None and not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."

    if nif is not None and not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."

    # so atualiza os campos que o utilizador preencher
    if nome:
        barbearias[id_barbearia]["nome"] = nome.strip()
    if morada:
        barbearias[id_barbearia]["morada"] = morada.strip()
    if nif:
        barbearias[id_barbearia]["nif"] = nif.strip()

    return 200, barbearias[id_barbearia]


def remover_barbearia(id_barbearia):
    if id_barbearia not in barbearias:
        return 404, "Barbearia nao encontrada."

    # apaga o registo da barbearia do dicionario
    barbearia_removida = barbearias[id_barbearia]
    del barbearias[id_barbearia]
    return 200, barbearia_removida