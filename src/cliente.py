from utils import campo_apenas_letras, campo_numerico, campo_vazio, gerar_id_cliente

clientes = {}

def criar_cliente(id_barbearia, nome, telefone, nif, iban, morada, email):
    
    # valida se os campos obrigatorios foram preenchidos
    if (
        campo_vazio(nome)
        or campo_vazio(telefone)
        or campo_vazio(nif)
        or campo_vazio(iban)
        or campo_vazio(morada)
        or campo_vazio(email)
        or campo_vazio(id_barbearia)
    ):
        return 401, "Não pode deixar campos vazios."
    
    if not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    
    if not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."
    
    if not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas números."
    
    if not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    
    if not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."
    
    # gera um ID sequencial no formato C001, C002, ...
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
    return 201, {"id_cliente": id_cliente, **cliente}


def listar_clientes(id_barbearia=None):
    
    if not clientes:
        return 404, "Não existem clientes registados."
    
    # Se id_barbearia foi fornecido, filtra apenas os clientes dessa barbearia
    if id_barbearia:
        clientes_filtrados = {
            id_cliente: dados 
            for id_cliente, dados in clientes.items() 
            if dados.get("id_barbearia") == str(id_barbearia).strip()
        }
        
        if not clientes_filtrados:
            return 404, f"Não existem clientes registados para a barbearia {id_barbearia}."
        
        return 200, clientes_filtrados
    
    return 200, clientes


def consultar_cliente(id_cliente, id_barbearia=None):
  
    # verifica se o ID pedido existe antes de mostrar
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    # Se id_barbearia foi fornecido, valida se o cliente pertence a essa barbearia
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        return 403, "Não tem permissão para acessar este cliente."
    
    return 200, {id_cliente: cliente}


def atualizar_cliente(id_cliente, id_barbearia=None, nome=None, telefone=None, nif=None, iban=None, morada=None, email=None):
  
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    # Se id_barbearia foi fornecido, valida se o cliente pertence a essa barbearia
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        return 403, "Não tem permissão para atualizar este cliente."
    
    # se o utilizador escrever apenas espaços, devolve erro
    if (
        (nome is not None and campo_vazio(nome))
        or (telefone is not None and campo_vazio(telefone))
        or (nif is not None and campo_vazio(nif))
        or (iban is not None and campo_vazio(iban))
        or (morada is not None and campo_vazio(morada))
        or (email is not None and campo_vazio(email))
    ):
        return 401, "Não pode deixar campos vazios."
    
    if nome is not None and not campo_apenas_letras(nome):
        return 401, "O nome deve conter apenas letras."
    
    if morada is not None and not campo_apenas_letras(morada):
        return 401, "A morada deve conter apenas letras."
    
    if telefone is not None and not campo_numerico(telefone):
        return 401, "O telefone deve conter apenas números."
    
    if nif is not None and not campo_numerico(nif):
        return 401, "O NIF deve conter apenas números."
    
    if iban is not None and not campo_numerico(iban):
        return 401, "O IBAN deve conter apenas números."
    
    # só atualiza os campos que o utilizador preencher
    if nome:
        clientes[id_cliente]["nome"] = nome.strip()
    if telefone:
        clientes[id_cliente]["telefone"] = telefone.strip()
    if nif:
        clientes[id_cliente]["nif"] = nif.strip()
    if iban:
        clientes[id_cliente]["iban"] = iban.strip()
    if morada:
        clientes[id_cliente]["morada"] = morada.strip()
    if email:
        clientes[id_cliente]["email"] = email.strip()
    
    return 200, {id_cliente: clientes[id_cliente]}


def remover_cliente(id_cliente, id_barbearia=None):
  
    if id_cliente not in clientes:
        return 404, "Cliente não encontrado."
    
    cliente = clientes[id_cliente]
    
    # Se id_barbearia foi fornecido, valida se o cliente pertence a essa barbearia
    if id_barbearia and cliente.get("id_barbearia") != str(id_barbearia).strip():
        return 403, "Não tem permissão para remover este cliente."
    
    # apaga o registo do cliente do dicionario
    cliente_removido = clientes.pop(id_cliente)
    
    return 200, {id_cliente: cliente_removido}
