# importa as funcoes de gestao de barbeiros
from barbeiro import (
    criar_barbeiro,
    listar_barbeiros,
    consultar_barbeiro,
    atualizar_barbeiro,
    remover_barbeiro,
)
# importa as funcoes de gestao de clientes
from cliente import (
    criar_cliente,
    listar_clientes,
    consultar_cliente,
    atualizar_cliente,
    remover_cliente,
)


def menu():
    # mostra as opcoes disponiveis no terminal
    print("\n===== GESTOR DE BARBEARIA =====")
    print("1 - Criar barbeiro")
    print("2 - Listar barbeiros")
    print("3 - Consultar barbeiro")
    print("4 - Atualizar barbeiro")
    print("5 - Remover barbeiro")
    print("6 - Criar cliente")
    print("7 - Listar clientes")
    print("8 - Consultar cliente")
    print("9 - Atualizar cliente")
    print("10 - Remover cliente")
    print("0 - Sair")


def ler_campo_opcional(texto):
    valor = input(texto)
    if valor == "":
        return None
    return valor


def mostrar_resultado(resultado):
    codigo, obj = resultado
    if codigo in (200, 201):
        print(obj)
    else:
        print("ERRO: " + str(codigo) + " - " + str(obj))

def main():
    # ciclo principal do programa
    while True:
        menu()
        try:
            opcao = input("Escolha uma opcao: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nVolte sempre!")
            break

        if opcao == "1":
            # cría um novo barbeiro com os dados introduzidos
            resultado = criar_barbeiro(
                input("Nome: "),
                input("Especialidade: "),
                input("Telefone: "),
                input("NIF: "),
                input("IBAN: "),
                input("Morada: "),
                input("Email: "),
            )
            mostrar_resultado(resultado)

        elif opcao == "2":
            # lista todos os barbeiros
            mostrar_resultado(listar_barbeiros())
        elif opcao == "3":
            # consulta um barbeiro pelo ID
            mostrar_resultado(consultar_barbeiro(input("ID do barbeiro: ").strip()))
        elif opcao == "4":
            # atualiza apenas os campos preenchidos
            id_barbeiro = input("ID do barbeiro: ").strip()
            resultado = atualizar_barbeiro(
                id_barbeiro,
                ler_campo_opcional("Novo nome (enter para manter): "),
                ler_campo_opcional("Nova especialidade (enter para manter): "),
                ler_campo_opcional("Novo telefone (enter para manter): "),
                ler_campo_opcional("Novo NIF (enter para manter): "),
                ler_campo_opcional("Novo IBAN (enter para manter): "),
                ler_campo_opcional("Nova morada (enter para manter): "),
                ler_campo_opcional("Novo email (enter para manter): "),
            )
            mostrar_resultado(resultado)
        elif opcao == "5":
            # remove um barbeiro pelo ID
            mostrar_resultado(remover_barbeiro(input("ID do barbeiro: ").strip()))
        elif opcao == "6":
            # cría um novo cliente com os dados introduzidos
            resultado = criar_cliente(
                input("Nome: "),
                input("Telefone: "),
                input("NIF: "),
                input("IBAN: "),
                input("Morada: "),
                input("Email: "),
            )
            mostrar_resultado(resultado)
        elif opcao == "7":
            # lista todos os clientes
            mostrar_resultado(listar_clientes())
        elif opcao == "8":
            # consulta um cliente pelo ID
            mostrar_resultado(consultar_cliente(input("ID do cliente: ").strip()))
        elif opcao == "9":
            # atualiza apenas os campos preenchidos
            id_cliente = input("ID do cliente: ").strip()
            resultado = atualizar_cliente(
                id_cliente,
                ler_campo_opcional("Novo nome (enter para manter): "),
                ler_campo_opcional("Novo telefone (enter para manter): "),
                ler_campo_opcional("Novo NIF (enter para manter): "),
                ler_campo_opcional("Novo IBAN (enter para manter): "),
                ler_campo_opcional("Nova morada (enter para manter): "),
                ler_campo_opcional("Novo email (enter para manter): "),
            )
            mostrar_resultado(resultado)
        elif opcao == "10":
            # remove um cliente pelo ID
            mostrar_resultado(remover_cliente(input("ID do cliente: ").strip()))
        elif opcao == "0":
            print("Volte sempre!")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    # executa o programa apenas quando este ficheiro e corrido diretamente
    main()
