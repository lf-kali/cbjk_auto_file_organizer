import os


import interface as i
from lib.core import ler_caminho

if __name__ == '__main__':
    caminho = ler_caminho('Caminho do projeto: ')

    nome_projeto = caminho.split('\\')[-1]
    nome_arquivo_projeto = nome_projeto+'.txt'
    caminho_txt = os.path.join(caminho, nome_arquivo_projeto)

    varredura = list(item for item in os.walk(caminho) if '.idea' not in item[0] and '.venv' not in item[0] and '__' not in item[0])

    modulo = []

    for raiz, diretorios, arquivos in varredura:
        pular = 'logs' in raiz or 'profiles' in raiz

        if pular:
            continue

        nome_pacote = raiz.split('\\')[-1]

        txt = open(caminho_txt, 'a+', encoding='utf-8')
        txt.write(str(i.header(f'Pacote "{nome_pacote}": ')))
        print(i.header(f'Pacote "{nome_pacote}": '))

        for arquivo in arquivos:
            nome_arquivo, ext_arquivo = os.path.splitext(arquivo)

            if ext_arquivo != '.py':
                continue

            caminho_arquivo = os.path.join(raiz, arquivo)
            txt.write(str(i.header(f'\tMódulo "{arquivo[:-3]}:"')))
            print(i.header(f'\tMódulo "{arquivo[:-3]}":'))

            with open(caminho_arquivo, 'r', encoding='utf-8') as codigo:
                for linha in codigo:
                    modulo.append(linha)
                    print(linha)
            txt.write('\n')
            print('\n')

            for linha in modulo:
                txt.write(f'\t\t{linha}')
                print(f'\t\t{linha}')
            modulo.clear()





