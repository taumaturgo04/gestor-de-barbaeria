import Barbeiro
import cliente


def inicializar_sistema():
    Barbeiro.garantir_tabela()
    cliente.garantir_tabela()


def ler_dados_barbeiro():
    print("\nIntroduza os dados do barbeiro:")
    return (
        input("Nome: "),
        input("Especialidade: "),
        input("NIF: "),
        input("Categoria: "),
        input("Telefone: "),
        input("Morada: "),
        input("Email: "),
        input("IBAN: "),
        input("Horario: "),
    )


def ler_dados_cliente():
    print("\nIntroduza os dados do cliente:")
    return (
        input("Nome: "),
        input("Telefone: "),
        input("NIF: "),
        input("Email: "),
        input("Numero de cliente: "),
        input("Historico: "),
    )


def main():
    inicializar_sistema()

    while True:
        print("\n" + "=" * 40)
        print("      SISTEMA DE GESTAO BARBEARIA")
        print("=" * 40)
        print("1. Adicionar barbeiro")
        print("2. Listar barbeiros")
        print("3. Atualizar barbeiro")
        print("4. Remover barbeiro")
        print("-" * 40)
        print("5. Adicionar cliente")
        print("6. Listar clientes")
        print("7. Atualizar cliente")
        print("8. Remover cliente")
        print("-" * 40)
        print("0. Sair")

        opcao = input("\nEscolha uma opcao: ").strip()
        if opcao == "1":
            Barbeiro.adicionar(*ler_dados_barbeiro())
        elif opcao == "2":
            Barbeiro.listar()
        elif opcao == "3":
            id_barbeiro = input("ID do barbeiro a atualizar: ").strip()
            Barbeiro.atualizar(id_barbeiro, *ler_dados_barbeiro())
        elif opcao == "4":
            id_barbeiro = input("ID do barbeiro a remover: ").strip()
            Barbeiro.remover(id_barbeiro)
        elif opcao == "5":
            cliente.adicionar(*ler_dados_cliente())
        elif opcao == "6":
            cliente.listar()
        elif opcao == "7":
            id_cliente = input("ID do cliente a atualizar: ").strip()
            cliente.atualizar(id_cliente, *ler_dados_cliente())
        elif opcao == "8":
            id_cliente = input("ID do cliente a remover: ").strip()
            cliente.remover(id_cliente)
        elif opcao == "0":
            print("A encerrar o sistema.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
