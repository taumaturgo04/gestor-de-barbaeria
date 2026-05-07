# importa as funções de gestão de barbearias
from barbearia import (
    criar_barbearia,
    listar_barbearias,
    consultar_barbearia,
    atualizar_barbearia,
    remover_barbearia,
)
# importa as funções de gestão de barbeiros
from barbeiro import (
    criar_barbeiro,
    listar_barbeiros,
    consultar_barbeiro,
    atualizar_barbeiro,
    remover_barbeiro,
)
# importa as funções de gestão de clientes
from cliente import (
    criar_cliente,
    listar_clientes,
    consultar_cliente,
    atualizar_cliente,
    remover_cliente,
)
from agendamento import (
    criar_agendamento,
    listar_agendamentos,
    consultar_agendamento,
    atualizar_status,
    eliminar_agendamento,
)
from produto import (
    adicionar_produto,
    listar_produtos,
    consultar_produto,
    atualizar_produto,
    vender_produto,
    remover_produto,
)


def menu():
    # mostra as opções disponíveis no terminal
    print("\n===== GESTOR DE BARBEARIA =====")
    print("--- BARBEARIAS ---")
    print("1 - Criar barbearia")
    print("2 - Listar barbearias")
    print("3 - Consultar barbearia")
    print("4 - Atualizar barbearia")
    print("5 - Remover barbearia")
    print("--- BARBEIROS ---")
    print("6 - Criar barbeiro")
    print("7 - Listar barbeiros")
    print("8 - Consultar barbeiro")
    print("9 - Atualizar barbeiro")
    print("10 - Remover barbeiro")
    print("--- CLIENTES ---")
    print("11 - Criar cliente")
    print("12 - Listar clientes")
    print("13 - Consultar cliente")
    print("14 - Atualizar cliente")
    print("15 - Remover cliente")
    print("--- AGENDAMENTOS ---")
    print("16 - Criar agendamento")
    print("17 - Listar agendamentos")
    print("18 - Consultar agendamento")
    print("19 - Atualizar status do agendamento")
    print("20 - Eliminar agendamento")
    print("--- PRODUTOS ---")
    print("21 - Adicionar produto")
    print("22 - Listar produtos")
    print("23 - Consultar produto")
    print("24 - Atualizar produto")
    print("25 - Vender produto")
    print("26 - Remover produto")
    print("0 - Sair")


def ler_campo_opcional(texto):
    valor = input(texto)
    if valor == "":
        return None
    return valor


def formatar_objeto(obj):
    if isinstance(obj, dict):
        if obj and all(isinstance(valor, dict) for valor in obj.values()):
            for identificador, dados in obj.items():
                print(f"{identificador}: {dados}")
            return
        print(obj)
        return
    print(obj)


def mostrar_resultado(resultado):
    codigo, obj = resultado
    if codigo in (200, 201):
        formatar_objeto(obj)
    else:
        print("ERRO: " + str(codigo) + " - " + str(obj))


