import json
import os
import logging
from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_cliente

FICHEIRO_CLIENTES = "clientes.json"
clientes = {}

# ==========================
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clientes.log", encoding="utf-8"),
        logging.StreamHandler()  # Mostra também no console
    ]
)

logger = logging.getLogger(__name__)

# ==========================
# Persistência
# ==========================
def guardar_clientes():
    try:
        with open(FICHEIRO_CLIENTES, "w", encoding="utf-8") as ficheiro:
            json.dump(clientes, ficheiro, indent=4, ensure_ascii=False)
        logger.info("Clientes guardados com sucesso. Total: %d", len(clientes))
    except Exception as e:
        logger.error("Erro ao guardar clientes: %s", str(e))
        raise


def carregar_clientes():
    global clientes
    try:
        if os.path.exists(FICHEIRO_CLIENTES):
            with open(FICHEIRO_CLIENTES, "r", encoding="utf-8") as ficheiro:
                clientes = json.load(ficheiro)
            logger.info("Clientes carregados com sucesso. Total: %d", len(clientes))
        else:
            clientes = {}
            logger.info("Ficheiro de clientes não existe. Novo dicionário criado.")
    except Exception as e:
        logger.error("Erro ao carregar clientes: %s", str(e))
        clientes = {}


# ==========================
# CREATE
# ==========================
def criar_cliente(id_barbearia, nome, telefone, nif, iban, morada, email):
    logger.info("Tentativa de criar cliente: %s | Barbearia: %s", nome, id_barbearia)
    
    carregar_clientes()
    
    if (campo_vazio(nome) or campo_vazio(telefone) or campo_vazio(nif) or 
        campo_vazio(iban) or campo_vazio(morada) or campo_vazio(email) or 
        campo_vazio(id_barbearia)):
        logger.warning("Tentativa de criar cliente com campos vazios")
        return 401, "Não pode deixar campos vazios."
    
    if not campo_apenas_letras(nome):
        logger.warning("Nome inválido (apenas letras): %s", nome)
        return 401, "O nome deve conter apenas letras."
    
    if not campo_apenas_letras(morada):
        logger.warning("Morada inválida (apenas letras)")
        return 401, "A morada deve conter apenas letras."
    
    if not campo_numerico(telefone):
        logger.warning("Telefone inválido: %s", telefone)
        return 401, "O telefone deve conter apenas números."
    
    if not campo_numerico(nif):
        logger.warning("NIF inválido: %s", nif)
        return 401, "O NIF deve conter apenas números."
    
    if not campo_numerico(iban):
        logger.warning("IBAN inválido: %s", iban)
        return 401, "O IBAN deve conter apenas números."
    
    id_cliente = gerar_id_cliente()
    
    cliente = {
        "id_barbearia": str(id_barbearia).strip(),
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "nif": nif.strip(),
        "iban": iban.strip(),
        "morada": morada.strip(),
        "email": email.strip(),
    }
    
    clientes[id_cliente] = cliente
    guardar_clientes()
    
    logger.info("Cliente criado com sucesso! ID: %s - Nome: %s", id_cliente, nome)
    return 201, {"id_cliente": id_cliente, **cliente}


# ==========================
# READ ALL
# ==========================
def listar_clientes(id_barbearia=None):
    carregar_clientes()
    
    if id_barbearia:
        logger.info("Listagem de clientes para a barbearia: %s", id_barbearia)
        clientes_filtrados = {
            cid: dados for cid, dados in clientes.items()
            if dados.get("id_barbearia") == str(id_barbearia).strip()
        }
        
        if not clientes_filtrados:
            logger.info("Nenhum cliente encontrado para a barbearia %s", id_barbearia)
            return 404, f"Não existem clientes registados para a barbearia {id_barbearia}."
        
        logger.info("%d clientes encontrados para a barbearia %s", len(clientes_filtrados), id_barbearia)
        return 200, clientes_filtrados
    else:
        logger.info("Listagem de todos os clientes solicitada. Total: %d", len(clientes))
        if not clientes:
            return 404, "Não existem clientes registados."
        return 200, clientes


