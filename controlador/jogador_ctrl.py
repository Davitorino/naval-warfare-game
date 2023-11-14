from tela.jogador_tela import JogadorTela
from dao.jogador_dao import JogadorDAO
from entidade.jogador import Jogador
from exception.nao_encontrado_error import NaoEncontradoErro


class JogadorCtrl:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__jogador_tela = JogadorTela()
        self.__jogador_dao = JogadorDAO()
        self.__proximo_id = self.obter_proximo_id()

    @property
    def jogadores(self) -> list:
        return self.__jogador_dao.get_all()

    def obter_proximo_id(self):
        ids = [jogador.id for jogador in self.jogadores]
        return max(ids) + 1

    def obter_jogador_por_id(self, id_jogador: int) -> Jogador:
        try:
            return self.__jogador_dao.get(id_jogador)
        except NaoEncontradoErro as e:
            self.__jogador_tela.mostra_mensagem(e)


    def logar_jogador(self) -> Jogador:
        usuario, senha = self.__jogador_tela.mostra_login_jogador()
        for jogador in self.jogadores:
            if usuario == jogador.usuario and \
                    senha == jogador.senha:
                return jogador
        self.__jogador_tela.mostra_mensagem('Usuário ou senha incorretos.')

    def mostrar_jogador(self):
        id_jogador = self.__jogador_tela.obtem_id_jogador()
        jogador = self.obter_jogador_por_id(id_jogador)
        if jogador:
            self.__jogador_tela.mostra_perfil_jogador(jogador.id,
                                                      jogador.nome,
                                                      jogador.data_nascimento,
                                                      jogador.usuario,
                                                      jogador.pontuacao_total)
            opcoes_acoes = {
                1: self.mostrar_historico_jogos,
                2: self.__controlador_principal.iniciar_app,
            }
            while True:
                opcao_escolhida = self.__jogador_tela.mostra_menu_perfil()
                if opcao_escolhida == 1:
                    opcoes_acoes[opcao_escolhida](jogador)
                else:
                    opcoes_acoes[opcao_escolhida]()

    def mostrar_jogador_logado(self):
        jogador = self.__controlador_principal.jogador_logado
        jogador_tela = self.__jogador_tela
        if jogador:
            opcoes_acoes = {
                1: self.mostrar_historico_jogos_logado,
                2: self.editar_jogador,
                3: self.excluir_jogador,
                4: self.__controlador_principal.iniciar_app,
            }
            while True:
                jogador_tela.mostra_perfil_jogador(jogador.id,
                                                   jogador.nome,
                                                   jogador.data_nascimento,
                                                   jogador.usuario,
                                                   jogador.pontuacao_total)
                opcao_escolhida = jogador_tela.mostra_menu_perfil_logado()
                opcoes_acoes[opcao_escolhida]()

    def tratar_usario(self) -> str:
        jogador_logado = self.__controlador_principal.jogador_logado
        usuarios = [jogador.usuario for jogador in self.jogadores]
        while True:
            usuario = self.__jogador_tela.obtem_informacao(
                'Digite seu usuário: ').strip()
            if usuario not in usuarios or \
                    (jogador_logado and jogador_logado.usuario == usuario):
                return usuario
            else:
                self.__jogador_tela.mostra_mensagem(
                    'Nome de usuário já está em uso...')

    def tratar_data_nascimento(self) -> str:
        while True:
            try:
                dia, mes, ano = self.__jogador_tela.obtem_informacao(
                    f'Digite sua data de nascimento '
                    f'separada por espaços (ex: 01 01 2000): ').split()
                dia = int(dia)
                mes = int(mes)
                ano = int(ano)
                if not (0 < dia < 32) or not (0 < mes < 13) or\
                        not (ano > 0):
                    raise ValueError
                return f'{dia}/{mes}/{ano}'
            except ValueError:
                self.__jogador_tela.mostra_mensagem(
                    'Data de nascimento inválida!')

    def obter_informacoes_jogador(self) -> tuple:
        nome = self.__jogador_tela.obtem_informacao(
            'Digite seu nome: ')
        data_nascimento = self.tratar_data_nascimento()
        usuario = self.tratar_usario()
        senha = self.__jogador_tela.obtem_informacao(
            'Digite sua senha: ').strip()
        return nome, data_nascimento, usuario, senha

    def cadastrar_jogador(self) -> Jogador:
        self.__jogador_tela.mostra_titulo('CADASTRANDO JOGADOR')
        nome, data_nasc, usuario, senha = self.obter_informacoes_jogador()
        novo_jogador = Jogador(self.__proximo_id, nome, data_nasc,
                               usuario, senha)
        self.__jogador_dao.add(novo_jogador)
        self.__proximo_id += 1
        return novo_jogador

    def excluir_jogador(self):
        self.__jogador_tela.mostra_mensagem('** Ao excluir sua conta, os '
                                            'registros dos seus jogos serão '
                                            'perdidos! **')
        confirmacao = self.__jogador_tela.confirma_acao(
            'Tem certeza que deseja excluir sua conta?'
        )
        if confirmacao:
            jogador_logado = self.__controlador_principal.jogador_logado
            for jogo in jogador_logado.jogos:
                self.__controlador_principal.jogo_ctrl.remover_jogo(jogo)
            self.__jogador_dao.remove(jogador_logado)
            self.__jogador_tela.mostra_mensagem(
                'Jogador excluído com sucesso!'
            )
            self.__controlador_principal.logout()

    def editar_jogador(self):
        self.__jogador_tela.mostra_titulo('EDITANDO JOGADOR')
        nome, data_nasc, usuario, senha = self.obter_informacoes_jogador()
        jogador_logado = self.__controlador_principal.jogador_logado
        jogador_logado.nome = nome
        jogador_logado.data_nascimento = data_nasc
        jogador_logado.usuario = usuario
        jogador_logado.senha = senha

    def mostrar_historico_jogos_logado(self):
        jogador = self.__controlador_principal.jogador_logado
        self.mostrar_historico_jogos(jogador)

    def mostrar_historico_jogos(self, jogador: Jogador):
        self.__jogador_tela.mostra_historico_jogos(jogador.jogos)
        opcoes_acoes = {
            1: self.__controlador_principal.jogo_ctrl.mostrar_relatorio_jogo,
            2: self.__controlador_principal.iniciar_app
        }
        while True:
            opcao_escolhida = self.__jogador_tela.mostra_menu_historico_jogo()
            opcoes_acoes[opcao_escolhida]()
