import json
import os
import logging
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
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("produtos.log", encoding="utf-8"),
        logging.StreamHandler()  # Mostra também no console
    ]
)

logger = logging.getLogger(__name__)

# ==========================
# Persistência
# ==========================
def guardar_produtos():
    try:
        with open(FICHEIRO_PRODUTOS, "w", encoding="utf-8") as ficheiro:
            json.dump(produtos, ficheiro, indent=4, ensure_ascii=False)
        logger.info("Produtos guardados com sucesso. Total: %d", len(produtos))
    except Exception as e:
        logger.error("Erro ao guardar produtos: %s", str(e))
        raise


def carregar_produtos():
    global produtos
    try:
        if os.path.exists(FICHEIRO_PRODUTOS):
            with open(FICHEIRO_PRODUTOS, "r", encoding="utf-8") as ficheiro:
                produtos = json.load(ficheiro)
            logger.info("Produtos carregados com sucesso. Total: %d", len(produtos))
        else:
            produtos = {}
            logger.info("Ficheiro de produtos não existe. Novo dicionário criado.")
    except Exception as e:
        logger.error("Erro ao carregar produtos: %s", str(e))
        produtos = {}


# ==========================
# CREATE
# ==========================
def adicionar_produto(nome, preco, qtd, id_barbearia):
    logger.info("Tentativa de adicionar produto: %s | Barbearia: %s", nome, id_barbearia)
    
    carregar_produtos()
    
    if campo_vazio(nome) or campo_vazio(preco) or campo_vazio(qtd) or campo_vazio(id_barbearia):
        logger.warning("Tentativa de adicionar produto com campos vazios")
        return 401, "Nao pode deixar campos vazios."
    
    if not campo_apenas_letras(nome):
        logger.warning("Nome inválido (deve conter apenas letras): %s", nome)
        return 401, "O nome deve conter apenas letras."
    
    if not campo_decimal_positivo(preco):
        logger.warning("Preço inválido: %s", preco)
        return 401, "O preco deve ser um numero maior que zero."
    
    if not campo_inteiro_positivo(qtd):
        logger.warning("Quantidade inválida: %s", qtd)
        return 401, "A quantidade deve ser um numero inteiro maior que zero."
    
    # Valida se a barbearia existe
    codigo_barbearia, barbearia = consultar_barbearia(id_barbearia.strip())
    if codigo_barbearia != 200:
        logger.warning("Barbearia não encontrada: %s", id_barbearia)
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
    
    logger.info("Produto adicionado com sucesso! ID: %s - Nome: %s", id_produto, nome)
    return 201, produto


# ==========================
# READ ALL
# ==========================
def listar_produtos():
    carregar_produtos()
    logger.info("Listagem de produtos solicitada. Total: %d", len(produtos))
    
    if not produtos:
        logger.info("Nenhum produto registado")
        return 404, "Nao existem produtos registados."
    
    return 200, produtos


# ==========================
# READ ONE
# ==========================
def consultar_produto(id_produto):
    carregar_produtos()
    if id_produto not in produtos:
        logger.warning("Produto não encontrado: %s", id_produto)
        return 404, "Produto nao encontrado."
    
    logger.info("Produto consultado: %s", id_produto)
    return 200, produtos[id_produto]


# ==========================
# UPDATE
# ==========================
def atualizar_produto(id_produto, nome=None, preco=None, qtd=None, id_barbearia=None):
    logger.info("Tentativa de atualizar produto: %s", id_produto)
    
    carregar_produtos()
    
    if id_produto not in produtos:
        logger.warning("Produto não encontrado para atualização: %s", id_produto)
        return 404, "Produto nao encontrado."
    
    if (
        (nome is not None and campo_vazio(nome))
        or (preco is not None and campo_vazio(preco))
        or (qtd is not None and campo_vazio(qtd))
        or (id_barbearia is not None and campo_vazio(id_barbearia))
    ):
        logger.warning("Tentativa de atualizar produto com campos vazios")
        return 401, "Nao pode deixar campos vazios."
    
    if nome is not None and not campo_apenas_letras(nome):
        logger.warning("Nome inválido na atualização")
        return 401, "O nome deve conter apenas letras."
    
    if preco is not None and not campo_decimal_positivo(preco):
        logger.warning("Preço inválido na atualização: %s", preco)
        return 401, "O preco deve ser um numero maior que zero."
    
    if qtd is not None and not campo_inteiro_positivo(qtd):
        logger.warning("Quantidade inválida na atualização: %s", qtd)
        return 401, "A quantidade deve ser um numero inteiro maior que zero."
    
    # Atualiza apenas os campos enviados
    if nome:
        produtos[id_produto]["nome"] = nome.strip()
    if preco:
        produtos[id_produto]["preco_venda"] = float(str(preco).strip())
    if qtd:
        produtos[id_produto]["quantidade_stock"] = int(str(qtd).strip())
    if id_barbearia:
        produtos[id_produto]["id_barbearia"] = id_barbearia.strip()
    
    guardar_produtos()
    
    logger.info("Produto atualizado com sucesso: %s", id_produto)
    return 200, produtos[id_produto]


# ==========================
# DELETE
# ==========================
def remover_produto(id_produto):
    logger.info("Tentativa de remover produto: %s", id_produto)
    
    carregar_produtos()
    
    if id_produto not in produtos:
        logger.warning("Produto não encontrado para remoção: %s", id_produto)
        return 404, "Produto nao encontrado."
    
    produto_removido = produtos[id_produto]
    del produtos[id_produto]
    guardar_produtos()
    
    logger.info("Produto removido com sucesso: %s - %s", id_produto, produto_removido.get("nome"))
    return 200, produto_removido