# ==========================
# READ ONE
# ==========================
def consultar_cliente(id_cliente, id_barbearia=None):
    carregar_clientes()
    
    if id_cliente not in clientes:
        logger.warning("Cliente não encontrado: %s", id_cliente)
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        logger.warning("Acesso não autorizado ao cliente %s pela barbearia %s", id_cliente, id_barbearia)
        return 403, "Não tem permissão para acessar este cliente."
    
    logger.info("Cliente consultado: %s", id_cliente)
    return 200, {id_cliente: cliente}


# ==========================
# UPDATE
# ==========================
def atualizar_cliente(id_cliente, id_barbearia=None, nome=None, telefone=None, nif=None, 
                      iban=None, morada=None, email=None):
    logger.info("Tentativa de atualizar cliente: %s", id_cliente)
    
    carregar_clientes()
    
    if id_cliente not in clientes:
        logger.warning("Cliente não encontrado para atualização: %s", id_cliente)
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        logger.warning("Atualização não autorizada para cliente %s", id_cliente)
        return 403, "Não tem permissão para atualizar este cliente."
    
    if (
        (nome is not None and campo_vazio(nome))
        or (telefone is not None and campo_vazio(telefone))
        or (nif is not None and campo_vazio(nif))
        or (iban is not None and campo_vazio(iban))
        or (morada is not None and campo_vazio(morada))
        or (email is not None and campo_vazio(email))
    ):
        logger.warning("Tentativa de atualização com campos vazios")
        return 401, "Não pode deixar campos vazios."
    
    if nome is not None and not campo_apenas_letras(nome):
        logger.warning("Nome inválido na atualização")
        return 401, "O nome deve conter apenas letras."
    
    if morada is not None and not campo_apenas_letras(morada):
        logger.warning("Morada inválida na atualização")
        return 401, "A morada deve conter apenas letras."
    
    if telefone is not None and not campo_numerico(telefone):
        logger.warning("Telefone inválido na atualização")
        return 401, "O telefone deve conter apenas números."
    
    if nif is not None and not campo_numerico(nif):
        logger.warning("NIF inválido na atualização")
        return 401, "O NIF deve conter apenas números."
    
    if iban is not None and not campo_numerico(iban):
        logger.warning("IBAN inválido na atualização")
        return 401, "O IBAN deve conter apenas números."
    
    # Atualiza apenas os campos enviados
    if nome: clientes[id_cliente]["nome"] = nome.strip()
    if telefone: clientes[id_cliente]["telefone"] = telefone.strip()
    if nif: clientes[id_cliente]["nif"] = nif.strip()
    if iban: clientes[id_cliente]["iban"] = iban.strip()
    if morada: clientes[id_cliente]["morada"] = morada.strip()
    if email: clientes[id_cliente]["email"] = email.strip()
    
    guardar_clientes()
    
    logger.info("Cliente atualizado com sucesso: %s", id_cliente)
    return 200, {id_cliente: clientes[id_cliente]}


# ==========================
# DELETE
# ==========================
def remover_cliente(id_cliente, id_barbearia=None):
    logger.info("Tentativa de remover cliente: %s", id_cliente)
    
    carregar_clientes()
    
    if id_cliente not in clientes:
        logger.warning("Cliente não encontrado para remoção: %s", id_cliente)
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        logger.warning("Remoção não autorizada para cliente %s", id_cliente)
        return 403, "Não tem permissão para remover este cliente."
    
    cliente_removido = clientes.pop(id_cliente)
    guardar_clientes()
    
    logger.info("Cliente removido com sucesso: %s - %s", id_cliente, cliente_removido.get("nome"))
    return 200, {id_cliente: cliente_removido}
