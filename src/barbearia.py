import json
import os
import logging
from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_barbearia

FICHEIRO_BARBEARIAS = "barbearias.json"
barbearias = {}

# ==========================
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("barbearias.log", encoding="utf-8"),
        logging.StreamHandler()  # Mostra também no terminal/console
    ]
)

logger = logging.getLogger(__name__)

# ==========================
# Persistência
# ==========================
def guardar_barbearias():
    try:
        with open(FICHEIRO_BARBEARIAS, "w", encoding="utf-8") as ficheiro:
            json.dump(barbearias, ficheiro, indent=4, ensure_ascii=False)
        logger.info("Barbearias guardadas com sucesso. Total: %d", len(barbearias))
    except Exception as e:
        logger.error("Erro ao guardar barbearias: %s", str(e))
        raise


def carregar_barbearias():
    global barbearias
    try:
        if os.path.exists(FICHEIRO_BARBEARIAS):
            with open(FICHEIRO_BARBEARIAS, "r", encoding="utf-8") as ficheiro:
                barbearias = json.load(ficheiro)
            logger.info("Barbearias carregadas com sucesso. Total: %d", len(barbearias))
        else:
            barbearias = {}
            logger.info("Ficheiro de barbearias não existe. Criado novo dicionário.")
    except Exception as e:
        logger.error("Erro ao carregar barbearias: %s", str(e))
        barbearias = {}


# ==========================
# CREATE
# ==========================
def criar_barbearia(nome, morada, nif):
    logger.info("Tentativa de criar barbearia: %s", nome)
    
    carregar_barbearias()
    
    if campo_vazio(nome) or campo_vazio(morada) or campo_vazio(nif):
        logger.warning("Tentativa de criar barbearia com campos vazios")
        return 401, "Nao pode deixar campos vazios."
    
    if not campo_apenas_letras(nome):
        logger.warning("Nome inválido (deve conter apenas letras): %s", nome)
        return 401, "O nome deve conter apenas letras."
    
    if not campo_apenas_letras(morada):
        logger.warning("Morada inválida (deve conter apenas letras)")
        return 401, "A morada deve conter apenas letras."
    
    if not campo_numerico(nif):
        logger.warning("NIF inválido (deve conter apenas números): %s", nif)
        return 401, "O NIF deve conter apenas números."
    
    id_barbearia = gerar_id_barbearia()
    
    barbearia = {
        "nome": nome.strip(),
        "morada": morada.strip(),
        "nif": nif.strip(),
    }
    
    barbearias[id_barbearia] = barbearia
    guardar_barbearias()
    
    logger.info("Barbearia criada com sucesso! ID: %s - Nome: %s", id_barbearia, nome)
    return 201, barbearia


# ==========================
# READ ALL
# ==========================
def listar_barbearias():
    carregar_barbearias()
    logger.info("Listagem de barbearias solicitada. Total: %d", len(barbearias))
    
    if not barbearias:
        logger.info("Nenhuma barbearia encontrada")
        return 404, "Nao existem barbearias registadas."
    
    return 200, barbearias


# ==========================
# READ ONE
# ==========================
def consultar_barbearia(id_barbearia):
    carregar_barbearias()
    if id_barbearia not in barbearias:
        logger.warning("Barbearia não encontrada: %s", id_barbearia)
        return 404, "Barbearia nao encontrada."
    
    logger.info("Barbearia consultada: %s", id_barbearia)
    return 200, barbearias[id_barbearia]


# ==========================
# UPDATE
# ==========================
def atualizar_barbearia(id_barbearia, nome=None, morada=None, nif=None):
    logger.info("Tentativa de atualizar barbearia: %s", id_barbearia)
    
    carregar_barbearias()
    
    if id_barbearia not in barbearias:
        logger.warning("Barbearia não encontrada para atualização: %s", id_barbearia)
        return 404, "Barbearia nao encontrada."
    
    # Validação de campos vazios
    if (
        (nome is not None and campo_vazio(nome))
        or (morada is not None and campo_vazio(morada))
        or (nif is not None and campo_vazio(nif))
    ):
        logger.warning("Tentativa de atualizar com campos vazios")
        return 401, "Nao pode deixar campos vazios."
    
    if nome is not None and not campo_apenas_letras(nome):
        logger.warning("Nome inválido na atualização")
        return 401, "O nome deve conter apenas letras."
    
    if morada is not None and not campo_apenas_letras(morada):
        logger.warning("Morada inválida na atualização")
        return 401, "A morada deve conter apenas letras."
    
    if nif is not None and not campo_numerico(nif):
        logger.warning("NIF inválido na atualização: %s", nif)
        return 401, "O NIF deve conter apenas números."
    
    # Atualiza apenas os campos enviados
    if nome:
        barbearias[id_barbearia]["nome"] = nome.strip()
    if morada:
        barbearias[id_barbearia]["morada"] = morada.strip()
    if nif:
        barbearias[id_barbearia]["nif"] = nif.strip()
    
    guardar_barbearias()
    
    logger.info("Barbearia atualizada com sucesso: %s", id_barbearia)
    return 200, barbearias[id_barbearia]


# ==========================
# DELETE
# ==========================
def remover_barbearia(id_barbearia):
    logger.info("Tentativa de remover barbearia: %s", id_barbearia)
    
    carregar_barbearias()
    
    if id_barbearia not in barbearias:
        logger.warning("Barbearia não encontrada para remoção: %s", id_barbearia)
        return 404, "Barbearia nao encontrada."
    
    barbearia_removida = barbearias[id_barbearia]
    del barbearias[id_barbearia]
    guardar_barbearias()
    
    logger.info("Barbearia removida com sucesso: %s - %s", id_barbearia, barbearia_removida.get("nome"))
    return 200, barbearia_removida
