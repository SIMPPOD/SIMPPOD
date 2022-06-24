# -*- coding: utf-8 -*-
# Modulo: Euler

""" Nesse modulo, temos a implementacao proposta da classe que resolve
o metodo de Euler para a resolucao de um sistema de equacoes
diferenciais ordinarias e de primeira ordem. Tambem esta nesse arquivo
a funcao que faz a avaliacao da funcao F que e fixa """

# Importacao de bibliotecas
from math import exp
from Cenario import Cenario
from Constantes import Constantes
import numpy as np

# Definicao da classe
class Euler(object):

    # METODOS

    # Metodo que verifica se, no passo atual do Euler, existe uma nova contribuicao
    @staticmethod
    def existe_nova_contribuicao(j, i, matriz_contribuicoes):
        if j + 1 <= len(matriz_contribuicoes):
            if matriz_contribuicoes[j][9] == i:  # Se N == i
                return True
            else:
                return False
        else:
            return False

    # Metodo que faz o calculo do metodo de Euler, considerando tanto novas contribuicoes quanto novas reducoes
    def Calcula(self, Rio, matriz_contribuicoes, Cs, matriz_tipo_contribuicoes, simula_difusa):
        # Setando os parametros iniciais
        j = 0

        Q = Rio.Qr
        T = Rio.T
        v = Rio.a_vel*(Q**Rio.b_vel)
        H = Rio.a_prof*(Q**Rio.b_prof)
        prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (T + 273.2))) - Rio.PH))
        Amonia_livre = [Rio.NAMONr*prop]
        Amonia_ionizada = [Rio.NAMONr*(1-prop)]

        Const = Constantes(Rio.K1, Rio.K2, Rio.Ks, Rio.Koa, Rio.Kan, Rio.Knn, Rio.Kspo, Rio.Koi, Rio.Kso, Rio.Kt, Rio.Samon, Rio.Sd, Rio.Lrd)
        Const.set_constantes(1.024, 1.047, 1.024, 1.047, 1.080, 1.024, 1.047, 1.024, 1.047, T, Q, H, v, Rio, 1.074, 1.060, Cs)
        
        perfilK2 = [Const.K2]
        perfilKd = [Const.Kd]
        perfilCs = [Const.Cs]
        perfilQ = [Q]
        perfilV = [v]
        perfilH = [H]
        perfilTempo = [0]
        
        yi_DBO = Rio.DBO5r
        yi_OD = Rio.ODr
        yi_Norg = Rio.NORGr
        yi_Namon = Rio.NAMONr
        yi_Nnitri = Rio.NNITRIr
        yi_Nnitra = Rio.NNITRAr
        yi_Porg = Rio.PORGr
        yi_Pinorg = Rio.PINORGr             
        
        if matriz_contribuicoes[0][9] == 0:
            yi_DBO = Rio.eq_mistura_DBO(yi_DBO, matriz_contribuicoes[0][0], Q, matriz_contribuicoes[0][8])
            yi_OD = Rio.eq_mistura_OD(yi_OD, matriz_contribuicoes[0][1], Q, matriz_contribuicoes[0][8])
            yi_Norg = Rio.eq_mistura_Norg(yi_Norg, matriz_contribuicoes[0][2], Q, matriz_contribuicoes[0][8])
            yi_Namon = Rio.eq_mistura_Namon(yi_Namon, matriz_contribuicoes[0][3], Q, matriz_contribuicoes[0][8])
            yi_Nnitri = Rio.eq_mistura_Nnitri(yi_Nnitri, matriz_contribuicoes[0][4], Q, matriz_contribuicoes[0][8])
            yi_Nnitra = Rio.eq_mistura_Nnitra(yi_Nnitra, matriz_contribuicoes[0][5], Q, matriz_contribuicoes[0][8])
            yi_Porg = Rio.eq_mistura_Porg(yi_Porg, matriz_contribuicoes[0][6], Q, matriz_contribuicoes[0][8])
            yi_Pinorg = Rio.eq_mistura_Pinorg(yi_Pinorg, matriz_contribuicoes[0][7], Q, matriz_contribuicoes[0][8])

            j = j + 1
    
        Y_DBO = [yi_DBO]
        Y_OD = [yi_OD]
        Y_Norg = [yi_Norg]
        Y_Namon = [yi_Namon]
        Y_Nnitri = [yi_Nnitri]
        Y_Nnitra = [yi_Nnitra]
        Y_Porg = [yi_Porg]
        Y_Pinorg = [yi_Pinorg]
        
        num_cel = Rio.tam_rio / Rio.tam_cel
        num_cel = int(num_cel)

        for i in range(1, num_cel):
            fnitr = (1 - (exp(-Rio.Knitr*yi_OD)))
            if self.existe_nova_contribuicao(j, i, matriz_contribuicoes):
                yi_DBO = Rio.eq_mistura_DBO(yi_DBO, matriz_contribuicoes[j][0], Q, matriz_contribuicoes[j][8])
                yi_OD = Rio.eq_mistura_OD(yi_OD, matriz_contribuicoes[j][1], Q, matriz_contribuicoes[j][8])
                yi_Norg = Rio.eq_mistura_Norg(yi_Norg, matriz_contribuicoes[j][2], Q, matriz_contribuicoes[j][8])
                yi_Namon = Rio.eq_mistura_Namon(yi_Namon, matriz_contribuicoes[j][3], Q, matriz_contribuicoes[j][8])
                yi_Nnitri = Rio.eq_mistura_Nnitri(yi_Nnitri, matriz_contribuicoes[j][4], Q, matriz_contribuicoes[j][8])
                yi_Nnitra = Rio.eq_mistura_Nnitra(yi_Nnitra, matriz_contribuicoes[j][5], Q, matriz_contribuicoes[j][8])
                yi_Porg = Rio.eq_mistura_Porg(yi_Porg, matriz_contribuicoes[j][6], Q, matriz_contribuicoes[j][8])
                yi_Pinorg = Rio.eq_mistura_Pinorg(yi_Pinorg, matriz_contribuicoes[j][7], Q, matriz_contribuicoes[j][8])

                if simula_difusa:
                    Q += matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q + Qe + Qinc
                else: 
                    if matriz_tipo_contribuicoes[j] != "C":
                        Q += matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q + Qe + Qinc
                    else:
                        Q = Q - matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q - Qe + Qinc
                
                j += 1

            else:
                yi_DBO = Rio.eq_mistura_DBO(yi_DBO, 0, Q, 0)
                yi_OD = Rio.eq_mistura_OD(yi_OD, 0, Q, 0)
                yi_Norg = Rio.eq_mistura_Norg(yi_Norg, 0, Q, 0)
                yi_Namon = Rio.eq_mistura_Namon(yi_Namon, 0, Q, 0)
                yi_Nnitri = Rio.eq_mistura_Nnitri(yi_Nnitri, 0, Q, 0)
                yi_Nnitra = Rio.eq_mistura_Nnitra(yi_Nnitra, 0, Q, 0)
                yi_Porg = Rio.eq_mistura_Porg(yi_Porg, 0, Q, 0)
                yi_Pinorg = Rio.eq_mistura_Pinorg(yi_Pinorg, 0, Q, 0)

                Q += Rio.Qinc

            if yi_OD < 0:
                yi_OD = 0
            elif yi_OD > 9:
                yi_OD = 9

            Q = round(Q, 6) 
            v = Rio.a_vel*(Q**Rio.b_vel)
            H = Rio.a_prof*(Q**Rio.b_prof)
            b = Q/(v*H)
            tempo = Rio.tam_cel / (v*24*3600)
            prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (T + 273.2))) - Rio.PH))
            Amonia_livre.append(yi_Namon*prop)
            Amonia_ionizada.append(yi_Namon*(1-prop))
                
            Const.Kd = Const.set_Kd(Q, H, 1.047, Const.K1, T)
            Const.Kt = Const.set_Kt(Rio.useK1, Const.K1, Const.Kd)
            Const.K2 = Const.set_K2(Q, 1.024, H, v, T, Rio)
                
            perfilK2.append(Const.K2)
            perfilKd.append(Const.Kd)
            perfilCs.append(Const.Cs)
            perfilQ.append(Q)
            perfilV.append(v)
            perfilH.append(H)
            perfilTempo.append(tempo)

            yi_DBO = yi_DBO + (Const.Kd + Const.Ks)*yi_DBO*tempo + Const.Lrd*tempo/b*H
            yi_OD = yi_OD + (Const.K2*(Const.Cs-yi_OD))*tempo + (-Const.Kd*yi_DBO*Const.Kt*tempo) + (-Rio.Ro2a*yi_Namon*Const.Kan*fnitr*tempo) + (-Rio.Ro2n*yi_Nnitri*Const.Knn*fnitr*tempo) - Const.Sd*tempo/H
            yi_Norg = yi_Norg - yi_Norg*(Const.Kso+Const.Koa)*tempo
            yi_Namon = yi_Namon + (Const.Koa*yi_Norg - yi_Namon*Const.Kan*fnitr + Rio.Samon)*fnitr
            yi_Nnitri = yi_Nnitri+ (yi_Namon*Const.Kan*fnitr - yi_Nnitri*Const.Knn*fnitr)*tempo
            yi_Nnitra = yi_Nnitra + (yi_Nnitri*Const.Knn*fnitr)*tempo
            yi_Porg = yi_Porg - yi_Porg*(Const.Kspo + Const.Koi)*tempo
            yi_Pinorg = yi_Pinorg + (Const.Koi*yi_Porg + Rio.Sinorg/H)*tempo

            # Anexa os valores calculados na iteracao 'i' aos vetores finais e atualiza os parametros que mudam a cada iteracao
            Y_DBO.append(yi_DBO)
            Y_OD.append(yi_OD)
            Y_Norg.append(yi_Norg)
            Y_Namon.append(yi_Namon)
            Y_Nnitri.append(yi_Nnitri)
            Y_Nnitra.append(yi_Nnitra)
            Y_Porg.append(yi_Porg)
            Y_Pinorg.append(yi_Pinorg)
                    
        Amonia = [Amonia_livre, Amonia_ionizada]
        
        cenario = Cenario(Y_DBO, Y_OD, Y_Norg, Y_Namon, Y_Nnitri, Y_Nnitra, Y_Porg, Y_Pinorg, Amonia, perfilK2, perfilKd, perfilQ, perfilV, perfilH, perfilCs, perfilTempo, matriz_contribuicoes)
        return cenario
