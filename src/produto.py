from utils import (
    campo_apenas_letras,
    campo_decimal_positivo,
    campo_inteiro_positivo,
    campo_vazio,
    gerar_id_produto,
)
from barbearia import consultar_barbearia


produtos = {}


def adicionar_produto(nome, preco, qtd, id_barbearia):
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
    return 201, produto


def listar_produtos():
    if not produtos:
        return 404, "Nao existem produtos registados."

    return 200, produtos


def consultar_produto(id_produto):
    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    return 200, produtos[id_produto]


def atualizar_produto(id_produto, nome=None, preco=None, qtd=None, id_barbearia=None):
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


def remover_produto(id_produto):
    if id_produto not in produtos:
        return 404, "Produto nao encontrado."

    produto_removido = produtos[id_produto]
    del produtos[id_produto]
    return 200, produto_removido
