import json
import os
import logging
from utils import campo_vazio, campo_decimal_positivo, campo_inteiro_positivo, gerar_id_produto

FICHEIRO_PRODUTOS = "produtos.json"
produtos = {}

logger = logging.getLogger(__name__)

def guardar_produtos():
    try:
        with open(FICHEIRO_PRODUTOS, "w", encoding="utf-8") as f:
            json.dump(produtos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Erro ao guardar produtos: %s", str(e))

def carregar_produtos():
    global produtos
    if os.path.exists(FICHEIRO_PRODUTOS):
        try:
            with open(FICHEIRO_PRODUTOS, "r", encoding="utf-8") as f:
                produtos = json.load(f)
        except Exception:
            produtos = {}

def adicionar_produto(nome, preco, stock):
    carregar_produtos()
    if campo_vazio(nome) or campo_vazio(preco) or campo_vazio(stock):
        return 401, "Não pode deixar campos vazios."
    if not campo_decimal_positivo(preco):
        return 401, "O preço deve ser um número decimal positivo."
    if not campo_inteiro_positivo(stock):
        return 401, "O stock deve ser um número inteiro positivo."

    id_prod = gerar_id_produto()
    produtos[id_prod] = {
        "nome": nome.strip(),
        "preco": float(str(preco).strip()),
        "stock": int(str(stock).strip())
    }
    guardar_produtos()
    return 201, produtos[id_prod]

def listar_produtos():
    carregar_produtos()
    return 200, produtos

def remover_produto(id_produto):
    carregar_produtos()
    if id_produto not in produtos:
        return 404, "Produto não encontrado."
    removido = produtos.pop(id_produto)
    guardar_produtos()
    return 200, removido
