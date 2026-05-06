# 💈 Gestor de Barbearia

Um sistema completo de gestão para barbearias, desenvolvido em Python com funcionalidades de CRUD para clientes, serviços, agendamentos e mais.

---

## 📋 Sobre o Projeto

O **Gestor de Barbearia** é uma aplicação desenvolvida para auxiliar no gerenciamento operacional de barbearias. O sistema permite gerenciar:

- ✅ **Clientes** - Cadastro, consulta, atualização e exclusão de clientes
- ✅ **Barbearias** - Múltiplas unidades/filiais
- 📅 **Agendamentos** - Marcação de consultas (fase futura)
- 💰 **Serviços** - Catálogo de cortes e serviços (fase futura)
- 📊 **Relatórios** - Análise de dados e receitas (fase futura)

---

## 🚀 Funcionalidades Atuais (Fase 1)

### Gestão de Clientes
- ✅ **Criar Cliente** - Registar novo cliente com dados pessoais
- ✅ **Listar Clientes** - Ver todos os clientes ou filtrar por barbearia
- ✅ **Consultar Cliente** - Buscar dados detalhados de um cliente
- ✅ **Atualizar Cliente** - Editar informações de um cliente
- ✅ **Remover Cliente** - Deletar registo de um cliente

### Validações
- ✅ Validação de campos obrigatórios
- ✅ Validação de formatos (letras, números, email)
- ✅ Validação de permissões (multi-barbearia)
- ✅ Tratamento de erros com códigos HTTP

### Segurança
- ✅ Associação de clientes a barbearias específicas
- ✅ Validação de permissões em operações sensíveis
- ✅ Prevenção de acesso não autorizado entre barbearias

---

## 📁 Estrutura do Projeto

```
gestor-de-barbaeria/
├── README.md                 # Este arquivo
├── main.py                   # Arquivo principal da aplicação
├── clientes.py              # Módulo de gestão de clientes
├── barbearias.py            # Módulo de gestão de barbearias
├── utils.py                 # Funções utilitárias
└── tests/                   # Testes unitários (futuro)
```

---

## 🛠️ Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/taumaturgo04/gestor-de-barbaeria.git
cd gestor-de-barbaeria
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python main.py
```

---

## 📖 Guia de Uso

### Criar um Cliente

```python
from clientes import criar_cliente

status, resultado = criar_cliente(
    id_barbearia="B001",
    nome="João Silva",
    telefone="912345678",
    nif="123456789",
    iban="PT50ABIN0000000000001",
    morada="Rua Principal Lisboa",
    email="joao@email.com"
)

if status == 201:
    print(f"Cliente criado com ID: {resultado['id_cliente']}")
else:
    print(f"Erro: {resultado}")
```

### Listar Clientes

```python
from clientes import listar_clientes

# Todos os clientes
status, clientes = listar_clientes()

# Clientes de uma barbearia específica
status, clientes = listar_clientes(id_barbearia="B001")

if status == 200:
    for id_cliente, dados in clientes.items():
        print(f"{id_cliente}: {dados['nome']}")
```

### Consultar Cliente

```python
from clientes import consultar_cliente

status, cliente = consultar_cliente(
    id_cliente="C001",
    id_barbearia="B001"  # Validação de permissão
)

if status == 200:
    print(cliente)
elif status == 403:
    print("Acesso negado!")
```

### Atualizar Cliente

```python
from clientes import atualizar_cliente

status, resultado = atualizar_cliente(
    id_cliente="C001",
    id_barbearia="B001",
    email="novo.email@example.com",
    telefone="987654321"
)

if status == 200:
    print("Cliente atualizado com sucesso")
```

### Remover Cliente

```python
from clientes import remover_cliente

status, resultado = remover_cliente(
    id_cliente="C001",
    id_barbearia="B001"
)

if status == 200:
    print("Cliente removido com sucesso")
```

---

## 🔐 Códigos de Resposta HTTP

| Código | Significado | Explicação |
|--------|-------------|-----------|
| **200** | OK | Operação bem-sucedida (leitura/atualização) |
| **201** | Criado | Recurso criado com sucesso |
| **401** | Não Autorizado | Validação falhou (campos vazios, formato inválido) |
| **403** | Proibido | Sem permissão para acessar recursos de outra barbearia |
| **404** | Não Encontrado | Cliente ou barbearia não existe |

---

## 📝 Validações Implementadas

### Campos Obrigatórios
- Nome do cliente
- Telefone
- NIF (Número de Identificação Fiscal)
- IBAN (Número de Conta Bancária)
- Morada
- Email
- ID da Barbearia

### Tipos de Validação

#### Nome e Morada
- ✅ Apenas letras (sem números ou caracteres especiais)
- ✅ Não pode estar vazio

#### Telefone, NIF e IBAN
- ✅ Apenas números
- ✅ Não pode estar vazio

#### Email
- ✅ Não pode estar vazio
- ✅ (Validação de formato em desenvolvimento)

---

## 🔄 Fluxo de Dados

```
┌─────────────────┐
│  Entrada do Utilizador │
└──────────┬──────────┘
           │
           ▼
┌─────────────────┐
│  Validação de Campos │
└──────────┬──────────┘
           │
        ┌──┴──┐
        │     │
      ✅NO  ❌SIM
        │     │
        ▼     ▼
┌──────────┐ ┌─────────────────┐
│ Processar│ │ Retornar Erro   │
│  Dados   │ │ (401, mensagem) │
└──────┬───┘ └─────────────────┘
       │
       ▼
┌─────────────────┐
│  Validar Permissões │
│ (id_barbearia)  │
└──────────┬──────────┘
           │
        ┌──┴──┐
        │     │
      ✅SIM ❌NÃO
        │     │
        ▼     ▼
┌──────────┐ ┌─────────────────┐
│ Executar │ │ Retornar Erro   │
│ Operação │ │ (403, acesso)   │
└──────┬───┘ └─────────────────┘
       │
       ▼
┌─────────────────┐
│  Retornar Resultado │
│ (status, dados) │
└─────────────────┘
```

---

## 📊 Estrutura de Dados

### Dicionário de Clientes

```python
clientes = {
    "C001": {
        "id_barbearia": "B001",
        "nome": "João Silva",
        "telefone": "912345678",
        "nif": "123456789",
        "iban": "PT50ABIN0000000000001",
        "morada": "Rua Principal Lisboa",
        "email": "joao@email.com"
    },
    "C002": {
        "id_barbearia": "B002",
        "nome": "Maria Santos",
        "telefone": "918765432",
        "nif": "987654321",
        "iban": "PT50ABIN0000000000002",
        "morada": "Avenida Central Porto",
        "email": "maria@email.com"
    }
}
