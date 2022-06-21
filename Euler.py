# -*- coding: utf-8 -*-
# Modulo: Euler

""" Nesse modulo, temos a implementacao proposta da classe que resolve
o metodo de Euler para a resolucao de um sistema de equacoes
diferenciais ordinarias e de primeira ordem. Tambem esta nesse arquivo
a funcao que faz a avaliacao da funcao F que e fixa """

# Importacao de bibliotecas
from dataclasses import FrozenInstanceError
from math import exp
from tkinter.constants import S
from xml.dom.minidom import NamedNodeMap
from DBO import DBO
from Nitrogenio import Nitrogenio
from Fosforo import Fosforo
from Cenario import Cenario
from Constantes import Constantes
import numpy as np

# Definicao da classe
class Euler(object):

    # METODOS

    # Metodo que avalia a funcao F que varia de poluente para poluente, mas que tem o formato matriz*vetor + vetor auxiliar
    @staticmethod
    def F(M1, M2, v):
        f = np.dot(M1, M2)  # Multiplicacao de matrizes
        f = f + v
        return f

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
        Const = Constantes(Rio.K1, Rio.K2, Rio.Ks, Rio.Koa, Rio.Kan, Rio.Knn, Rio.Kspo, Rio.Koi, Rio.Kso, Rio.Kt, Rio.Samon)
        Const.Cs = Cs
        
        Q = Rio.Qr
        T = Rio.T
        v = Rio.a_vel*(Q**Rio.b_vel)
        H = Rio.a_prof*(Q**Rio.b_prof)
        prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (T + 273.2))) - Rio.PH))
        Amonia_livre = [Rio.NAMONr*prop]
        Amonia_ionizada = [Rio.NAMONr*(1-prop)]
    
        Const.set_constantes(1.024, 1.047, 1.024, 1.047, 1.080, 1.024, 1.047, 1.024, 1.047, T, Q, H, v, Rio, 1.074)
        # set_constantes    (tetaS, tetaD, teta2, tetaOA, tetaAN, tetaSPO, tetaOI, tetaSO, tetaNN, T, Q, H, v, Rio, tetaSamon)

        perfilK2 = [Const.K2]
        perfilKd = [Const.Kd]
        perfilCs = [Const.Cs]
        perfilQ = [Q]
        perfilV = [v]
        perfilH = [H]
        perfilTempo = [0]
 
        y0_DBO = np.array([[Rio.DBO5r], [(Const.Cs - Rio.ODr)], [Rio.ODr]])
        y0_Nitr = np.array([[Rio.NORGr], [Rio.NAMONr], [Rio.NNITRIr], [Rio.NNITRAr]])
        y0_Fosf = np.array([[Rio.PORGr], [Rio.PINORGr]])           
        
        vazoes = []
        profundidades = []
        velocidades = []
        
        yi_DBO = y0_DBO
        yi_Nitr = y0_Nitr
        yi_Fosf = y0_Fosf

        if matriz_contribuicoes[0][9] == 0:
            yi_DBO = Rio.eq_mistura_OD(yi_DBO[0][0], yi_DBO[2][0], matriz_contribuicoes[0][0], matriz_contribuicoes[0][1], Q, matriz_contribuicoes[0][8], Const.Cs)
            yi_Nitr = Rio.eq_mistura_Nitr(yi_Nitr[0][0], yi_Nitr[1][0], yi_Nitr[2][0], yi_Nitr[3][0], matriz_contribuicoes[0][2], matriz_contribuicoes[0][3], matriz_contribuicoes[0][4], matriz_contribuicoes[0][5], Q, matriz_contribuicoes[0][8])
            yi_Fosf = Rio.eq_mistura_Fosf(yi_Fosf[0][0], yi_Fosf[1][0], matriz_contribuicoes[0][6], matriz_contribuicoes[0][7], Q, matriz_contribuicoes[0][8])
            j = j + 1
    
        Y_DBO = yi_DBO
        Y_Nitr = yi_Nitr
        Y_Fosf = yi_Fosf

        Dbo = DBO()
        Nitr = Nitrogenio()
        Fosf = Fosforo()
        
        num_cel = Rio.tam_rio / Rio.tam_cel
        num_cel = int(num_cel)

        for i in range(1, num_cel):
            if self.existe_nova_contribuicao(j, i, matriz_contribuicoes):
                fnitr = (1 - (exp(-Rio.Knitr*yi_DBO[2][0])))  # fnitr = (1 - exp(-Knitr*ODr))
                    
                # Considera uma nova contribuicao sem aplicar reducao
                yi_DBO = Rio.eq_mistura_OD(yi_DBO[0][0], yi_DBO[2][0], matriz_contribuicoes[j][0], matriz_contribuicoes[j][1], Q, matriz_contribuicoes[j][8], Const.Cs)
                yi_Nitr = Rio.eq_mistura_Nitr(yi_Nitr[0][0], yi_Nitr[1][0], yi_Nitr[2][0], yi_Nitr[3][0], matriz_contribuicoes[j][2], matriz_contribuicoes[j][3], matriz_contribuicoes[j][4], matriz_contribuicoes[j][5], Q, matriz_contribuicoes[j][8])
                yi_Fosf = Rio.eq_mistura_Fosf(yi_Fosf[0][0], yi_Fosf[1][0], matriz_contribuicoes[j][6], matriz_contribuicoes[j][7], Q, matriz_contribuicoes[j][8])

                if yi_DBO[2][0] < 0:
                    yi_DBO[2][0] = 0
                elif yi_DBO[2][0] > 9:
                    yi_DBO[2][0] = 9
                
                vazoes.append(Q)
                profundidades.append(H)
                velocidades.append(v)

                if simula_difusa:
                    Q += matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q + Qe + Qinc
                else: 
                    if matriz_tipo_contribuicoes[j] != "C":
                        Q += matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q + Qe + Qinc
                    else:
                        Q = Q - matriz_contribuicoes[j][8] + Rio.Qinc  # Q = Q - Qe + Qinc

                Q = round(Q, 6)
                v = Rio.a_vel*(Q**Rio.b_vel)
                H = Rio.a_prof*(Q**Rio.b_prof)
                tempo = Rio.tam_cel / (v*24*3600)
                prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (T + 273.2))) - Rio.PH))
                Amonia_livre.append(yi_Nitr[1][0]*prop)
                Amonia_ionizada.append(yi_Nitr[1][0]*(1-prop))
                j = j + 1
                    
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

                M_DBO = Dbo.constroi_matriz(Const.Kd, Const.Ks, Const.K2, Const.Kt)
                M_Nitr = Nitr.constroi_matriz(Const.Koa, Const.Kan, Const.Kso, Const.Knn, fnitr)
                M_Fosf = Fosf.constroi_matriz(Const.Koi, Const.Kspo)

                M_DBO  = [[-Kd - Ks, 0, 0],
                          [Kd, K2, 0],
                          [-Kd*Kt, 0, -K2]]

                yi_DBO = [[((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc)],
                          [Cs - C0],
                          [((Qr * ODr) + (Qe * ODe) + (self.ODinc * self.Qinc)) / (Qr + Qe + self.Qinc)]]
                
                M_DBO * yi_DBO = [(-Kd - Ks) * ((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc)],
                                 [Kd * ((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc) + K2 * (Cs - C0)]
                                 [(-Kd*Kt) * ((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc) - K2 * ((Qr * ODr) + (Qe * ODe) + (self.ODinc * self.Qinc)) / (Qr + Qe + self.Qinc)]

                               = [(-Kd - Ks) * Ldbo] 
                                 [Kd * Ldbo + K2 * (Cs - C0)]
                                 [-Kd*Kt*Ldbo - K2*Lod]
                
                M_DBO * yi_DBO + aux_DBO = [(-Kd - Ks) * Ldbo]
                                           [(Kd*Ldbo + K2*(Cs - C0)) + (Ro2a * fnitr * Namon * Kan) + (Ro2n * fnitr * Nnitri * Knn) - (K2 * Cs)]
                                           [(-Kd*Kt*Ldbo - K2*Lod) + (K2 * Cs) - (Ro2a * fnitr * Namon * Kan) + (Ro2n * fnitr * Nnitri * Knn)]

                                         = [-Kd*Ldbo - Ks*Ldbo ==> + (Lrd/(base{coluna P}*altura))]
                                           [Kd*Ldbo - K2*C0 + Ro2a*fnitr*Namon*Kan + {Ro2n*fnitr*Nnitri*Knn}]
                                           [-Kd*Kt*Ldbo - K2*Lod + K2*Cs - Ro2a*fnitr*Namon*Kan + Ro2n*fnitr*Nnitri*Knn]

                
                
                aux_DBO =  [[0], [(Ro2a * fnitr * Namon * Kan) + (Ro2n * fnitr * Nnitri * Knn) - (K2 * Cs)], [(K2 * Cs) - (Ro2a * fnitr * Namon * Kan) + (Ro2n * fnitr * Nnitri * Knn)]]
                              
                # Calculo dos vetores auxiliares
                aux_DBO = Dbo.constroi_vetor_auxiliar(Const.K2, Const.Cs, Rio.Ro2a, Rio.Ro2n, Const.Kan, fnitr, y0_Nitr[1][0], y0_Nitr[2][0], Const.Knn)
                aux_Nitr = Nitr.constroi_vetor_auxiliar(Rio.Samon, H)
                aux_Fosf = Fosf.constroi_vetor_auxiliar(Rio.Sinorg, H)

                # Calculo das matrizes
                Fxy_DBO = Euler.F(M_DBO, yi_DBO, aux_DBO)
                Fxy_Nitr = Euler.F(M_Nitr, yi_Nitr, aux_Nitr)
                Fxy_Fosf = Euler.F(M_Fosf, yi_Fosf, aux_Fosf)
                    
                yi_DBO += tempo * Fxy_DBO
                yi_Nitr += tempo * Fxy_Nitr
                yi_Fosf += tempo * Fxy_Fosf

            else:                
                fnitr = (1 - (exp(-Rio.Knitr*yi_DBO[2][0])))  # fnitr = (1 - exp(-Knitr*ODr))
                yi_DBO = Rio.eq_mistura_OD(yi_DBO[0][0], yi_DBO[2][0], 0, 0, Q, 0, Const.Cs)
                yi_Nitr = Rio.eq_mistura_Nitr(yi_Nitr[0][0], yi_Nitr[1][0], yi_Nitr[2][0], yi_Nitr[3][0], 0, 0, 0, 0, Q, 0)

                if yi_DBO[2][0] < 0:
                    yi_DBO[2][0] = 0
                elif yi_DBO[2][0] > 9:
                    yi_DBO[2][0] = 9

                vazoes.append(Q)
                profundidades.append(H)
                velocidades.append(v)
                
                Q += Rio.Qinc
                Q = round(Q, 6) 
                v = Rio.a_vel*(Q**Rio.b_vel)
                H = Rio.a_prof*(Q**Rio.b_prof)
                tempo = Rio.tam_cel / (v*24*3600)
                prop = 100/(1 + 10 ** ((0.09018 + (2729.92 / (T + 273.2))) - Rio.PH))
                Amonia_livre.append(yi_Nitr[1][0]*prop)
                Amonia_ionizada.append(yi_Nitr[1][0]*(1-prop))
                
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

                M_DBO = Dbo.constroi_matriz(Const.Kd, Rio.Ks, Const.K2, Const.Kt)
                M_Nitr = Nitr.constroi_matriz(Const.Koa, Const.Kan, Const.Kso, Const.Knn, fnitr)
                M_Fosf = Fosf.constroi_matriz(Const.Koi, Const.Kspo)

                aux_DBO = Dbo.constroi_vetor_auxiliar(Const.K2, Const.Cs, Rio.Ro2a, Rio.Ro2n, Rio.Kan, fnitr, yi_Nitr[1][0], yi_Nitr[2][0], Const.Knn)
                aux_Nitr = Nitr.constroi_vetor_auxiliar(Rio.Samon, H)
                aux_Fosf = Fosf.constroi_vetor_auxiliar(Rio.Sinorg, H)

                Fxy_DBO = Euler.F(M_DBO, yi_DBO, aux_DBO)
                Fxy_Nitr = Euler.F(M_Nitr, yi_Nitr, aux_Nitr)
                Fxy_Fosf = Euler.F(M_Fosf, yi_Fosf, aux_Fosf)
                
                yi_DBO += tempo * Fxy_DBO
                yi_Nitr += tempo * Fxy_Nitr
                yi_Fosf += tempo * Fxy_Fosf

            # Anexa os valores calculados na iteracao 'i' aos vetores finais e atualiza os parametros que mudam a cada iteracao
            Y_DBO = np.append(Y_DBO, yi_DBO, axis=1)
            Y_Nitr = np.append(Y_Nitr, yi_Nitr, axis=1)
            Y_Fosf = np.append(Y_Fosf, yi_Fosf, axis=1)
                    
        Amonia = [Amonia_livre, Amonia_ionizada]
        
        cenario = Cenario(Y_DBO, Y_Nitr, Y_Fosf, Amonia, perfilK2, perfilKd, perfilQ, perfilV, perfilH, perfilCs, perfilTempo, matriz_contribuicoes)
        return cenario
