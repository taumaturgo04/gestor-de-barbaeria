import json
import os

from utils import (
    campo_apenas_letras,
    campo_decimal_positivo,
    campo_inteiro_positivo,
    campo_vazio,
    gerar_id_produto,
)
from barbearia import consultar_barbearia


FICHEIRO_PRODUTOS = "produtos.json"

produtos = {}


# ==========================
# Persistência
# ==========================
def guardar_produtos():
    with open(FICHEIRO_PRODUTOS, "w", encoding="utf-8") as ficheiro:
        json.dump(produtos, ficheiro, indent=4, ensure_ascii=False)


def carregar_produtos():
    global produtos

    if os.path.exists(FICHEIRO_PRODUTOS):
        with open(FICHEIRO_PRODUTOS, "r", encoding="utf-8") as ficheiro:
            produtos = json.load(ficheiro)
    else:
        produtos = {}


# ==========================
# CREATE
# ==========================
def adicionar_produto(nome, preco, qtd, id_barbearia):
    carregar_produtos()

    if campo_vazio(nome) or campo_vazio(preco) or campo_vazio(qtd) or campo_vazio(id_barbearia):
        return 401, "Nao pode deixar campos vazios."

    if not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."

    if not campo_decimal_positivo(preco):
        return 401, "O preco deve ser um numero maior que zero."

    if not campo_inteiro_positivo(qtd):
        return 401, "A quantidade deve ser um numero inteiro maior que zero."

    # valida se a barbearia existe
    codigo_barbearia, barbearia = consultar_barbearia(id_barbearia.strip())
    if codigo_barbearia != 200:
        return 404, "Barbearia nao encontrada."

    id_produto = gerar_id_produto()
    produto = {
        "nome": nome.strip(),
        "preco_venda": float(str(preco).strip()),
        "quantidade_stock": int(str(qtd).strip()),
        "id_barbearia": id_barbearia.strip(),
    }
    produtos[id_produto] = produto
    guardar_produtos()

    return 201, produto


# ==========================
# READ ALL
# ==========================
def listar_produtos():
    carregar_produtos()

    if not produtos:
        return 404, "Nao existem produtos registados."

    return 200, produtos


# ==========================
# READ ONE
# ==========================
def consultar_produto(id_produto):
    carregar_produtos()

    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    return 200, produtos[id_produto]


# ==========================
# UPDATE
# ==========================
def atualizar_produto(id_produto, nome=None, preco=None, qtd=None, id_barbearia=None):
    carregar_produtos()

    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    if (
        (nome is not None and campo_vazio(nome))
        or (preco is not None and campo_vazio(preco))
        or (qtd is not None and campo_vazio(qtd))
        or (id_barbearia is not None and campo_vazio(id_barbearia))
    ):
        return 401, "Nao pode deixar campos vazios."

    if nome is not None and not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."

    if preco is not None and not campo_decimal_positivo(preco):
        return 401, "O preco deve ser um numero maior que zero."

    if qtd is not None and not campo_inteiro_positivo(qtd):
        return 401, "A quantidade deve ser um numero inteiro maior que zero."

    # só atualiza os campos que o utilizador preencher
    if nome:
        produtos[id_produto]["nome"] = nome.strip()
    if preco:
        produtos[id_produto]["preco_venda"] = float(str(preco).strip())
    if qtd:
        produtos[id_produto]["quantidade_stock"] = int(str(qtd).strip())
    if id_barbearia:
        produtos[id_produto]["id_barbearia"] = id_barbearia.strip()

    guardar_produtos()

    return 200, produtos[id_produto]


# ==========================
# VENDER
# ==========================
def vender_produto(id_produto, quantidade):
    carregar_produtos()

    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    if campo_vazio(quantidade):
        return 401, "Quantidade nao pode estar vazia."

    if not campo_inteiro_positivo(quantidade):
        return 401, "A quantidade deve ser um numero inteiro maior que zero."

    qtd = int(str(quantidade).strip())

    if produtos[id_produto]["quantidade_stock"] < qtd:
        return 400, "Quantidade insuficiente em stock."

    produtos[id_produto]["quantidade_stock"] -= qtd
    guardar_produtos()

    return 200, produtos[id_produto]


# ==========================
# DELETE
# ==========================
def remover_produto(id_produto):
    carregar_produtos()

    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    produto_removido = produtos[id_produto]
    del produtos[id_produto]
    guardar_produtos()

    return 200, produto_removido
