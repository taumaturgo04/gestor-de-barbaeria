import json
import os
import logging
from utils import campo_vazio, gerar_id_cliente

FICHEIRO_CLIENTES = "clientes.json"
clientes = {}

logger = logging.getLogger("cliente")

def carregar_clientes():
    global clientes
    if os.path.exists(FICHEIRO_CLIENTES):
        try:
            with open(FICHEIRO_CLIENTES, "r", encoding="utf-8") as f:
                clientes = json.load(f)
        except Exception:
            clientes = {}

def guardar_clientes():
    with open(FICHEIRO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

def criar_cliente(nome, telefone, email, nif, id_barbearia="BR001"):
    carregar_clientes()
    if campo_vazio(nome) or campo_vazio(telefone) or campo_vazio(nif):
        return 400, "Nome, Telefone (para SMS/WhatsApp) e NIF são obrigatórios."
    
    id_c = gerar_id_cliente()
    clientes[id_c] = {
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "email": email.strip() if email else "",
        "nif": nif.strip(),
        "id_barbearia": id_barbearia.strip() if id_barbearia else "BR001",
        "historico_servicos": []
    }
    guardar_clientes()
    return 201, id_c

def listar_clientes():
    carregar_clientes()
    return 200, clientes

def consultar_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    return 200, clientes[id_cliente]

def atualizar_cliente(id_cliente, nome, telefone, email, nif, id_barbearia="BR001"):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não localizado."
    if campo_vazio(nome) or campo_vazio(telefone) or campo_vazio(nif):
        return 400, "Os campos essenciais não podem ficar vazios."
    
    hist_preservado = clientes[id_cliente].get("historico_servicos", [])
    
    clientes[id_cliente] = {
        "nome": nome.strip(),
        "telefone": telefone.strip(),
        "email": email.strip() if email else "",
        "nif": nif.strip(),
        "id_barbearia": id_barbearia.strip() if id_barbearia else "BR001",
        "historico_servicos": hist_preservado
    }
    guardar_clientes()
    return 200, "Cliente atualizado."

def remover_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    del clientes[id_cliente]
    guardar_clientes()
    return 200, "Cliente removido do arquivo."

def adicionar_ao_historico(id_cliente, id_agendamento):
    carregar_clientes()
    if id_cliente in clientes:
        if "historico_servicos" not in clientes[id_cliente]:
            clientes[id_cliente]["historico_servicos"] = []
        if id_agendamento not in clientes[id_cliente]["historico_servicos"]:
            clientes[id_cliente]["historico_servicos"].append(id_agendamento)
            guardar_clientes()
