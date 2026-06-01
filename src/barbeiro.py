import json
import os
import logging
from utils import campo_vazio, gerar_id_barbeiro

FICHEIRO_BARBEIROS = "barbeiros.json"
barbeiros = {}

logger = logging.getLogger("barbeiro")

def carregar_barbeiros():
    global barbeiros
    if os.path.exists(FICHEIRO_BARBEIROS):
        try:
            with open(FICHEIRO_BARBEIROS, "r", encoding="utf-8") as f:
                barbeiros = json.load(f)
        except Exception:
            barbeiros = {}

def guardar_barbeiros():
    with open(FICHEIRO_BARBEIROS, "w", encoding="utf-8") as f:
        json.dump(barbeiros, f, indent=4, ensure_ascii=False)

def criar_barbeiro(nome, especialidades, horarios_trabalho, iban, telefone, email, categoria_profissional, id_barbearia="BR001", nif=""):
    carregar_barbeiros()
    if campo_vazio(nome) or campo_vazio(telefone) or campo_vazio(categoria_profissional):
        return 400, "Nome, Telemóvel e Categoria Profissional são obrigatórios."
    
    id_b = gerar_id_barbeiro()
    barbeiros[id_b] = {
        "nome": nome.strip(),
        "especialidades": especialidades.strip() if especialidades else "Cortes Gerais",
        "horarios_trabalho": horarios_trabalho.strip() if horarios_trabalho else "09:00 - 19:00",
        "iban": iban.strip() if iban else "",
        "telefone": telefone.strip(),
        "email": email.strip() if email else "",
        "categoria_profissional": categoria_profissional.strip(),
        "id_barbearia": id_barbearia.strip() if id_barbearia else "BR001",
        "nif": nif.strip() if nif else ""
    }
    guardar_barbeiros()
    return 201, id_b

def listar_barbeiros():
    carregar_barbeiros()
    return 200, barbeiros

def consultar_barbeiro(id_barbeiro):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."
    return 200, barbeiros[id_barbeiro]

def atualizar_barbeiro(id_barbeiro, nome, especialidades, horarios_trabalho, iban, telefone, email, categoria_profissional, id_barbearia="BR001", nif=""):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não encontrado."
    if campo_vazio(nome) or campo_vazio(telefone):
        return 400, "Nome e Telemóvel não podem ficar vazios."
        
    barbeiros[id_barbeiro] = {
        "nome": nome.strip(),
        "especialidades": especialidades.strip(),
        "horarios_trabalho": horarios_trabalho.strip(),
        "iban": iban.strip(),
        "telefone": telefone.strip(),
        "email": email.strip(),
        "categoria_profissional": categoria_profissional.strip(),
        "id_barbearia": id_barbearia.strip() if id_barbearia else "BR001",
        "nif": nif.strip() if nif else barbeiros[id_barbeiro].get("nif", "")
    }
    guardar_barbeiros()
    return 200, "Barbeiro atualizado."

def remover_barbeiro(id_barbeiro):
    carregar_barbeiros()
    if id_barbeiro not in barbeiros:
        return 404, "Barbeiro não localizado."
    del barbeiros[id_barbeiro]
    guardar_barbeiros()
    return 200, "Barbeiro removido com sucesso."
