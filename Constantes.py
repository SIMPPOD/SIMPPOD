# -*- coding: utf-8 -*-
# Modulo: Constantes

# Importacao de bibliotecas
from math import exp

# Definicao de variavel global
Tbase = 20

# Definicao da classe
class Constantes:

    # CONSTRUTOR
    def __init__(self, K1, K2, Ks, Koa, Kan, Knn, Kspo, Koi, Kso, Kt, Samon, Sd, Lrd):
        self.K1 = K1  # Coeficiente de desoxigenacao
        self.K2 = K2  # Coeficiente de reaeracao
        self.Koa = Koa  # Coeficiente de conversao do nitrogenio organico a amonia
        self.Kan = Kan  # Coeficiente de conversao de amonia a nitrito
        self.Knn = Knn  # Coeficiente de conversao de nitrito a nitrato
        self.Cs = 0  # Coeficiente de saturacao
        self.Kspo = Kspo  # Coeficiente de remocao do fosforo organico por sedimentacao
        self.Koi = Koi  # Coeficiente de conversao de fosforo organico a fosforo inorganico
        self.Kso = Kso  # Coeficiente de sedimentacao do nitrogenio organico
        self.Kt = Kt  # Coeficiente de conversao entre a DBO5 e a DBOu
        self.Kd = 0  # Coeficiente de decomposicao
        self.Ks = Ks  # Coeficiente de sedimentacao
        self.Samon = Samon  # Fluxo de liberacao de amonia pelo sedimento de fundo
        self.Sd = Sd
        self.Lrd = Lrd

    # METODOS
    # elf.correcao(self.Kspo, 1.047, 20.6, 20)
    # Metodo para ajuste de constantes com base na temperatura
    @staticmethod
    def correcao(K, teta, t, tbase):
        corrigido = K * (teta ** (t - tbase))
        return corrigido

    # Metodo que seta o Kd
    def set_Kd(self, Q, H, tetaD, K1, T):
        if H <= 2.5:
            Kd = 0.3 * ((H / 2.5) ** (-0.434))
        elif 10 > H > 0.25 and 0 <= Q <= 500:
            Kd = 1.8 * (Q ** (-0.49))
        else:
            Kd = K1

        Kd = self.correcao(Kd, tetaD, T, 20)

        return Kd

    # Metodo que seta o Kt
    @staticmethod
    def set_Kt(useK1, K1, Kd):
        if useK1 == 1:
            Kt = (1 / (1 - (exp(-5 * K1))))
        else:
            Kt = (1 / (1 - (exp(-5 * Kd))))
            
        return Kt

    # Metodo que calcula K2 baseado em uma das formulas escolhidas pelo usuario
    def set_K2(self, Q, teta2, H, v, T, Rio): 
        if Rio.formula_k2 == 0:
            K2 = 0.37

        elif Rio.formula_k2 == 1:
            # Quadro 1.4
            if 0.6 <= H < 4:
                if 0.05 <= v < 0.8:
                    K2 = 3.93 * (v ** 0.5) * (H ** (-1.5))
                elif 0.8 <= v < 1.5:
                    K2 = 5 * (v ** 0.97) * (H ** (-1.67))
            elif 0.1 <= H < 0.6:
                if 0.05 <= v < 1.5:
                    K2 = 5.3 * (v ** 0.67) * (H ** (-1.85))

        elif Rio.formula_k2 == 2:
            K2 = Rio.m * (Q ** Rio.n)

        elif Rio.formula_k2 == 3:
            K2 = 3.73 * ((0.1433 * (Q ** 0.6305)) ** 0.5) * ((0.6076 * (Q ** 0.2566)) ** (-1.5))

        else:
            K2 = self.K2

        K2 = self.correcao(K2, teta2, T, Tbase)

        if K2 > 10:
            K2 = 10

        return K2

    def set_constantes(self, tetaS, tetaD, teta2, tetaOA, tetaAN, tetaSPO, tetaOI, tetaSO, tetaNN, T, Q, H, v, Rio, tetaSamon, tetaSd):
        self.Ks = self.correcao(self.Ks, tetaS, T, Tbase)
        self.Koa = self.correcao(self.Koa, tetaOA, T, Tbase)
        self.Kan = self.correcao(self.Kan, tetaAN, T, Tbase)
        self.Kspo = self.correcao(self.Kspo, tetaSPO, T, Tbase)
        self.Koi = self.correcao(self.Koi, tetaOI, T, Tbase)
        self.Kso = self.correcao(self.Kso, tetaSO, T, Tbase)
        self.Knn = self.correcao(self.Knn, tetaNN, T, Tbase)
        self.K2 = self.set_K2(Q, teta2, H, v, T, Rio)
        self.Kd = self.set_Kd(Q, H, tetaD, self.K1, T)
        self.Kt = self.set_Kt(Rio.useK1, self.K1, self.Kd)
        self.Samon = self.correcao(self.Samon, tetaSamon, T, Tbase)
        self.Sd = self.correcao(self.Sd, tetaSd, T, Tbase)

    # Metodo que corrige o coeficiente de saturacao
    @staticmethod
    def corrige_Cs(Alt, T):
        Cs = (1 - (Alt / 9450)) * (14.652 - (0.41022 * T) + (0.007911 * (T ** 2)) - (0.000077774 * (T ** 3)))
        if Cs > 10:
            Cs = 10

        return Cs
