from lib.core import *


def pesquisa_manual():
    filtros = {}
    caminho_pesquisa = ler_caminho('Caminho a executar a pesquisa: ')

    menu_filtros = Menu('Selecionar Filtros:',
        ('Palavra-chave', adiar_input_dict(filtros, 'palavra_chave', str)),
        ('Extensão', adiar_input_dict(filtros, 'extensao', str)),
        ('Tamanho mínimo', adiar_input_dict(filtros, 'tamanho_min', str)),
        ('Tamanho máximo', adiar_input_dict(filtros, 'tamanho_max', str)),
        ('Pesquisar', None),
    )

    menu_filtros.executar()

    resultados = pesquisar_arquivos(caminho_pesquisa, filtro=filtros)

    for resultado in resultados:
        print(resultado, end=f'\n{'='*80}\n')

    menu_manipulacao = Menu(
        'Escolha o que fazer com os arquivos:',
        ('Mover', adiar_execucao(mover_resultados, resultados)),
        ('Copiar', adiar_execucao(copiar_resultados, resultados)),
        ('Excluir', adiar_execucao(excluir_resultados, resultados)),
        ('Renomear', adiar_execucao(renomear_resultados, resultados)),
        ('Sair', None),
    )

    menu_manipulacao.executar()


def main():
    menu_inicial = Menu(
        'Menu Inicial', (
            ('Iniciar pesquisa manual', pesquisa_manual),
            #('Iniciar pesquisa automática', pesquisa_automatica),
            ('Sair', None),
        )
    )
    menu_inicial.executar()


main()
