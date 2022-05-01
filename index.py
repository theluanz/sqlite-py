from database import *


def clean(pressEnter=True):
    if (pressEnter):
        input('Precione enter para continuar')
    print('\n'*30)


def init():
    opcao = 0
    pressEnter = False
    while not(opcao == "6"):
        clean(pressEnter)
        pressEnter = True
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Criar tabela')
        print('2. Incluir dados')
        print('3. Alterar dados')
        print('4. Excluir dados')
        print('5. Listar dados')
        print('6. Sair')

        opcao = input('Opção [1-5]: ')

        if opcao == "1":
            clean(False)
            create_table_inputs()
        elif opcao == "2":
            clean(False)
            insert_data_inputs()
        elif opcao == "3":
            clean(False)
            update_data_inputs() 
        elif opcao == "4":
            clean(False)
            delete_data_inputs()
        elif opcao == "5":
            clean(False)
            list_data_inputs()
        elif opcao == "6":
            print("Finalizando...")
            break
        else:
            print("Comando inválido")


def create_table_inputs():
    print("Digite qual tabela você deseja criar?")
    table = input("TABELA: ")
    print(table)
    print("="*100)
    nomes_campos = []
    tipos_campos = []
    opt = 1
    args = []
    while opt != "0":
        print(
            "Digite o nome de uma coluna que você deseja adicionar (escreva 0 para parar): ")
        opt = input("COLUNA: ")
        if opt != "0":
            nomes_campos.append(opt)
            print(
                f"Digite o formato da coluna {opt} (caso queira que seja AUTOINCREMENT, escreva aqui também)")
            tipos_campos.append(input("TIPO DE DADO: "))
    for x in range(0, len(nomes_campos)):
        args.append([nomes_campos[x], tipos_campos[x]])
    createTable(connectDb(), table, args)


def insert_data_inputs():
    print("Qual tabela você deseja adicionar dados?")
    printTable()

    table = input()
    colunas = get_columns(connectDb(), table)
    if len(colunas) > 0:
        dados = []
        for coluna in colunas:
            print(f"Dado para a coluna {coluna[0]}")
            dados.append(input(f"Tipo de dado {coluna[1]}: "))
        insertDbCommit(connectDb(), table, colunas, dados)
    else:
        print("Essa tabela não existe ou não tem colunas.")

def update_data_inputs():
    print("Qual tabela você deseja atualizar algum dado?")
    printTable()
    table = input()
    colunas = get_columns(connectDb(), table)
    nome_colunas = ''
    for coluna in colunas:
        nome_colunas += "|" + coluna[0].upper() + "|"
    print("Com base em qual coluna você deseja verificar (WHERE)?")
    print(nome_colunas)
    where= [input()]
    where.append(input(f"Quando {where[0]} for igual a: "))
    print("Qual coluna você deseja atualizar (WHERE)?")
    print(nome_colunas)
    value= [input()]
    value.append(input("Atualizar para: "))
    updateDbCommit(connectDb(), table, value, where)


def list_data_inputs():
    print("Qual tabela você deseja visualizar os dados?")
    printTable()
    table = input()
    colunas = get_columns(connectDb(), table)

    if len(colunas) > 0:
        nome_colunas = ''
        for coluna in colunas:
            nome_colunas += "|" + coluna[0].upper() + "|"
        print("Quais colunas você deseja visualizar? Separe utilizando virgulas (caso queira ver todas, excreva *)")
        print("COLUNAS: " + nome_colunas)
        params = input()

        registros = selectQueryDb(connectDb(), table, params)
        if(params == "*"):
            for x in range(0, len(registros)):
                for i in range(0, len(colunas)):
                    print(f'{colunas[i][0].upper()}: ' + f'{registros[x][i]}')
                print("="*10)

        else:
            params = params.split(',')
            for x in range(0, len(registros)):
                for i in range(len(params)):
                    print(f'{params[i].upper()}: ' + f'{registros[x][i]}')
                print("="*10)
    else:
        print("Essa tabela não existe ou não tem colunas.")


def delete_data_inputs():
    print("Qual tabela você deseja deletar algum dado?")
    printTable()
    table = input()
    colunas = get_columns(connectDb(), table)
    nome_colunas = ''
    for coluna in colunas:
        nome_colunas += "|" + coluna[0].upper() + "|"
    print(nome_colunas)
    print("Com base em qual coluna você deseja verificar?")
    where = [input()]
    where.append(input("Qual valor?"))
    deleteDbCommit(connectDb(), table, where)

def printTable():
    tabelas = get_tables(connectDb())
    nome_tabelas = ''
    for tabela in tabelas:
        nome_tabelas += "|" + tabela[0].upper() + "|"
    print("Tabelas existentes:", nome_tabelas)


init()
