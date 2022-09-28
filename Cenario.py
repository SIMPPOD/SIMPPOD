# -*- coding: utf-8 -*-
# Modulo: Cenario

# Definicao da classe
class Cenario:

    # CONSTRUTOR
    def __init__(self, Y_DBO, Y_OD, Y_Norg, Y_Namon, Y_Nnitri, Y_Nnitra, Y_Porg, Y_Pinorg, Amonia, PerfilK2, PerfilKd, PerfilQ, PerfilV, PerfilH, PerfilTempo, matriz_contribuicoes):
        # Valores calculados em Euler
        self.Y_DBO = Y_DBO 
        self.Y_OD = Y_OD
        self.Y_Norg = Y_Norg
        self.Y_Namon = Y_Namon
        self.Y_Nnitri = Y_Nnitri
        self.Y_Nnitra = Y_Nnitra
        self.Y_Porg = Y_Porg
        self.Y_Pinorg = Y_Pinorg
        self.Amonia = Amonia  # Matriz [Amonia livre, Amonia ionizada]
        self.PerfilK2 = PerfilK2 
        self.PerfilKd = PerfilKd  
        self.PerfilQ = PerfilQ  
        self.PerfilV = PerfilV 
        self.PerfilH = PerfilH  
        self.matriz_contribuicoes = matriz_contribuicoes
        self.sub_bacias = []  # Matriz [DBO,Cs,NTK,NOx,Pinorg,Qacumulada,Qdistribuida,TC,Jusante,Visitada,ID]
        self.matriz_cargas = []  # Matriz [Carga DBO, Carga NTK, Carga NOx, Carga Pinorg]
        self.PerfilTempo = PerfilTempo
    
    @staticmethod
    def get_N(N):
        return N