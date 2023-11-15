from dao.dao import DAO
from entidade.jogador import Jogador
from exception.nao_encontrado_error import NaoEncontradoErro


class JogadorDAO(DAO):
    def __init__(self):
        super().__init__('jogador.pkl')

    def add(self, jogador: Jogador):
        if isinstance(jogador, Jogador) and isinstance(jogador.id, int):
            super().add(jogador.id, jogador)

    def get(self, id_jogador: int):
        try:
            if isinstance(id_jogador, int):
                return super().get(id_jogador)
        except KeyError:
            raise NaoEncontradoErro('jogador')

    def remove(self, jogador: Jogador):
        try:
            if isinstance(jogador, Jogador) and isinstance(jogador.id, int):
                super().remove(jogador.id)
        except KeyError:
            raise NaoEncontradoErro('jogador')
