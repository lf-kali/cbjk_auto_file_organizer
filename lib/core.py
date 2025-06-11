import os

import shutil

import json

from typing import Type, Callable


class FormattedSize:
    __LABELS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    __BASE = 1024

    def __init__(self, num, txt):
        if num > 0:
            self._num = num
        else:
            raise ValueError(f'"{num}" não é um numero válido.')

        if txt.upper() in FormattedSize.__LABELS:
            self._txt = txt
        else:
            raise ValueError(f'Unidade de tamanho inexistente: {txt}')

    def tobytes(self):
        for exp in range(6, 0, -1):
            idx = exp - 1
            if FormattedSize.__LABELS[idx] == self._txt:
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
    def frombytes(cls, size: int):
        for exp, label in enumerate(cls.__LABELS):
            next_size = cls.__BASE ** (exp + 1)
            if size < next_size:
                tamanho = float(size / cls.__BASE ** exp)
                return cls(round(tamanho, 2), label)

    @classmethod
    def fromstr(cls, txt: str):
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

        if label not in cls.__LABELS:
            raise ValueError(f'Unidade de tamanho inexistente: {label}')

        return cls(num, label)

    def __str__(self):
        return f'{self._num}{self._txt}'


class Arquivo:
    def __init__(self, caminho: str):
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

    def mover(self, destino: str):
        novo_caminho = os.path.join(destino, self.nome)
        shutil.move(self._caminho, novo_caminho)

    def copiar(self, destino: str):
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
    def __init__(self, group: list[Arquivo]):
        tests = [isinstance(item, Arquivo) for item in group]
        if not all(tests):
            raise TypeError
            pass
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

    def renomear_todos(self, nova_stem: str):
        for i, arquivo in enumerate(self):
            arquivo.renomear(f'{nova_stem}_{i}')


class Filtro:
    def __init__(self, *, palavra_chave: str = None, extensao: str = None, tamanho_min: str = None,
                 tamanho_max: str = None):
        self.palavra_chave = palavra_chave
        self.extensao = extensao
        try:
            self.tamanho_min = None if tamanho_min is None else FormattedSize.fromstr(tamanho_min)
        except ValueError:
            raise ValueError(f'"{tamanho_min}" não é um tamanho de arquivo válido.')
        try:
            self.tamanho_max = None if tamanho_min is None else FormattedSize.fromstr(tamanho_min)
        except ValueError:
            raise ValueError(f'"{tamanho_max}" não é um tamanho de arquivo válido')

    def match(self, arquivo: Arquivo):
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

    def to_dict(self):
        return {
            'palavra_chave':self.palavra_chave,
            'extensao': self.extensao,
            'tamanho_min': None if not self.tamanho_min else self.tamanho_min.tostr(),
            'tamanho_max': None if not self.tamanho_max else self.tamanho_max.tostr()
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)


class Menu:
    def __init__(self, titulo: str, opcoes):
        self.titulo = titulo
        self.opcoes = opcoes

    def exibir(self):
        print('=' * 80)
        print(f'    {self.titulo}')
        print('=' * 80)
        for i, (texto, _) in enumerate(self.opcoes, start=1):
            print(f'\033[32m{i}\033[m - \033[34m{texto}\033[m')
        print('=' * 40)

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


class Routine:
    def __init__(self, name, _funcs=None):
        self._name = name
        self._descritive_funcs = _funcs if _funcs else []
        self._funcs =  []
        self._results = []

    @property
    def funcs(self):
        return self._descritive_funcs

    def addfunc(self, func, *args, **kwargs):
        call = {
            'func': func.__name__,
            'args': list(args),
            'kwargs': dict(kwargs)
        }
        self._descritive_funcs.append(call)
        self.compile_funcs()

    def compile_funcs(self):

        for i, d_func in enumerate(self._descritive_funcs, start=0):
            if i < len(self._funcs):
                continue

            nomefunc = d_func['func']
            func = reg[nomefunc]

            c_args = d_func['args']
            c_kwargs = d_func['kwargs']

            self._funcs.append(adiar_execucao(func, *c_args, **c_kwargs))

    def run(self, unpack=False):
        send = []
        for func in self._funcs:
            ret = func()
            if ret is None:
                continue

            send.append(ret)

        if len(send) == 0:
            pass

        elif unpack:
            self._results.extend(send)

        else:
            self._results.append(send)

    def get_results(self):
        return self._results

    # noinspection PyTypeChecker
    def export_routine(self):
        data = {
            'name': self._name,
            'funcs': self._descritive_funcs,
        }
        with open(f'{self._name}.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def import_routine(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(name=data['name'], _funcs=data['funcs'],)


def is_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


def adiar_execucao(func, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)

    return wrapper


def adiar_input_dict(dic: dict, chave: str, valuetype: Type = None, factorymethod: Callable = None):
    # noinspection PyCallingNonCallable
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


def pesquisar_arquivos(diretorio, filtro: dict = None):
    filtro = Filtro.from_dict(filtro)
    varredura = list(os.walk(diretorio))
    resultados = []

    for raiz, _, arquivos in varredura:
        for arquivo in arquivos:
            arquivo = Arquivo(str(os.path.join(raiz, arquivo)))

            if filtro is None or filtro.match(arquivo):
                resultados.append(arquivo)

    return FileGroup(resultados)


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


reg = {
    'FormattedSize':FormattedSize,
    'Arquivo':Arquivo,
    'FileGroup':FileGroup,
    'Filtro':Filtro,
    'Menu':Menu,
    'Routine':Routine,
    'is_serializable':is_serializable,
    'adiar_execucao':adiar_execucao,
    'adiar_input_dict':adiar_input_dict,
    'ler_caminho':ler_caminho,
    'pesquisar_arquivos':pesquisar_arquivos,
    'mover_resultados':mover_resultados,
    'copiar_resultados':copiar_resultados,
    'excluir_resultados':excluir_resultados,
    'renomear_resultados':renomear_resultados,
}

#testes
if __name__ == '__main__':
    #teste de rotinas
    pesquisar_imagens = Routine('pesquisar_imagens')
    filtros_jpg = {'extensao':'.jpg'}
    filtros_png = {'extensao':'.png'}
    pesquisar_imagens.addfunc(pesquisar_arquivos,r'C:\Users\Meu Computador\Downloads', filtro=filtros_jpg)
    pesquisar_imagens.addfunc(pesquisar_arquivos,r'C:\Users\Meu Computador\Downloads', filtro=filtros_png)
    print(*pesquisar_imagens.funcs, sep='\n\n')
    #pesquisar_imagens.export_routine()
    pesquisar_imagens.run()
    ress = pesquisar_imagens.get_results()
    print(ress)


