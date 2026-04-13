# Gestor Simples de Barbearia

Projeto simples em Python para gerir barbeiros e clientes em terminal.

## Funcionalidades

- Criar barbeiros
- Listar barbeiros
- Consultar barbeiro por ID
- Atualizar barbeiro
- Remover barbeiro
- Criar clientes
- Listar clientes
- Consultar cliente por ID
- Atualizar cliente
- Remover cliente

## Estrutura

- `src/main.py`: menu principal da aplicacao
- `src/Barbeiro.py`: funcoes CRUD dos barbeiros
- `src/cliente.py`: funcoes CRUD dos clientes

## Dados guardados

Os dados sao guardados em dicionarios em memoria.

Cada barbeiro guarda:

- nome
- especialidade
- telefone
- nif
- iban
- morada
- email

Cada cliente guarda:

- nome
- telefone
- nif
- iban
- morada
- email

## Validacoes

- Se um campo obrigatorio vier vazio ou com apenas espacos, o sistema devolve erro `401`
- Se o ID nao existir, o sistema devolve erro `404`

## Como executar

Executa o ficheiro:

```bash
python src/main.py
```

## Exemplo de IDs

- Barbeiros: `B001`, `B002`
- Clientes: `C001`, `C002`

## Notas

- O projeto nao usa classes
- O projeto usa apenas funcoes e dicionarios
- Os dados desaparecem quando o programa termina
