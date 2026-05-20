import json
import os
import logging
from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_barbeiro
from barbearia import consultar_barbearia  # Caso queiras validar a barbearia

FICHEIRO_BARBEIROS = "barbeiros.json"
barbeiros = {}

# ==========================
# Configuração do Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("barbeiros.log", encoding="utf-8"),
        logging.StreamHandler()  # Mostra no console/terminal
    ]
)

logger = logging.getLogger(__name__)

# ==========================
# Persistência
# ==========================
def guardar_barbeiros():
    try:
        with open(FICHEIRO_BARBEIROS, "w", encoding="utf-8") as ficheiro:
            json.dump(barbeiros, ficheiro, indent=4, ensure_ascii=False)
        logger.info("Barbeiros guardados com sucesso. Total: %d", len(barbeiros))
    except Exception as e:
        logger.error("Erro ao guardar barbeiros: %s", str(e))
        raise


def carregar_barbeiros():
    global barbeiros
    try:
        if os.path.exists(FICHEIRO_BARBEIROS):
            with open(FICHEIRO_BARBEIROS, "r", encoding="utf-8") as ficheiro:
                barbeiros = json.load(ficheiro)
            logger.info("Barbeiros carregados com sucesso. Total: %d", len(barbeiros))
        else:
            barbeiros = {}
            logger.info("Ficheiro de barbeiros não existe. Novo dicionário criado.")
    except Exception as e:
        logger.error("Erro ao carregar barbeiros: %s", str(e))
        barbeiros = {}


# ==========================
# CREATE
# ==========================
def criar_barbeiro(nome, especialidade, telefone, nif, iban, morada, email, id_barbearia):
    logger.info("Tentativa de criar barbeiro: %s | Barbearia: %s", nome, id_barbearia)
    
    carregar_barbeiros()
    
    if (campo_vazio(nome) or campo_vazio(especialidade) or campo_vazio(telefone) or 
        campo_vazio(nif) or campo_vazio(iban) or campo_vazio(morada) or 
        campo_vazio(email) or campo_vazio(id_barbearia)):
        logger.warning("Tentativa de criar barbeiro com campos vazios")
        return 401, "Não pode deixar campos vazios."
    
    if not campo_apenas_letras(nome):
        logger.warning("Nome inválido: %s", nome)
        return 401, "O nome deve conter apenas letras."
    
    if not campo_apenas_letras(especialidade):
        logger.warning("Especialidade inválida")
        return 401, "A especialidade deve conter apenas letras."
    
    if not campo_apenas_letras(morada):
        logger.warning("Morada inválida")
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
    
    # Opcional: Validar se a barbearia existe
    # codigo, _ = consultar_barbearia(id_barbearia)
    # if codigo != 200:
    #     logger.warning("Barbearia não encontrada: %s", id_barbearia)
    #     return 404, "Barbearia nao encontrada."
    
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
    guardar_barbeiros()
    
    logger.info("Barbeiro criado com sucesso! ID: %s - Nome: %s", id_barbeiro, nome)
    return 201, barbeiro


# ==========================
# READ ALL
# ==========================
def listar_barbeiros():
    carregar_barbeiros()
    logger.info("Listagem de barbeiros solicitada. Total: %d", len(barbeiros))
    
    if not barbeiros:
        logger.info("Nenhum barbeiro encontrado")
        return 404, "Não existem barbeiros registados."
    
    return 200, barbeiros


# ==========================
# READ ONE
# ==========================
def consultar_barbeiro(id_barbeiro):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        logger.warning("Barbeiro não encontrado: %s", id_barbeiro)
        return 404, "Barbeiro não encontrado."
    
    logger.info("Barbeiro consultado: %s", id_barbeiro)
    return 200, barbeiros[id_barbeiro]


# ==========================
# UPDATE
# ==========================
def atualizar_barbeiro(id_barbeiro, nome=None, especialidade=None, telefone=None, nif=None, 
                       iban=None, morada=None, email=None, id_barbearia=None):
    logger.info("Tentativa de atualizar barbeiro: %s", id
