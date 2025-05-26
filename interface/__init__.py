def linha(caractere = '-', tamanho = 40):
    return caractere * tamanho


def header(msg):
    r = ""
    r += ('\n'+'=' * (len(msg) + 100))
    r += ('\n'+'     '+msg+'     ')
    r += ('\n'+'=' * (len(msg) + 100))
    return r


def leiaint(prompt):
    while True:
        try:
            n = int(input(prompt))
        except ValueError:
            print('Somente números inteiros!')
        else:
            return n


def leiafloat(prompt):
    while True:
        n = input(prompt).strip()
        if ',' in n:
            n = n.replace(',', '.')
        try:
            valor = float(n)
            return valor
        except ValueError:
            print('Somente números reais!')


def menu(lista):
    print(linha())
    for i in range (0, len(lista)):
        print(f'\033[32m{i+1}\033[m - \033[34m{lista[i]}\033[m')
    print(linha())
    opc = leiaint('Opção: ')
    if opc > len(lista):
        print('\033[31mOpção inválida\033[m')
    print(linha())
    return opc

