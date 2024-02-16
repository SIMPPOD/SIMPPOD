# -*- coding: utf-8 -*-
# Modulo: Euler

""" Nesse modulo, temos a implementacao proposta da classe que resolve
o metodo de Euler para a resolucao de um sistema de equacoes
diferenciais ordinarias e de primeira ordem. """

from math import exp
from Cenario import Cenario
from Constantes import Constantes

# Definicao da classe
class Euler(object):

    @staticmethod
    def existe_nova_contribuicao(j, i, matriz_contribuicoes):
        if j + 1 <= len(matriz_contribuicoes):
            if matriz_contribuicoes[j][10] == i:  # Se N == i
                return True
            else:
                return False
        else:
            return False
        
    @staticmethod
    def junta_matriz_contribuicoes(matriz_contribuicoes, tributarios, celula_entrada_tributario):
        for i in range(len(tributarios)):
            tributario = [tributarios[i].Y_DBO[-1], tributarios[i].Y_OD[-1], tributarios[i].Y_Norg[-1], tributarios[i].Y_Namon[-1], tributarios[i].Y_Nnitri[-1], tributarios[i].Y_Nnitra[-1], tributarios[i].Y_Porg[-1], tributarios[i].Y_Pinorg[-1], tributarios[i].Y_Coliformes[-1], tributarios[i].PerfilQ[-1], celula_entrada_tributario[i], 0, 0, 0, 0, "T"]
            matriz_contribuicoes.append(tributario)
        celulas_entrada = []
        for i in range(len(matriz_contribuicoes)):
            celulas_entrada.append(matriz_contribuicoes[i][11])
        celulas_entrada.sort()
        return celulas_entrada
        
    @staticmethod
    def ordena_matriz_contribuicoes(matriz_contribuicoes, tributarios, celula_entrada_tributario, matriz_tipo_contribuicoes):
        aux = matriz_contribuicoes.copy()
        for i in range(len(tributarios)):
            tributario = [tributarios[i].Y_DBO[-1], tributarios[i].Y_OD[-1], tributarios[i].Y_Norg[-1], tributarios[i].Y_Namon[-1], tributarios[i].Y_Nnitri[-1], tributarios[i].Y_Nnitra[-1], tributarios[i].Y_Porg[-1], tributarios[i].Y_Pinorg[-1], tributarios[i].Y_Coliformes[-1], tributarios[i].PerfilQ[-1], celula_entrada_tributario[i], 0, 0, 0, 0, "T"]
            aux.append(tributario)
            matriz_tipo_contribuicoes.append("T")

        celulas_entrada = []
        for i in range(len(aux)):
            celulas_entrada.append(aux[i][10])
        celulas_entrada.sort()

        matriz_contribuicoes_ordenada = []
        matriz_tipo_contribuicoes_ordenada = []
        for i in range(len(celulas_entrada)):
            for j in range(len(aux)):
                if aux[j][10] == celulas_entrada[i]:
                    matriz_contribuicoes_ordenada.append(aux[j])
                    matriz_tipo_contribuicoes_ordenada.append(aux[j][-1])
        return [matriz_contribuicoes_ordenada, matriz_tipo_contribuicoes_ordenada, celulas_entrada]

    # Metodo que faz o calculo do metodo de Euler, considerando tanto novas contribuicoes quanto novas reducoes
    def Calcula(self, curso, simulacao_curso, Rio, matriz_contribuicoes, matriz_tipo_contribuicoes, simula_difusa, celula_entrada_tributarios):
        num_cel = Rio.tam_rio / Rio.tam_cel
        num_cel = int(num_cel)

        # Setando os parametros iniciais na celula 0
        perfilK2 = [0]
        perfilKd = [0]
        perfilQ = [Rio.Qr]
        perfilV = [0]
        perfilH = [0]
        perfilTempo = [0]
        prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (Rio.T + 273.2))) - Rio.PH))
        Amonia_livre = [Rio.NAMONr*prop]
        Amonia_ionizada = [Rio.NAMONr*(1-prop)]
        ODsat = (1-Rio.Alt/9450) * (14.652 - (0.41022 * Rio.T) + (0.007991 * (Rio.T ** 2)) - (0.000077774 * (Rio.T ** 3)))
        
        Mistura_DBO = [Rio.DBO5r]
        Mistura_OD = [ODsat]
        Mistura_NORG = [Rio.NORGr]
        Mistura_NAMON = [Rio.NAMONr]
        Mistura_NNITRI = [Rio.NNITRIr]
        Mistura_NNITRA = [Rio.NNITRAr]
        Mistura_PORG = [Rio.PORGr]
        Mistura_PINORG = [Rio.PINORGr]
        Mistura_COL = [Rio.COLr] # em L
    
        Modelagem_DBO = [Rio.DBO5r]
        Modelagem_OD = [ODsat]
        Modelagem_Norg = [Rio.NORGr]
        Modelagem_Namon = [Rio.NAMONr]
        Modelagem_Nnitri = [Rio.NNITRIr]
        Modelagem_Nnitra = [Rio.NNITRAr]
        Modelagem_Porg = [Rio.PORGr]
        Modelagem_Pinorg = [Rio.PINORGr]
        Modelagem_COL = [Rio.COLr] # em L

        Q = Rio.Qr
        v = Rio.a_vel*(Q**Rio.b_vel)
        H = Rio.a_prof*(Q**Rio.b_prof)

        Const = Constantes(Rio.K1, Rio.Ks, Rio.Koa, Rio.Kan, Rio.Knn, Rio.Kspo, Rio.Koi, Rio.Kso, Rio.Kt, Rio.Kb, Rio.Samon, Rio.Sd, Rio.Lrd, Rio.Sinorg)
        Const.set_constantes(1.047, 1.024, 1.024, 1.047, 1.080, 1.047, 1.024, 1.047, 1.024, 1.047, 1.074, 1.060, 1.074, 1.07, Rio.T, Rio.Qr, H, v)
        
        matriz_contribuicoes = [linha[:-1] for linha in matriz_contribuicoes]
        if curso[1]:
            tributarios = []
            for i in range(len(curso[1])):
                if not int(curso[1][i][49]): tributarios.append(simulacao_curso[int(curso[1][i][47])])
            [matriz_contribuicoes, matriz_tipo_contribuicoes, celula_entrada_tributarios] = self.ordena_matriz_contribuicoes(matriz_contribuicoes, tributarios, celula_entrada_tributarios, matriz_tipo_contribuicoes)
        j = 0
        for i in range(1, num_cel+1):
            if Mistura_OD[i-1] <= 0: fnitr = 0.00001
            else: fnitr = 1 - (exp(-Rio.Knitr*Mistura_OD[i-1]))
            if self.existe_nova_contribuicao(j, i, matriz_contribuicoes):
                Mistura_DBO.append(Rio.eq_mistura_DBO(Modelagem_DBO[i-1], matriz_contribuicoes[j][0], Q, matriz_contribuicoes[j][9]))
                Mistura_OD.append(Rio.eq_mistura_OD(Modelagem_OD[i-1], matriz_contribuicoes[j][1], Q, matriz_contribuicoes[j][9]))
                Mistura_NORG.append(Rio.eq_mistura_Norg(Modelagem_Norg[i-1], matriz_contribuicoes[j][2], Q, matriz_contribuicoes[j][9]))
                Mistura_NAMON.append(Rio.eq_mistura_Namon(Modelagem_Namon[i-1], matriz_contribuicoes[j][3], Q, matriz_contribuicoes[j][9]))
                Mistura_NNITRI.append(Rio.eq_mistura_Nnitri(Modelagem_Nnitri[i-1], matriz_contribuicoes[j][4], Q, matriz_contribuicoes[j][9]))
                Mistura_NNITRA.append(Rio.eq_mistura_Nnitra(Modelagem_Nnitra[i-1], matriz_contribuicoes[j][5], Q, matriz_contribuicoes[j][9]))
                Mistura_PORG.append(Rio.eq_mistura_Porg(Modelagem_Porg[i-1], matriz_contribuicoes[j][6], Q, matriz_contribuicoes[j][9]))
                Mistura_PINORG.append(Rio.eq_mistura_Pinorg(Modelagem_Pinorg[i-1], matriz_contribuicoes[j][7], Q, matriz_contribuicoes[j][9]))
                Mistura_COL.append(Rio.eq_mistura_Coliformes(Modelagem_COL[i-1], matriz_contribuicoes[j][8]*10, Q, matriz_contribuicoes[j][9]))  # passa COLe para L 
                                 
                if simula_difusa:
                    Q += matriz_contribuicoes[j][9] + Rio.Qinc  # Q = Q + Qe + Qinc
                else: 
                    if matriz_tipo_contribuicoes[j] != "C":
                        Q += matriz_contribuicoes[j][9] + Rio.Qinc  # Q = Q + Qe + Qinc
                    else:
                        Q = Q - matriz_contribuicoes[j][9] + Rio.Qinc  # Q = Q - Qe + Qinc
                
                j += 1

            else:
                Mistura_DBO.append(Rio.eq_mistura_DBO(Modelagem_DBO[i-1], 0, Q, 0))
                Mistura_OD.append(Rio.eq_mistura_OD(Modelagem_OD[i-1], 0, Q, 0))
                Mistura_NORG.append(Rio.eq_mistura_Norg(Modelagem_Norg[i-1], 0, Q, 0))
                Mistura_NAMON.append(Rio.eq_mistura_Namon(Modelagem_Namon[i-1], 0, Q, 0))
                Mistura_NNITRI.append(Rio.eq_mistura_Nnitri(Modelagem_Nnitri[i-1], 0, Q, 0))
                Mistura_NNITRA.append(Rio.eq_mistura_Nnitra(Modelagem_Nnitra[i-1], 0, Q, 0))
                Mistura_PORG.append(Rio.eq_mistura_Porg(Modelagem_Porg[i-1], 0, Q, 0))
                Mistura_PINORG.append(Rio.eq_mistura_Pinorg(Modelagem_Pinorg[i-1], 0, Q, 0))
                Mistura_COL.append(Rio.eq_mistura_Coliformes(Modelagem_COL[i-1], 0, Q, 0))  # em L

                Q = Q + Rio.Qinc

            v = Rio.a_vel*(Q**Rio.b_vel)
            H = Rio.a_prof*(Q**Rio.b_prof)
            b = Q/(v*H)
            tempo = Rio.tam_cel / (v*24*3600)
            prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (Rio.T + 273.2))) - Rio.PH))
            Amonia_livre.append(Mistura_NAMON[i]*prop)
            Amonia_ionizada.append(Mistura_NAMON[i]*(1-prop))

            Const.Kd = Const.set_Kd(Q, H, 1.047, Const.K1, Rio.T)
            Const.Kt = Const.set_Kt(Const.K1)
            Const.K2 = Const.set_K2(Q, 1.024, Rio.T, H, v)
            Const.Spinorg = Const.corrige_Spinorg(Rio.Sinorg, 1.074, Rio.T, 20, H)
            Const.Samon = Const.corrige_Samon(Rio.Samon, 1.074, Rio.T, 20, H)
            Const.Sd = Const.corrige_Sd(Rio.Sd, 1.060, Rio.T, 20, H)
            
            perfilK2.append(Const.K2)
            perfilKd.append(Const.Kd)
            perfilQ.append(Q)
            perfilV.append(v)
            perfilH.append(H)
            perfilTempo.append(tempo)
            
            modelagem_DBO = Mistura_DBO[i] + tempo * ((-Const.Kd-Const.Ks)*Mistura_DBO[i] + Const.Lrd/(b*H))
            if modelagem_DBO >= 0: Modelagem_DBO.append(modelagem_DBO)
            else: Modelagem_DBO.append(0)
            
            Modelagem_Norg.append(Mistura_NORG[i] + tempo * ((-Const.Koa-Const.Kso)*Mistura_NORG[i]))
            Modelagem_Namon.append(Mistura_NAMON[i] + tempo * (Const.Koa*Mistura_NORG[i] - fnitr*Const.Kan*Mistura_NAMON[i] + Const.Samon/H))
            Modelagem_Nnitri.append(Mistura_NNITRI[i] + tempo * (fnitr*Const.Kan*Mistura_NAMON[i] - fnitr*Const.Knn*Mistura_NNITRI[i]))
            Modelagem_Nnitra.append(Mistura_NNITRA[i] + tempo * (fnitr*Const.Knn*Mistura_NNITRI[i]))

            modelagem_od = Mistura_OD[i] + tempo * (Const.K2*(ODsat - Mistura_OD[i]) - Const.Kd*Mistura_DBO[i]*Const.Kt - Rio.Ro2a*Mistura_NAMON[i]*Const.Kan*fnitr - Rio.Ro2n*Mistura_NNITRI[i]*Const.Knn*fnitr - Const.Sd)
            if modelagem_od <= ODsat: 
                if modelagem_od >= 0: Modelagem_OD.append(modelagem_od)
                else: Modelagem_OD.append(0)
            else: Modelagem_OD.append(ODsat)            
            
            Modelagem_Porg.append(Mistura_PORG[i] - tempo * (Mistura_PORG[i]*(Const.Koi + Const.Kspo))) 
            Modelagem_Pinorg.append(Mistura_PINORG[i] + tempo * (Const.Koi*Mistura_PORG[i] + Const.Spinorg/H))

            modelagem_col = Mistura_COL[i] - tempo * (Mistura_COL[i]*Const.Kb)
            if modelagem_col >= 0: Modelagem_COL.append(modelagem_col)  # em L
            else: Modelagem_COL.append(0)

        Amonia = [Amonia_livre, Amonia_ionizada]
        cenario = Cenario(Modelagem_DBO, Modelagem_OD, Modelagem_Norg, Modelagem_Namon, Modelagem_Nnitri, Modelagem_Nnitra, Modelagem_Porg, Modelagem_Pinorg, Modelagem_COL, Amonia, perfilK2, perfilKd, perfilQ, perfilV, perfilH, perfilTempo, matriz_contribuicoes)

        return cenario