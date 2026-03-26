# Gestor de Barbearia

Aplicacao de consola em Python para gerir uma barbearia com registo de barbeiros e clientes, usando uma base de dados SQLite local.

## Funcionalidades

- Adicionar barbeiros
- Listar barbeiros
- Atualizar barbeiros
- Remover barbeiros
- Adicionar clientes
- Listar clientes
- Atualizar clientes
- Remover clientes
- Criacao automatica das tabelas em SQLite, se nao existirem

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicacao e menu principal
- `Barbeiro.py`: operacoes CRUD da tabela `barbeiros`
- `cliente.py`: operacoes CRUD da tabela `clientes`
- `barbearia.db`: base de dados SQLite usada pela aplicacao

## Requisitos

- Python 3.x
- Biblioteca `sqlite3` (incluida por defeito no Python)

## Como executar

No terminal, dentro da pasta `gestor de Barbearia`, execute:

```bash
python main.py
```

## Menu da aplicacao

Ao iniciar, o programa apresenta as seguintes opcoes:

```text
1. Adicionar barbeiro
2. Listar barbeiros
3. Atualizar barbeiro
4. Remover barbeiro
5. Adicionar cliente
6. Listar clientes
7. Atualizar cliente
8. Remover cliente
0. Sair
```

## Dados guardados

### Barbeiros

Os barbeiros incluem os seguintes campos:

- `id`
- `nome`
- `especialidade`
- `nif`
- `categoria`
- `telefone`
- `morada`
- `email`
- `iban`
- `horario`

### Clientes

Os clientes incluem os seguintes campos:

- `id`
- `nome`
- `telefone`
- `nif`
- `email`
- `numero_cliente`
- `historico`

## Comportamento da base de dados

- A aplicacao usa o ficheiro `barbearia.db`
- As tabelas sao criadas automaticamente com `CREATE TABLE IF NOT EXISTS`
- O campo `nif` e unico tanto em barbeiros como em clientes
- O sistema tenta adaptar estruturas antigas da base de dados, adicionando colunas em falta quando necessario

## Exemplo de utilizacao

1. Executar `python main.py`
2. Escolher a opcao `1` para registar um barbeiro ou `5` para registar um cliente
3. Preencher os dados pedidos no terminal
4. Usar as opcoes de listagem, atualizacao e remocao conforme necessario

## Observacoes

- Os dados sao geridos diretamente no terminal
- A validacao atual e basica, focada principalmente na unicidade do `nif`
- O projeto esta organizado de forma simples, adequado para aprendizagem de Python com SQLite e operacoes CRUD
