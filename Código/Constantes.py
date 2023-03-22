# -*- coding: utf-8 -*-
# Modulo: Constantes

from math import exp

# Definicao de variavel global
Tbase = 20

class Constantes:

    def __init__(self, K1, Ks, Koa, Kan, Knn, Kspo, Koi, Kso, Kt, Kb, Samon, Sd, Lrd, Spinorg):
        self.K1 = K1  # Coeficiente de desoxigenacao
        self.K2 = 0  # Coeficiente de reaeracao
        self.Ks = Ks  # Coeficiente de sedimentacao
        self.Koa = Koa  # Coeficiente de conversao do nitrogenio organico a amonia
        self.Kan = Kan  # Coeficiente de conversao de amonia a nitrito
        self.Knn = Knn  # Coeficiente de conversao de nitrito a nitrato
        self.Kspo = Kspo  # Coeficiente de remocao do fosforo organico por sedimentacao
        self.Koi = Koi  # Coeficiente de conversao de fosforo organico a fosforo inorganico
        self.Kso = Kso  # Coeficiente de sedimentacao do nitrogenio organico
        self.Kt = Kt  # Coeficiente de conversao entre a DBO5 e a DBOu
        self.Kd = 0  # Coeficiente de decomposicao
        self.Kb = Kb # Coeficiente dos coliformes
        self.Samon = Samon  # Fluxo de liberacao de amonia pelo sedimento de fundo
        self.Sd = Sd
        self.Lrd = Lrd
        self.Spinorg = Spinorg

    # Metodo para ajuste de constantes com base na temperatura
    @staticmethod
    def correcao(K, teta, t, tbase):
        corrigido = K * (teta ** (t - tbase))
        return corrigido

    def set_Kd(self, Q, H, tetaD, K1, T):
        if H <= 2.5:
            Kd = 0.3 * ((H / 2.5) ** (-0.434))
        elif 10 > H > 0.25 and 0 <= Q <= 500:
            Kd = 1.8 * (Q ** (-0.49))
        else:
            Kd = K1

        Kd = self.correcao(Kd, tetaD, T, 20)

        return Kd

    @staticmethod
    def set_Kt(K1):
        Kt = (1 / (1 - (exp(-5 * K1))))
            
        return Kt

    def set_K2(self, Q, teta2, T, H, v): 
        if H < 0.6:
            coef1 = 5.3 * (v ** 0.67) * (H ** -1.85)
        elif v < 0.8:
            coef1 = 3.93 * (v ** 0.5) * (H ** -1.5)
        else:
            coef1 = 5 * (v ** 0.97) * (H ** -1.67)

        if Q < 0.3:
            coef2 = 31.6 * v
        else:
            coef2 = 15.4 * v

        if Q < 0.556:
            coef3 = 517 * ((v * 0.001) ** 0.524) * (Q ** -0.242)
        else:
            coef3 = 596 * ((v * 0.001) ** 0.528) * (Q ** -0.136)

        if min(coef1, coef2, coef3) < 10: coef = min(coef1, coef2, coef3)
        else: coef = 10

        K2 = self.correcao(coef, teta2, T, Tbase)
        return K2
    
    @staticmethod
    def corrige_Spinorg(Spinorg, tetaSpinorg, T, Tbase, H):
        corrigido = Spinorg * (tetaSpinorg ** (T - Tbase)) / H
        return corrigido
    
    @staticmethod
    def corrige_Samon(Samon, tetaSamon, T, Tbase, H):
        return Samon * (tetaSamon ** (T - Tbase)) / H

    @staticmethod
    def corrige_Sd(Sd, tetaSd, T, Tbase, H):
        return Sd * (tetaSd ** (T - Tbase)) / H
    
    @staticmethod
    def corrige_k1(K1, tetaK1, T, Tbase):
        corrigido = K1 * (tetaK1 ** (T - Tbase))
        return corrigido

    def set_constantes(self, tetaK1, tetaK2, tetaS, tetaOA, tetaAN, tetaNN, tetaSPO, tetaOI, tetaSO, tetaD, tetaSamon, tetaSd, tetaSpinorg, tetaB, T, Q, H, v):
        self.K1 = self.corrige_k1(self.K1, tetaK1, T, Tbase)
        self.K2 = self.set_K2(Q, tetaK2, T, H, v)
        self.Ks = self.correcao(self.Ks, tetaS, T, Tbase)
        self.Koa = self.correcao(self.Koa, tetaOA, T, Tbase)
        self.Kan = self.correcao(self.Kan, tetaAN, T, Tbase)
        self.Knn = self.correcao(self.Knn, tetaNN, T, Tbase)
        self.Kspo = self.correcao(self.Kspo, tetaSPO, T, Tbase)
        self.Koi = self.correcao(self.Koi, tetaOI, T, Tbase)
        self.Kso = self.correcao(self.Kso, tetaSO, T, Tbase)
        self.Kt = self.set_Kt(self.K1)
        self.Kd = self.set_Kd(Q, H, tetaD, self.K1, T)
        self.Kb = self.correcao(self.Kb, tetaB, T, Tbase)
        self.Samon = self.corrige_Samon(self.Samon, tetaSamon, T, Tbase, H)
        self.Sd = self.corrige_Sd(self.Sd, tetaSd, T, Tbase, H)
        self.Spinorg = self.corrige_Spinorg(self.Spinorg, tetaSpinorg, T, Tbase, H)
        