import sqlite3

DB_PATH = "barbearia.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def garantir_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS barbeiros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            nif TEXT UNIQUE NOT NULL,
            categoria TEXT,
            telefone TEXT,
            morada TEXT,
            email TEXT,
            iban TEXT,
            horario TEXT
        )
        """
    )

    colunas = {
        "nome": "TEXT NOT NULL DEFAULT ''",
        "especialidade": "TEXT NOT NULL DEFAULT ''",
        "nif": "TEXT UNIQUE",
        "categoria": "TEXT",
        "telefone": "TEXT",
        "morada": "TEXT",
        "email": "TEXT",
        "iban": "TEXT",
        "horario": "TEXT",
    }

    existentes = {
        coluna[1] for coluna in cursor.execute("PRAGMA table_info(barbeiros)").fetchall()
    }
    for nome_coluna, definicao in colunas.items():
        if nome_coluna not in existentes:
            cursor.execute(f"ALTER TABLE barbeiros ADD COLUMN {nome_coluna} {definicao}")

    if "especialidades" in existentes and "especialidade" not in existentes:
        cursor.execute(
            "UPDATE barbeiros SET especialidade = COALESCE(especialidades, '') "
            "WHERE COALESCE(especialidade, '') = ''"
        )
    if "número" in existentes and "telefone" not in existentes:
        cursor.execute(
            "UPDATE barbeiros SET telefone = COALESCE([número], '') "
            "WHERE COALESCE(telefone, '') = ''"
        )
    if "horario de trabalho" in existentes and "horario" not in existentes:
        cursor.execute(
            "UPDATE barbeiros SET horario = COALESCE([horario de trabalho], '') "
            "WHERE COALESCE(horario, '') = ''"
        )

    conn.commit()
    conn.close()


def adicionar(nome, especialidade, nif, categoria, telefone, morada, email, iban, horario):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO barbeiros
            (nome, especialidade, nif, categoria, telefone, morada, email, iban, horario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, especialidade, nif, categoria, telefone, morada, email, iban, horario),
        )
        conn.commit()
        conn.close()
        print(f"Barbeiro {nome} registado com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: este NIF ja existe.")
    except Exception as erro:
        print(f"Erro ao adicionar barbeiro: {erro}")


def listar():
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        rows = cursor.execute(
            """
            SELECT id, nome, especialidade, nif, categoria, telefone
            FROM barbeiros
            ORDER BY id
            """
        ).fetchall()
        conn.close()

        print("\n--- BARBEIROS ---")
        if not rows:
            print("Sem barbeiros registados.")
            return

        for barbeiro in rows:
            print(
                f"ID: {barbeiro[0]} | Nome: {barbeiro[1]} | Especialidade: {barbeiro[2]} | "
                f"NIF: {barbeiro[3]} | Categoria: {barbeiro[4]} | Tel: {barbeiro[5]}"
            )
    except Exception as erro:
        print(f"Erro ao listar barbeiros: {erro}")


def atualizar(id_barbeiro, nome, especialidade, nif, categoria, telefone, morada, email, iban, horario):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE barbeiros
            SET nome = ?, especialidade = ?, nif = ?, categoria = ?, telefone = ?,
                morada = ?, email = ?, iban = ?, horario = ?
            WHERE id = ?
            """,
            (nome, especialidade, nif, categoria, telefone, morada, email, iban, horario, id_barbeiro),
        )
        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        if alterados:
            print(f"Barbeiro ID {id_barbeiro} atualizado com sucesso.")
        else:
            print("ID de barbeiro nao encontrado.")
    except sqlite3.IntegrityError:
        print("Erro: este NIF ja esta associado a outro barbeiro.")
    except Exception as erro:
        print(f"Erro ao atualizar barbeiro: {erro}")


def remover(id_barbeiro):
    try:
        garantir_tabela()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM barbeiros WHERE id = ?", (id_barbeiro,))
        conn.commit()
        removidos = cursor.rowcount
        conn.close()

        if removidos:
            print(f"Barbeiro ID {id_barbeiro} removido com sucesso.")
        else:
            print("ID de barbeiro nao encontrado.")
    except Exception as erro:
        print(f"Erro ao remover barbeiro: {erro}")
