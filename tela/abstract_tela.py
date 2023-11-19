from abc import ABC, abstractmethod
import PySimpleGUI as sg
from enum import Enum


class OpcaoBotao(Enum):
    VOLTAR = 'VOLTAR',


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        self._window = None

    def obtem_layout_titulo(self, titulo: str):
        return [
            [sg.Text('#' * 40, justification='center')],
            [sg.Text(titulo, justification='center')],
            [sg.Text('#' * 40, justification='center')],
        ]

    def obtem_layout_opcoes(self, opcoes: list):
        return [
            [sg.Button(opcao, key=index, size=15)]
            for index, opcao in enumerate(opcoes, start=1)
        ]

    def obtem_layout_lista(self, elementos: list):
        return [
            [sg.Text('-' * 70, justification='center')],
            *[[sg.Text(
                elemento,
                size=40,
                justification='center'
            )] for elemento in elementos],
            [sg.Text('-' * 70, justification='center')],
        ]

    def obtem_layout_mostra_dados(self, dados: dict):
        return [
            [sg.Text('-' * 70, justification='center')],
            *[[
                sg.Text(
                    f'{label}: ',
                    size=15,
                    justification='left',
                ),
                sg.Text(
                    dados[label],
                    size=15,
                    justification='right',
                ),
            ] for label in dados],
            [sg.Text('-' * 70, justification='center')],
        ]

    def obtem_layout_obtem_dados(self, dados: dict, label_confirmar: str):
        return [
            *[[
                sg.Text(dados[chave], size=20),
                sg.InputText(size=20, key=chave)
            ] for chave in dados],
            [
                sg.Submit(label_confirmar),
                sg.Cancel('Voltar', key=OpcaoBotao.VOLTAR)
            ]
        ]

    def obtem_opcao(self, mensagem: str, opcoes_validas: list = None) -> int:
        while True:
            try:
                opcao_escolhida = int(input(mensagem))
                if opcoes_validas and opcao_escolhida not in opcoes_validas:
                    raise ValueError
                return opcao_escolhida
            except ValueError:
                print('Selecione uma opção válida!')
                if opcoes_validas:
                    print('Opções válidas:', opcoes_validas)

    def mostra_opcoes(self, opcoes: list):
        for index, opcao in enumerate(opcoes, start=1):
            print(f'{index} - {opcao}')

    def obtem_informacao(self, mensagem: str) -> str:
        informacao = input(mensagem)
        return informacao

    def confirma_acao(self, mensagem: str) -> bool:
        confirmacao = input(f'{mensagem} [S/n] ')
        return confirmacao.lower() != 'n'

    def mostra_titulo(self, titulo: str):
        print('#' * 35)
        print(titulo)
        print('#' * 35)

    def mostra_mensagem(self, mensagem: str):
        sg.Popup(mensagem, title='Batalha Naval')

    def open(self):
        botao, valores = self._window.Read()
        return botao, valores

    def close(self):
        self._window.Close()
