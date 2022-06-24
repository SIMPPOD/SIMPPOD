# -*- coding: utf-8 -*-
# Modulo: Sub_bacia

# Importacao de bibliotecas
from Constantes import Constantes

# Definicao da classe
class Sub_bacia(object):

    # CONSTRUTOR
    def __init__(self, ID, J, L, N, Area, tam_cel, Alt, T, fator):
        self.ID = ID
        self.Q_absoluta = 0
        self.Q_acumulada = 0
        self.Q_distribuida = 0
        self.Pe = 0
        self.S = 0
        self.Tp = 0
        self.Tc = 0
        self.Area = Area
        self.Jusante = J
        self.extensao = L / tam_cel
        self.N_rio = N
        self.CME_DBO = 0
        self.CME_NTK = 0
        self.CME_NOX = 0
        self.CME_PINORG = 0
        self.Visitada = False

        constantes = Constantes(None, None, None, None, None, None, None, None, None, None, None, None, None)
        cs = constantes.corrige_Cs(Alt, T)
        self.Cs = (1-fator)*cs

    # METODOS
    def visita_sub(self):
        self.Visitada = True

    def calcula_param(self, L, s, A, C, P, CN):
        self.S = self.calcula_S(CN)
        self.Pe = self.calcula_Pe(P)
        self.Tc = self.calcula_Tc(L, s, A, C)
        self.Tp = self.calcula_Tp()
        self.Q_absoluta = self.calcula_Q(self.Pe, self.Tp, A)
        self.Q_acumulada = self.Q_absoluta

    @staticmethod
    def calcula_Tc(L, s, A, C):
        if A < 50:
            s = s*1000  # passa de m/m para m/km
            if C == 1:
                Tc = 0.00167 * ((L / (s ** 0.5)) ** 0.7)
            else:
                Tc = 0.00024 * ((L / (s ** 0.5)) ** 0.7)
        elif 140 < A < 930:
            s = s*1000
            Tc = 21.88 * (A ** 0.41) * s ** (-0.17)
            Tc = Tc/60
        else:
            L = L/1000  # passa pra km
            Tc = 20.17 * ((L / (s ** 0.5)) ** 0.5)
            Tc = Tc/60        
        return Tc

    def calcula_Pe(self, P):
        if P > 0.2 * self.S:
            Pe = ((P - (0.2 * self.S)) ** 2) / (P + (0.8 * self.S))
        else:
            Pe = 0
        return Pe

    @staticmethod
    def calcula_S(CN):
        S = (25400 / CN) - 254
        return S

    def calcula_Tp(self):
        Tp = (self.Tc / 15) + (0.6 * self.Tc)
        return Tp

    @staticmethod
    def calcula_Q(Pe, Tp, A):
        Q = (0.208 * (Pe * A)) / Tp
        return Q

    def calculaQdistribuida(self):
        self.Q_distribuida = self.Q_acumulada / self.extensao

    def constroi_matrizDifusa(self, matriz_difusa):
        if self.extensao != 1 or self.N_rio > len(matriz_difusa):
            if self.Q_distribuida > 0:
                for i in range(int(self.extensao)):
                    vetor_aux = [self.CME_DBO, self.Cs, self.CME_NTK, self.CME_NOX, self.CME_PINORG, self.Q_distribuida,
                                 self.N_rio + i]
                    matriz_difusa.append(vetor_aux)
        else:
            for j in range(len(matriz_difusa)):
                if matriz_difusa[j][6] == self.N_rio:
                    matriz_difusa[j][0] = matriz_difusa[j][0] + self.CME_DBO
                    matriz_difusa[j][2] = matriz_difusa[j][2] + self.CME_NTK
                    matriz_difusa[j][3] = matriz_difusa[j][3] + self.CME_NOX
                    matriz_difusa[j][4] = matriz_difusa[j][4] + self.CME_PINORG
                    matriz_difusa[j][5] = matriz_difusa[j][5] + self.Q_distribuida

        return matriz_difusa

    def retorna_chave(self):
        if self.extensao != 1:
            return self.N_rio + 1
        else:
            return self.N_rio
