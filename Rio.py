# -*- coding: utf-8 -*-
# Modulo: Rio

# Importacao de bibliotecas
import numpy as np

# Definicao da classe
class Rio(object):

    # CONSTRUTOR
    def __init__(self, DBO5r, ODr, NORGr, NAMONr, NNITRIr, PORGr, PINORGr, Qr, tam_rio, T, Alt, v, Ro2a, Ks, K1, K2,
                 Koa, Kan, Koi, Kspo, a_vel, b_vel, Qinc, a_prof, b_prof, formula_k2, m, n, useK1, PH, Samon, NNITRAr,
                 Kso, Knn, Ro2n, Knitr, tam_cel, classe, Sinorg, DBOinc, ODinc, NORGinc, NAMONinc, NNITRinc, NNITRAinc, Sd, Lrd):

        self.DBO5r = DBO5r  # Concentracao de DBO no rio
        self.ODr = ODr  # Concentracao de OD no rio
        self.NORGr = NORGr  # Concentracao de nitrogenio organico no rio
        self.NAMONr = NAMONr  # Concentracao de amonia no rio
        self.NNITRIr = NNITRIr  # Concentracao de nitrito no rio
        self.NNITRAr = NNITRAr  # Concentracao de nitrato no rio
        self.PORGr = PORGr  # Concentracao de fosforo organico no rio
        self.PINORGr = PINORGr  # Concentracao de fosforo inorganico no rio
        self.Qr = Qr  # Vazao do rio
        self.Qinc = Qinc  # Vazao incremental
        self.tam_rio = tam_rio  # Tamanho do rio, em metros
        self.tam_cel = tam_cel  # Tamanho da celula
        self.T = T  # Temperatura
        self.Alt = Alt  # Altitude
        self.v = v  # Velocidade
        self.Ro2a = Ro2a  # Relacao entre o consumo de oxigenio e a oxidacao da amonia
        self.Ks = Ks  # Coeficiente de sedimentacao
        self.K1 = K1  # Coeficiente de desoxigenacao
        self.K2 = K2  # Coeficiente de reaeracao
        self.Kt = 0  # Coeficiente de conversao da DBO5 a DBOu
        self.Koa = Koa  # Coeficiente de conversao de nitrogenio organico a amonia
        self.Kan = Kan  # Coeficiente de conversao de amonia a nitrito
        self.Koi = Koi  # Coeficiente de conversao de fosforo organico a fosforo inorganico
        self.Kspo = Kspo  # Coeficiente de remocao do fosforo organico por sedimentacao
        self.Kso = Kso  # Coeficiente de sedimentacao do nitrogenio organico
        self.Knn = Knn  # Coeficiente de conversao de nitrito a nitrato
        self.Knitr = Knitr  # Coeficiente de inibicao da nitrificacao por baixo OD
        self.Sinorg = Sinorg  # Coeficiente de liberacao de fosforo inorganico pelo sedimento de fundo
        self.a_vel = a_vel  # Constante de atualizacao da velocidade
        self.b_vel = b_vel  # Constante de atualizacao da velocidade
        self.a_prof = a_prof  # Constante de atualizacao da profundidade
        self.b_prof = b_prof  # Constante de atualizacao da profundidade 
        self.formula_k2 = formula_k2  # Valor que incida qual formula sera usada no calculo de K2
        self.m = m  # Constante para calculo de K2
        self.n = n  # Constante para calculo de K2
        self.useK1 = useK1  # Booleando que diz qual a constante usada no calculo de Kt (K1 ou Kd)
        self.PH = PH  # Ph
        self.Samon = Samon  # Fluxo de liberacao de amonia pelo sedimento de fundo
        self.Ro2n = Ro2n  # Relacao entre o oxigenio consumido por cada unidade de nitrito oxidado a nitrato
        self.classe = classe  # Classe do rio
        self.DBOinc = DBOinc  # DBO incremental
        self.ODinc = ODinc  # OD incremental
        self.NORGinc = NORGinc
        self.NAMONinc = NAMONinc
        self.NNITRinc = NNITRinc
        self.NNITRAinc = NNITRAinc
        self.Sd = Sd
        self.Lrd = Lrd

    # METODOS

    # Metodo que usa a equacao de mistura do OD
    def eq_mistura_DBO(self, DBOur, DBO5e, Qr, Qe):
        return ((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc)
    
    def eq_mistura_OD(self, ODr, ODe, Qr, Qe):
        return ((Qr * ODr) + (Qe * ODe) + (self.ODinc * self.Qinc)) / (Qr + Qe + self.Qinc)
    
    # Metodo que usa a equacao de mistura do nitrogenio
    @staticmethod
    def eq_mistura_Norg(NORGr, NORGe, Qr, Qe):
        return ((NORGr * Qr) + (NORGe * Qe)) / (Qr + Qe)

    @staticmethod
    def eq_mistura_Namon(NAMONr, NAMONe, Qr, Qe):
        return ((NAMONr * Qr) + (NAMONe * Qe)) / (Qr + Qe)

    @staticmethod
    def eq_mistura_Nnitri(NNITRIr, NNITRIe, Qr, Qe):
        return ((NNITRIr * Qr) + (NNITRIe * Qe)) / (Qr + Qe)

    @staticmethod
    def eq_mistura_Nnitra(NNITRAr, NNITRAe, Qr, Qe):
        return ((NNITRAr * Qr) + (NNITRAe * Qe)) / (Qr + Qe)

    # Metodo que usa a equacao de mistura do fosforo
    @staticmethod
    def eq_mistura_Porg(PORGr, PORGe, Qr, Qe):
        return ((PORGr * Qr) + (PORGe * Qe)) / (Qr + Qe)

    @staticmethod
    def eq_mistura_Pinorg(PINORGr, PINORGe, Qr, Qe):
        return ((PINORGr * Qr) + (PINORGe * Qe)) / (Qr + Qe)

    def Concatena_matrizes(self, matriz_difusa, matriz_contribuicoes, Cs):
        matriz_final = []
        i = 0
        j = 0
        T = self.T

        while i < len(matriz_difusa) or j < len(matriz_contribuicoes):
            if i == (len(matriz_difusa)) and j < len(matriz_contribuicoes):
                matriz_final.append(matriz_contribuicoes[j])
                j = j + 1
            elif j == (len(matriz_contribuicoes)) and i < len(matriz_difusa):
                vetor_aux = self.cria_vetor(matriz_difusa[i], T)
                matriz_final.append(vetor_aux)
                vetor_aux = []
                i = i + 1
            else:
                if matriz_difusa[i][6] < matriz_contribuicoes[j][9]:
                    vetor_aux = self.cria_vetor(matriz_difusa[i], T)
                    matriz_final.append(vetor_aux)
                    vetor_aux = []
                    i = i + 1
                elif matriz_difusa[i][6] == matriz_contribuicoes[j][9]:
                    T = matriz_contribuicoes[j][13]
                    new_dbo = self.eq_mistura_OD(matriz_difusa[i][0], matriz_difusa[i][1], matriz_contribuicoes[j][0],
                                                 matriz_contribuicoes[j][1], matriz_difusa[i][5],
                                                 matriz_contribuicoes[j][8], Cs)
                    new_nitr = self.eq_mistura_Nitr(0, matriz_difusa[i][2], matriz_difusa[i][3], 0,
                                                    matriz_contribuicoes[j][2], matriz_contribuicoes[j][3],
                                                    matriz_contribuicoes[j][4], matriz_contribuicoes[j][5],
                                                    matriz_difusa[i][5], matriz_contribuicoes[j][8])
                    new_fosf = self.eq_mistura_Fosf(0, matriz_difusa[i][4], matriz_contribuicoes[j][6],
                                                    matriz_contribuicoes[j][7], matriz_difusa[i][5],
                                                    matriz_contribuicoes[j][8])
                    vetor_aux.append(new_dbo[0][0])
                    vetor_aux.append(new_dbo[2][0])
                    vetor_aux.append(new_nitr[0][0])
                    vetor_aux.append(new_nitr[1][0])
                    vetor_aux.append(new_nitr[2][0])
                    vetor_aux.append(new_nitr[3][0])
                    vetor_aux.append(new_fosf[0][0])
                    vetor_aux.append(new_fosf[1][0])
                    vetor_aux.append(matriz_contribuicoes[j][8] + matriz_difusa[i][5])
                    vetor_aux.append(matriz_contribuicoes[j][9])
                    vetor_aux.append(matriz_contribuicoes[j][10])
                    vetor_aux.append(matriz_contribuicoes[j][11])
                    vetor_aux.append(matriz_contribuicoes[j][12])
                    vetor_aux.append(T)
                    matriz_final.append(vetor_aux)
                    vetor_aux = []
                    i = i + 1
                    j = j + 1
                else:
                    T = matriz_contribuicoes[j][13]
                    matriz_final.append(matriz_contribuicoes[j])
                    j = j + 1

        return matriz_final

    def cria_vetor(self, vetor_difusa, T):
        vetor_final = [vetor_difusa[0], vetor_difusa[1], 0.0, vetor_difusa[2], vetor_difusa[3], 0.0, 0.0,
                       vetor_difusa[4], vetor_difusa[5], vetor_difusa[6], 0.0, 0.0, self.K1, T]
        return vetor_final