def main():
    # ciclo principal do programa
    while True:
        menu()
        try:
            opcao = input("Escolha uma opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nVolte sempre!")
            break

        if opcao == "1":
            # críar uma nova barbearia
            resultado = criar_barbearia(
                input("Nome: "),
                input("Morada: "),
                input("NIF: "),
            )
            mostrar_resultado(resultado)

        elif opcao == "2":
            # lista todas as barbearias
            mostrar_resultado(listar_barbearias())

        elif opcao == "3":
            # consulta uma barbearia pelo ID
            mostrar_resultado(consultar_barbearia(input("ID da barbearia: ").strip()))

        elif opcao == "4":
            # atualiza uma barbearia
            id_barbearia = input("ID da barbearia: ").strip()
            resultado = atualizar_barbearia(
                id_barbearia,
                ler_campo_opcional("Novo nome (enter para manter): "),
                ler_campo_opcional("Nova morada (enter para manter): "),
                ler_campo_opcional("Novo NIF (enter para manter): "),
            )
            mostrar_resultado(resultado)

        elif opcao == "5":
            # remove uma barbearia
            mostrar_resultado(remover_barbearia(input("ID da barbearia: ").strip()))

        elif opcao == "6":
            # cría um novo barbeiro com os dados introduzidos
            resultado = criar_barbeiro(
                input("Nome: "),
                input("Especialidade: "),
                input("Telefone: "),
                input("NIF: "),
                input("IBAN: "),
                input("Morada: "),
                input("Email: "),
                input("ID da barbearia: "),
            )
            mostrar_resultado(resultado)

        elif opcao == "7":
            # lista todos os barbeiros
            mostrar_resultado(listar_barbeiros())
        elif opcao == "8":
            # consulta um barbeiro pelo ID
            mostrar_resultado(consultar_barbeiro(input("ID do barbeiro: ").strip()))
        elif opcao == "9":
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
                ler_campo_opcional("Novo ID da barbearia (enter para manter): "),
            )
            mostrar_resultado(resultado)
        elif opcao == "10":
            # remove um barbeiro pelo ID
            mostrar_resultado(remover_barbeiro(input("ID do barbeiro: ").strip()))
        elif opcao == "11":
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
        elif opcao == "12":
            # lista todos os clientes
            mostrar_resultado(listar_clientes())
        elif opcao == "13":
            # consulta um cliente pelo ID
            mostrar_resultado(consultar_cliente(input("ID do cliente: ").strip()))
        elif opcao == "14":
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
        elif opcao == "15":
            # remove um cliente pelo ID
            mostrar_resultado(remover_cliente(input("ID do cliente: ").strip()))
        elif opcao == "16":
            code, obj = listar_clientes()
            if code == 200:
                print(obj)
                id_cliente = input("ID do cliente: ").strip()
            else:
                print("Não há clientes")
                continue

            resultado = criar_agendamento(
                input("Data e hora (YYYY-MM-DD HH:MM): "),
                id_cliente,
                input("ID do barbeiro: ").strip(),
                input("Servico: "),
                input("ID da barbearia: ").strip(),
            )
            mostrar_resultado(resultado)
        elif opcao == "17":
            mostrar_resultado(listar_agendamentos())
        elif opcao == "18":
            mostrar_resultado(consultar_agendamento(input("ID do agendamento: ").strip()))
        elif opcao == "19":
            id_agendamento = input("ID do agendamento: ").strip()
            resultado = atualizar_status(
                id_agendamento,
                input("Novo status: "),
            )
            mostrar_resultado(resultado)
        elif opcao == "20":
            mostrar_resultado(eliminar_agendamento(input("ID do agendamento: ").strip()))
        elif opcao == "21":
            resultado = adicionar_produto(
                input("Nome do produto: "),
                input("Preco de venda: "),
                input("Quantidade em stock: "),
                input("ID da barbearia: ").strip(),
            )
            mostrar_resultado(resultado)
        elif opcao == "22":
            mostrar_resultado(listar_produtos())
        elif opcao == "23":
            mostrar_resultado(consultar_produto(input("ID do produto: ").strip()))
        elif opcao == "24":
            id_produto = input("ID do produto: ").strip()
            resultado = atualizar_produto(
                id_produto,
                ler_campo_opcional("Novo nome (enter para manter): "),
                ler_campo_opcional("Novo preco (enter para manter): "),
                ler_campo_opcional("Nova quantidade (enter para manter): "),
                ler_campo_opcional("Novo ID da barbearia (enter para manter): "),
            )
            mostrar_resultado(resultado)
        elif opcao == "25":
            resultado = vender_produto(
                input("ID do produto: ").strip(),
                input("Quantidade vendida: "),
            )
            mostrar_resultado(resultado)
        elif opcao == "26":
            mostrar_resultado(remover_produto(input("ID do produto: ").strip()))
        elif opcao == "0":
            print("Volte sempre!")
            break
        else:
            print("Opção invalida.")


if __name__ == "__main__":
    # executa o programa apenas quando este ficheiro e corrido diretamente
    main()
