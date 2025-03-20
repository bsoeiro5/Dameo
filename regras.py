class RegrasDameo:
    def __init__(self, tabuleiro):
        """
        Inicializa as regras com o tabuleiro fornecido.
        :param tabuleiro: Instância do tabuleiro do jogo.
        """
        self.tabuleiro = tabuleiro

    def movimento_valido(self, pos_inicial, pos_final):
        """
        Verifica se um movimento é válido.
        :param pos_inicial: Tupla (linha, coluna) da posição inicial.
        :param pos_final: Tupla (linha, coluna) da posição final.
        :return: True se o movimento for válido, False caso contrário.
        """
        if not self.tabuleiro.posicao_valida(pos_inicial) or not self.tabuleiro.posicao_valida(pos_final):
            return False

        peca = self.tabuleiro.obter_peca(pos_inicial)
        if peca is None:
            return False

        if self.tabuleiro.obter_peca(pos_final) is not None:
            return False  # Não pode mover para um espaço ocupado

        if peca.tipo == "homem":
            # Movimento linear para frente
            if not self.movimento_linear_valido(pos_inicial, pos_final):
                return False
        elif peca.tipo == "rei":
            # Movimento queenwise
            if not self.movimento_queenwise_valido(pos_inicial, pos_final):
                return False

        return True

    def movimento_linear_valido(self, pos_inicial, pos_final):
        """
        Verifica se um movimento linear é válido.
        :param pos_inicial: Tupla (linha, coluna) da posição inicial.
        :param pos_final: Tupla (linha, coluna) da posição final.
        :return: True se o movimento linear for válido, False caso contrário.
        """
        linha_inicial, coluna_inicial = pos_inicial
        linha_final, coluna_final = pos_final

        # Movimento deve ser para frente e em linha reta
        if linha_final <= linha_inicial or coluna_inicial != coluna_final:
            return False

        # Verifica se todas as posições intermediárias estão ocupadas pela mesma cor
        for linha in range(linha_inicial + 1, linha_final):
            peca_intermediaria = self.tabuleiro.obter_peca((linha, coluna_inicial))
            if peca_intermediaria is None or peca_intermediaria.cor != self.tabuleiro.obter_peca(pos_inicial).cor:
                return False

        return True

    def movimento_queenwise_valido(self, pos_inicial, pos_final):
        """
        Verifica se um movimento queenwise é válido para um rei.
        :param pos_inicial: Tupla (linha, coluna) da posição inicial.
        :param pos_final: Tupla (linha, coluna) da posição final.
        :return: True se o movimento queenwise for válido, False caso contrário.
        """
        linha_inicial, coluna_inicial = pos_inicial
        linha_final, coluna_final = pos_final

        # Movimento deve ser em linha reta ou diagonal
        if abs(linha_final - linha_inicial) != abs(coluna_final - coluna_inicial) and linha_inicial != linha_final and coluna_inicial != coluna_final:
            return False

        # Verifica se todas as posições intermediárias estão vazias
        delta_linha = 1 if linha_final > linha_inicial else -1
        delta_coluna = 1 if coluna_final > coluna_inicial else -1

        linha, coluna = linha_inicial + delta_linha, coluna_inicial + delta_coluna
        while (linha, coluna) != (linha_final, coluna_final):
            if self.tabuleiro.obter_peca((linha, coluna)) is not None:
                return False
            linha += delta_linha
            coluna += delta_coluna

        return True

    def captura_valida(self, pos_inicial, pos_final):
        """
        Verifica se uma captura é válida.
        :param pos_inicial: Tupla (linha, coluna) da posição inicial.
        :param pos_final: Tupla (linha, coluna) da posição final.
        :return: True se a captura for válida, False caso contrário.
        """
        if not self.tabuleiro.posicao_valida(pos_inicial) or not self.tabuleiro.posicao_valida(pos_final):
            return False

        peca = self.tabuleiro.obter_peca(pos_inicial)
        if peca is None:
            return False

        if self.tabuleiro.obter_peca(pos_final) is not None:
            return False  # A posição final deve estar vazia

        pos_intermediaria = self.tabuleiro.posicao_intermediaria(pos_inicial, pos_final)
        peca_intermediaria = self.tabuleiro.obter_peca(pos_intermediaria)

        if peca_intermediaria is None or peca_intermediaria.cor == peca.cor:
            return False  # A peça adversária deve ser saltada

        # Verifica se a captura é válida para homens ou reis
        if peca.tipo == "homem":
            if not self.captura_homem_valida(pos_inicial, pos_final, pos_intermediaria):
                return False
        elif peca.tipo == "rei":
            if not self.captura_rei_valida(pos_inicial, pos_final, pos_intermediaria):
                return False

        return True

    def captura_homem_valida(self, pos_inicial, pos_final, pos_intermediaria):
        """
        Verifica se uma captura é válida para um homem.
        """
        linha_inicial, coluna_inicial = pos_inicial
        linha_final, coluna_final = pos_final

        # Captura deve ser em linha reta (frente, trás ou lado)
        if linha_inicial != linha_final and coluna_inicial != coluna_final:
            return False

        return True

    def captura_rei_valida(self, pos_inicial, pos_final, pos_intermediaria):
        """
        Verifica se uma captura é válida para um rei.
        """
        linha_inicial, coluna_inicial = pos_inicial
        linha_final, coluna_final = pos_final

        # Captura deve ser rookwise (linha reta)
        if linha_inicial != linha_final and coluna_inicial != coluna_final:
            return False

        return True