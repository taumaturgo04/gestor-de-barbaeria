import json
import os

from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_barbearia


FICHEIRO_BARBEARIAS = "barbearias.json"

# dicionario em memória para guardar as barbearias
barbearias = {}


# ==========================
# Persistência
# ==========================
def guardar_barbearias():
    with open(FICHEIRO_BARBEARIAS, "w", encoding="utf-8") as ficheiro:
        json.dump(barbearias, ficheiro, indent=4, ensure_ascii=False)


def carregar_barbearias():
    global barbearias

    if os.path.exists(FICHEIRO_BARBEARIAS):
        with open(FICHEIRO_BARBEARIAS, "r", encoding="utf-8") as ficheiro:
            barbearias = json.load(ficheiro)
    else:
        barbearias = {}


# ==========================
# CREATE
# ==========================
def criar_barbearia(nome, morada, nif):
    carregar_barbearias()

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
    guardar_barbearias()

    return 201, barbearia


# ==========================
# READ ALL
# ==========================
def listar_barbearias():
    carregar_barbearias()

    if not barbearias:
        return 404, "Nao existem barbearias registadas."

    return 200, barbearias


# ==========================
# READ ONE
# ==========================
def consultar_barbearia(id_barbearia):
    carregar_barbearias()

    # verifica se o ID pedido existe antes de mostrar
    if id_barbearia not in barbearias:
        return 404, "Barbearia nao encontrada."

    return 200, barbearias[id_barbearia]


# ==========================
# UPDATE
# ==========================
def atualizar_barbearia(id_barbearia, nome=None, morada=None, nif=None):
    carregar_barbearias()

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

    guardar_barbearias()

    return 200, barbearias[id_barbearia]


# ==========================
# DELETE
# ==========================
def remover_barbearia(id_barbearia):
    carregar_barbearias()

    if id_barbearia not in barbearias:
        return 404, "Barbearia nao encontrada."

    # apaga o registo da barbearia do dicionario
    barbearia_removida = barbearias[id_barbearia]
    del barbearias[id_barbearia]
    guardar_barbearias()

    return 200, barbearia_removida
