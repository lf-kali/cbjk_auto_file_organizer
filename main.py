from lib.core import *


def mover_resultados(arquivos:FileGroup):
    destino = input('Novo caminho: ')
    arquivos.mover_todos(destino)


def copiar_resultados(arquivos:FileGroup):
    destino = input('Novo caminho: ')
    arquivos.copiar_todos(destino)


def excluir_resultados(arquivos:FileGroup):
    arquivos.excluir_todos()


def renomear_resultados(arquivos:FileGroup):
    nova_stem = input('Novo nome padrão para os arquivos: ')
    arquivos.renomear_todos(nova_stem)


def pesquisa():
    filtros = {}
    caminho_pesquisa = ler_caminho('Caminho a executar a pesquisa: ')
    menu_filtros = Menu('Selecionar Filtros:',
                        (
                            ('Palavra-chave', adiar_input_dict(filtros, 'palavra_chave', str)),
                            ('Extensão', adiar_input_dict(filtros, 'extensao', str)),
                            ('Tamanho mínimo', adiar_input_dict(filtros, 'tamanho_min', str)),
                            ('Tamanho máximo', adiar_input_dict(filtros, 'tamanho_max', str)),
                            ('Pesquisar', None),
                        )
    )

    menu_filtros.executar()

    filtragem = Filtro(**filtros)

    resultados = pesquisar_arquivos(caminho_pesquisa, filtro=filtragem)

    for resultado in resultados:
        print(resultado, end=f'\n{'='*80}\n')

    menu_manipulacao = Menu('Escolha o que fazer com os arquivos:',
                            (
                                ('Mover', adiar_execucao(mover_resultados, resultados)),
                                ('Copiar', adiar_execucao(copiar_resultados, resultados)),
                                ('Excluir', adiar_execucao(excluir_resultados, resultados)),
                                ('Renomear', adiar_execucao(renomear_resultados, resultados)),
                                ('Sair', None),
                            )
    )

    menu_manipulacao.executar()


def main():
    menu_inicial = Menu('Menu Inicial', (('Iniciar pesquisa', pesquisa), ('Sair', None)))
    menu_inicial.executar()


main()
