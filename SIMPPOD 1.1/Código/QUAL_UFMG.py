# -*- coding: utf-8 -*-
# Modulo: QUAL_UFMG

"""
Neste modulo, esta a classe principal do modelo de qualidade de agua (QUAL-UFMG).
A classe conta com dois metodos: um para construir os parametros iniciais a partir
dos arquivos de entrada, e outro para executar o metodo de Euler, resolvendo as EDO's
do modelo
"""

# Importacao de bibliotecas
from SCS import SCS
from Euler import Euler
from Leitura import *
from Rio import Rio

# Definicao da classe
class QUAL_UFMG(object):

    # METODOS

    @staticmethod
    def constroi_param_ini(arquivo, simula_difusa):
        # Cria a matriz de contribuicoes
        [matriz_contribuicoes, matriz_reducoes, matriz_tipo_contribuicoes] = ler_entrada_pontual(arquivo)

        # Cria o vetor de constantes
        const = ler_entrada_constantes(arquivo)
        # const = [tam_rio, tam_cel, classe, T, Altitude, Ph, DBOr, ODr, NORGr, NAMONr, NNITRIr, NNITRAr, PORGr, PINORGr, COLr, Qr, Ro2a,
        #          Ks, K1, Kb, Koa, Kan, Koi, Kspo, Samon, Kso, Knn, Ro2n, Knitr, Sinorg, a_vel, b_vel, a_prof, b_prg, DBOinc, ODinc, NORGinc,
        #          NAMONinc, NNITRIinc, NNITRAinc, PORGinc, PINORGinc, COLinc, Qinc, Sd, Lrd, NT]

        # Cria o rio
        rio = Rio(const[0], const[1], const[2], const[3], const[4], const[5], const[6], const[7], const[8], const[9],
                  const[10], const[11], const[12], const[13], const[14], const[15], const[16], const[17], const[18],
                  const[19], const[20], const[21], const[22], const[23], const[24], const[25], const[26], const[27],
                  const[28], const[29], const[30], const[31], const[32], const[33], const[34], const[35], const[36],
                  const[37], const[38], const[39], const[40], const[41], const[42], const[43], const[44], const[45], const[46])

        # Correcao das constantes do rio de acordo com a temperatura
        if simula_difusa:
            scs = SCS(arquivo)
        else:
            scs = []

        return [rio, matriz_contribuicoes, matriz_reducoes, scs, const[0], const[1], const[5], matriz_tipo_contribuicoes]

    @staticmethod
    def aplica_reducoes(matriz_contribuicoes, matriz_reducao_pontual, numFuncao):
        j = 0
        i = 0
        matriz_contribuicoes_otimizada = []
        while i < len(matriz_contribuicoes): # and j < len(matriz_reducao_pontual[1]):
            # Se N em matriz_contribuicoes = N em matriz_reducao_pontual
            if j < len(matriz_reducao_pontual[1]) and matriz_contribuicoes[i][10] == matriz_reducao_pontual[1][j]:
                novo_vetor = matriz_contribuicoes[i].copy()  # novo_vetor = i-esima linha da Entrada_Pontual.txt
                if numFuncao == 1:
                    novo_vetor[0] = matriz_contribuicoes[i][0] * (1 - matriz_reducao_pontual[0][j])
                    # nova DBO5e = DBO5e * (1 - alelo)
                elif numFuncao == 2:
                    novo_vetor[3] = matriz_contribuicoes[i][3] * (1 - matriz_reducao_pontual[0][j])
                    # nova Namon = Namon * (1 - alelo)
                elif numFuncao == 3:
                    novo_vetor[0] = matriz_contribuicoes[i][0] * (1 - matriz_reducao_pontual[0][j][0])
                    # nova DBO5e = DBO5e * (1 - alelo)
                    novo_vetor[3] = matriz_contribuicoes[i][3] * (1 - matriz_reducao_pontual[0][j][1])
                    # nova Namon = Namon * (1 - alelo)
                if numFuncao == 4:
                    novo_vetor[8] = matriz_contribuicoes[i][8] * (1 - matriz_reducao_pontual[0][j])
                    # nova COL = COL * (1 - alelo)
                elif type(matriz_reducao_pontual[0][0]) is list:
                    novo_vetor[0] = matriz_contribuicoes[i][0] * (1 - matriz_reducao_pontual[0][j][0])
                    # nova DBO5e = DBO5e * (1 - alelo)
                elif numFuncao >= 5:
                    novo_vetor[0] = matriz_contribuicoes[i][0] * (1 - matriz_reducao_pontual[0][j])
                    # nova DBO5e = DBO5e * (1 - alelo)

                matriz_contribuicoes_otimizada.append(novo_vetor)  # Adiciona valor da DBO5e calculada
                j += 1
                i += 1
            else:
                matriz_contribuicoes_otimizada.append(matriz_contribuicoes[i])  # Adiciona a i-esima linha da Entrada_Pontual.txt
                i += 1

        return matriz_contribuicoes_otimizada

    def executa(self, Rio, matriz_contribuicoes, matriz_reducao_pontual, simula_difusa, matriz_reducao_difusa, scs, numFuncaoP, matriz_tipo_contribuicoes, tributarios, celula_entrada_tributarios):
        euler = Euler()

        if simula_difusa:
            [matriz_difusa, sub_bacias, matriz_cargas] = scs.executa(matriz_reducao_difusa)

            if matriz_reducao_pontual[0]:
                matriz_contribuicoes_otimizada_tributario = self.aplica_reducoes(matriz_contribuicoes, matriz_reducao_pontual, numFuncaoP)
                matriz_final = Rio.Concatena_matrizes(matriz_difusa, matriz_contribuicoes_otimizada_tributario)
            else:
                matriz_final = Rio.Concatena_matrizes(matriz_difusa, matriz_contribuicoes)

            cenario = euler.Calcula(Rio, matriz_final, matriz_tipo_contribuicoes, simula_difusa, tributarios, celula_entrada_tributarios)
            cenario.sub_bacias = sub_bacias
            cenario.matriz_cargas = matriz_cargas

        else:
            if matriz_reducao_pontual[0]:
                matriz_contribuicoes_otimizada_tributario = self.aplica_reducoes(matriz_contribuicoes, matriz_reducao_pontual, numFuncaoP)
                cenario = euler.Calcula(Rio, matriz_contribuicoes_otimizada_tributario, matriz_tipo_contribuicoes, simula_difusa, tributarios, celula_entrada_tributarios)
            else:
                cenario = euler.Calcula(Rio, matriz_contribuicoes, matriz_tipo_contribuicoes, simula_difusa, tributarios, celula_entrada_tributarios)

        for i in range(len(cenario.Y_Coliformes)): cenario.Y_Coliformes[i] = cenario.Y_Coliformes[i]/10

        return cenario
