import sqlite3

DB_PATH = "barbearia.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def garantir_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            nif TEXT UNIQUE NOT NULL,
            email TEXT,
            numero_cliente TEXT,
            historico TEXT
        )
        """
    )

    colunas = {
        "nome": "TEXT NOT NULL DEFAULT ''",
        "telefone": "TEXT",
        "nif": "TEXT UNIQUE",
        "email": "TEXT",
        "numero_cliente": "TEXT",
        "historico": "TEXT",
    }

    existentes = {
        coluna[1] for coluna in cursor.execute("PRAGMA table_info(clientes)").fetchall()
    }
    for nome_coluna, definicao in colunas.items():
        if nome_coluna not in existentes:
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {nome_coluna} {definicao}")

    if "historico_resumo" in existentes and "historico" not in existentes:
        cursor.execute(
            "UPDATE clientes SET historico = COALESCE(historico_resumo, '') "
            "WHERE COALESCE(historico, '') = ''"
        )

    conn.commit()
    conn.close()


def adicionar(nome, telefone, nif, email, numero_cliente, historico=""):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO clientes
            (nome, telefone, nif, email, numero_cliente, historico)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nome, telefone, nif, email, numero_cliente, historico),
        )
        conn.commit()
        conn.close()
        print(f"Cliente {nome} registado com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: este NIF ja esta associado a outro cliente.")
    except Exception as erro:
        print(f"Erro ao adicionar cliente: {erro}")

def listar():
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        rows = cursor.execute(
            """
            SELECT id, nome, telefone, nif, email, numero_cliente
            FROM clientes
            ORDER BY id
            """
        ).fetchall()
        conn.close()

        print("\n--- CLIENTES ---")
        if not rows:
            print("Sem clientes registados.")
            return

        for cliente_row in rows:
            print(
                f"ID: {cliente_row[0]} | Nome: {cliente_row[1]} | Tel: {cliente_row[2]} | "
                f"NIF: {cliente_row[3]} | Email: {cliente_row[4]} | Numero: {cliente_row[5]}"
            )
    except Exception as erro:
        print(f"Erro ao listar clientes: {erro}")


def atualizar(id_cliente, nome, telefone, nif, email, numero_cliente, historico=""):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE clientes
            SET nome = ?, telefone = ?, nif = ?, email = ?, numero_cliente = ?, historico = ?
            WHERE id = ?
            """,
            (nome, telefone, nif, email, numero_cliente, historico, id_cliente),
        )
        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        if alterados:
            print(f"Cliente ID {id_cliente} atualizado com sucesso.")
        else:
            print("ID de cliente nao encontrado.")
    except sqlite3.IntegrityError:
        print("Erro: este NIF ja esta associado a outro cliente.")
    except Exception as erro:
        print(f"Erro ao atualizar cliente: {erro}")

def remover(id_cliente):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conn.commit()
        removidos = cursor.rowcount
        conn.close()

        if removidos:
            print(f"Cliente ID {id_cliente} removido com sucesso.")
        else:
            print("ID de cliente nao encontrado.")
    except Exception as erro:
        print(f"Erro ao remover cliente: {erro}")
