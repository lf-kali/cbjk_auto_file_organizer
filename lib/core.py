import os

import shutil

from typing import Type

class FormattedSize:
    _LABELS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    __BASE = 1024


    def __init__(self, size:tuple[float|int, str]):
        if size[0] > 0:
            self._num = size[0]
        else:
            raise ValueError(f'"{size[0]}" não é um numero válido.')

        if size[1].upper() in FormattedSize._LABELS:
            self._txt = size[1]
        else:
            raise ValueError(f'Unidade de tamanho inexistente: {size[1]}')


    def tobytes(self):
        for exp in range(6, 0, -1):
            idx = exp - 1
            if FormattedSize._LABELS[idx] == self._txt:
                return int(self._num * FormattedSize.__BASE ** exp)


    def tostr(self):
        return f'{self._num}{self._txt}'


    @property
    def num(self):
        return self._num


    @property
    def txt(self):
        return self._txt


    @classmethod
    def frombytes(cls, size:int):
        for exp, label in enumerate(cls._LABELS):
            next_size = cls.__BASE ** (exp+1)
            if size < next_size:
                tamanho = float(size / cls.__BASE ** exp)
                return cls((round(tamanho, 2), label))


    @classmethod
    def fromstr(cls, txt:str):
        txt = txt.upper().replace(' ', '')

        for i, char in enumerate(txt):
            if not (char.isdigit() or char == '.'):
                break
        else:
            raise ValueError(f'Não foi possível identificar a unidade em {txt}.')

        num_str = txt[:i]
        label = txt[i:]

        try:
            num = float(num_str)
        except ValueError:
            raise ValueError(f'{num_str} não é um número válido.')

        if label not in cls._LABELS:
            raise ValueError(f'Unidade de tamanho inexistente: {label}')

        return cls((num, label))

    def __str__(self):
        return f'{self._num}{self._txt}'


class Arquivo:
    def __init__(self, caminho:str):
        self._caminho = caminho
        self._raiz, self._nome = os.path.split(caminho)
        self._stem, self._extensao = os.path.splitext(self._nome)
        self._tamanho = os.path.getsize(caminho)


    @property
    def caminho(self):
        return self._caminho


    @property
    def raiz(self):
        return self._raiz


    @property
    def nome(self):
        return self._nome


    @property
    def stem(self):
        return self._stem


    @property
    def extensao(self):
        return self._extensao


    @property
    def tamanho(self):
        return self._tamanho


    def formatar_tamanho(self):
        tamanho = FormattedSize.frombytes(self._tamanho)
        return tamanho.tostr()


    def mover(self, destino:str):
        novo_caminho = os.path.join(destino, self.nome)
        shutil.move(self._caminho, novo_caminho)


    def copiar(self, destino:str):
        novo_caminho = os.path.join(destino, self.nome)
        shutil.copy(self.caminho, novo_caminho)


    def excluir(self):
        os.remove(self.caminho)


    def renomear(self, nova_stem):
        novo_nome = f'{nova_stem}{self.extensao}'
        novo_caminho = os.path.join(self.raiz, novo_nome)
        os.rename(self.caminho, novo_caminho)
        self._caminho = novo_caminho
        self._raiz, self._nome = os.path.split(novo_caminho)
        self._stem = nova_stem


    def __repr__(self):
        return f'Nome: {self.nome}, Tamanho: {self.formatar_tamanho()}, Caminho: {self.caminho}'


class FileGroup(list):
    def __init__(self, group:list[Arquivo]):
        super().__init__(group)


    def mover_todos(self, destino: str):
        for arquivo in self:
            arquivo.mover(destino)


    def copiar_todos(self, destino: str):
        for arquivo in self:
            arquivo.copiar(destino)


    def excluir_todos(self):
        for arquivo in self:
            arquivo.excluir()


    def renomear_todos(self, nova_stem):
        for i, arquivo in enumerate(self):
            arquivo.renomear(f'{nova_stem}_{i}')


class Filtro:
    def __init__(self, *, palavra_chave:str=None, extensao:str=None, tamanho_min:FormattedSize=None, tamanho_max:FormattedSize=None):
        self.palavra_chave = palavra_chave
        self.extensao = extensao
        self.tamanho_min = tamanho_min
        self.tamanho_max = tamanho_max

    def match(self, arquivo:Arquivo):
        testes = []

        if self.palavra_chave is not None:
            teste_palavra_chave = self.palavra_chave in arquivo.stem
            testes.append(teste_palavra_chave)

        if self.extensao is not None:
            teste_extensao = self.extensao == arquivo.extensao
            testes.append(teste_extensao)

        if self.tamanho_min is not None:
            teste_tamanho_min = arquivo.tamanho >= self.tamanho_min.tobytes()
            testes.append(teste_tamanho_min)

        if self.tamanho_max is not None:
            teste_tamanho_max = arquivo.tamanho <= self.tamanho_max.tobytes()
            testes.append(teste_tamanho_max)

        return all(testes)


class Menu:
    def __init__(self, titulo:str, opcoes):
        self.titulo = titulo
        self.opcoes = opcoes


    def exibir(self):
        print('='*80)
        print(f'    {self.titulo}')
        print('=' * 80)
        for i, (texto, _) in enumerate(self.opcoes, start = 1):
            print(f'\033[32m{i}\033[m - \033[34m{texto}\033[m')
        print('='*40)


    def escolher(self):
        while True:
            try:
                opc = int(input('Selecionar opção: '))
                if 1 <= opc <= len(self.opcoes):
                    return opc
                else:
                    print('Opção inválida!')
            except ValueError:
                print('Opção inválida!')


    def executar(self):
        while True:
            self.exibir()
            escolher = self.escolher() - 1
            _, acao = self.opcoes[escolher]
            if acao is None:
                break
            acao()


def adiar_execucao(func, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)
    return wrapper


def adiar_input_dict(dic:dict, chave, valuetype:Type=None, factorymethod=None):
    def wrapper():
        while True:
            valor_str = input(f'{chave.replace('_', ' ').capitalize()}: ')
            try:
                valor_convertido = valuetype(valor_str) if factorymethod is None else factorymethod(valor_str)
                dic.update({chave: valor_convertido})
                break
            except ValueError:
                print('Entrada inválida!')
    return wrapper


def ler_caminho(prompt):
    while True:
        caminho = os.path.normpath(input(prompt).strip())
        caminho_valido = os.path.exists(caminho)
        if not caminho_valido:
            print(f'\033[31mERRO\033[m: Caminho "\033[31m{caminho}\033[m" é inválido!')
        else:
            return caminho


def pesquisar_arquivos(diretorio, filtro:Filtro = None):
    varredura = list(os.walk(diretorio))
    resultados = []

    for raiz, _, arquivos in varredura:
        for arquivo in arquivos:
            arquivo = Arquivo(str(os.path.join(raiz, arquivo)))

            if filtro is None or filtro.match(arquivo):
                resultados.append(arquivo)

    return FileGroup(resultados)


if __name__ == '__main__':

    aot = Arquivo(r'D:\arquivos_movidos\arquivo_2.txt')

    print(aot.tamanho)

    print(aot.formatar_tamanho())