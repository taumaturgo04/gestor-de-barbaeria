```markdown
💈 Gestor de Barbearia

Um sistema completo de gestão para barbearias desenvolvido em Python.

---

📋 Sobre o Projeto

O **Gestor de Barbearia** é uma aplicação de desktop/console para auxiliar na administração de barbearias. Permite gerir clientes, barbeiros, barbearias, produtos, agendamentos e stock de forma simples e eficiente.

---

✨ Funcionalidades Atuais (Fase 1)

 ✅ Módulos Completos
- **Barbearias** — Gestão de múltiplas unidades/filiais
- **Barbeiros** — Cadastro e gestão de profissionais
- **Clientes** — Cadastro, listagem e histórico
- **Produtos** — Gestão de stock e produtos à venda
- **Agendamentos** — Marcação e controlo de horários

 🔧 Funcionalidades Comuns
- CRUD completo (Criar, Ler, Atualizar, Eliminar)
- Logging detalhado em ficheiros separados
- Validações rigorosas de dados
- Suporte a múltiplas barbearias (isolamento de dados)
- Persistência em JSON
- Geração automática de IDs

---

📁 Estrutura do Projeto

```bash
gestor-de-barbearia/
├── main.py                     # Ponto de entrada da aplicação
├── clientes.py
├── barbearias.py
├── barbeiros.py
├── produtos.py
├── agendamentos.py
├── utils.py                    # Funções de validação e IDs
├── entidades.py                # Classes (opcional - futuro)
├── *.log                       # Ficheiros de logs
├── clientes.json
├── barbearias.json
├── barbeiros.json
├── produtos.json
├── agendamentos.json
├── README.md
└── requirements.txt
```

---

## 🛠️ Instalação

### Requisitos
- Python 3.8 ou superior

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/taumaturgo04/gestor-de-barbearia.git
cd gestor-de-barbearia
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
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

## 📖 Exemplo de Utilização

### Criar um Cliente
```python
from clientes import criar_cliente

status, resultado = criar_cliente(
    id_barbearia="BR001",
    nome="João Silva",
    telefone="912345678",
    nif="123456789",
    iban="PT5000000000000000000",
    morada="Rua das Flores, 45 Lisboa",
    email="joao.silva@email.com"
)

print(status, resultado)
```

### Outros Exemplos
- `listar_clientes(id_barbearia="BR001")`
- `consultar_cliente("C001", id_barbearia="BR001")`
- `atualizar_cliente("C001", nome="João Silva Santos")`

---

## 🔢 Códigos de Resposta

| Código | Significado              | Descrição |
|--------|--------------------------|---------|
| 200    | OK                       | Operação bem-sucedida |
| 201    | Criado                   | Registo criado com sucesso |
| 400    | Bad Request              | Dados inválidos |
| 401    | Unauthorized             | Campos vazios ou inválidos |
| 403    | Forbidden                | Sem permissão (outra barbearia) |
| 404    | Not Found                | Recurso não encontrado |

---

## 📌 Próximas Funcionalidades (Fase 2)

- Interface gráfica (Tkinter ou customtkinter)
- Agendamentos com calendário
- Vendas e faturação
- Relatórios e estatísticas
- Autenticação de utilizadores
- Backup automático

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Criar pull requests
