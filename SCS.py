# -*- coding: utf-8 -*-
# Modulo: SCS

# Importacao de bibliotecas
from Sub_bacia import Sub_bacia
from Leitura import *

# Definicao da classe
class SCS(object):

    # CONSTRUTOR
    def __init__(self, arquivo):
        self.vetor_CN = []  # Vetor com calculos do CN
        self.vetor_vazoes = []
        [self.matriz_subbacias, self.tam_cel, self.fator] = ler_entrada_hidro(arquivo)  # Entrada_Hidro.txt = [ID,L,s,A,C,P,J,M,L_Rio,N,Altitude,Temp]
        matriz_CN = ler_entrada_cn(arquivo)  # Entrada_CN.txt = [ID,Area,CN,Código]
        self.matriz_CME = ler_entrada_cme(arquivo)  # Entrada_CME.txt = [Codigo,Uso do Solo,CME_DBO,CME_NTK,CME_NOX,CME_PINORG]
        self.matriz_usos = ler_entrada_usos(arquivo)  # Entrada_Usos.txt = [ID,Area_codigo,Codigo]
        self.matriz_cargas = []  # matriz n° subbacias x 4, com vetores [carga_DBO, carga_NTK, carga_NOX, carga_PINORG]
        self.calcula_CN(matriz_CN)

    # METODOS
    # Metodo que executa
    def executa(self, matriz_reducao):
        self.sub_bacias = self.cria_subbacias(self.tam_cel)  # Lista com sub bacias dadas como entrada (n° em Hidro)
        self.calcula_CME_pond()
        self.gera_vazao_acumulada()
        matriz_difusa = []
        self.sub_bacias.sort(key=Sub_bacia.retorna_chave)  # Ordena a lista de subbacias pela chave

        for i in range(len(self.sub_bacias)):  # Para cada subbacia
            if len(matriz_reducao) > 0:  # Se matriz_reducao nao for nula
                self.sub_bacias[i].CME_DBO *= (1 - matriz_reducao[i][0])
                self.sub_bacias[i].CME_NTK *= (1 - matriz_reducao[i][1])
                self.sub_bacias[i].CME_NOX *= (1 - matriz_reducao[i][2])
                self.sub_bacias[i].CME_PINORG = self.sub_bacias[i].CME_PINORG * (1 - matriz_reducao[i][3])

            self.sub_bacias[i].calculaQdistribuida()
            self.sub_bacias[i].constroi_matrizDifusa(matriz_difusa)

            matriz_cargas = self.calcula_matriz_cargas()
            self.matriz_cargas = matriz_cargas

        return [matriz_difusa, self.sub_bacias, matriz_cargas]

    # Metodo que cria as subbacias
    def cria_subbacias(self, tam_cel):
        lista_subbacias = []

        for i in range(len(self.matriz_subbacias)):  # matriz_subbacias = [ID,L,s,A,C,P,J,M,L_Rio,N,Altitude,Temp,fator]
            aux = Sub_bacia(self.matriz_subbacias[i][0], self.matriz_subbacias[i][6], self.matriz_subbacias[i][8],
                            self.matriz_subbacias[i][9], self.matriz_subbacias[i][3], tam_cel,
                            self.matriz_subbacias[i][10], self.matriz_subbacias[i][11],self.fator)
            # aux = Sub_bacia(ID, J, L_Rio, N, A, tam_cel, Alt, T)

            aux.calcula_param(self.matriz_subbacias[i][1], self.matriz_subbacias[i][2], self.matriz_subbacias[i][3],
                              self.matriz_subbacias[i][4], self.matriz_subbacias[i][5], self.vetor_CN[i])
            # aux.calcula_param(L, s, A, C, P, CN)

            lista_subbacias.append(aux)
        
        # lista_subbacias = lista com sub bacias dadas como entrada
        return lista_subbacias

    def gera_vazao_acumulada(self):
        for i in range(len(self.sub_bacias)):  # Para cada subbacia
            j = i
            Area_anterior = 0
            Q_anterior = 0
            CME_ANTERIOR_DBO = 0
            CME_ANTERIOR_NTK = 0
            CME_ANTERIOR_NOX = 0
            CME_ANTERIOR_PINORG = 0

            while self.sub_bacias[j].Jusante != 0:  # Enquanto a jusante nao for nula
                if not self.sub_bacias[j].Visitada:  # Se a subbacia nao tiver sido visitada
                    self.sub_bacias[j].visita_sub()  # Visita a subbacia

                    # Guarda valores das constantes
                    Area_anterior = self.sub_bacias[j].Area
                    CME_ANTERIOR_DBO = self.sub_bacias[j].CME_DBO
                    CME_ANTERIOR_NTK = self.sub_bacias[j].CME_NTK
                    CME_ANTERIOR_NOX = self.sub_bacias[j].CME_NOX
                    CME_ANTERIOR_PINORG = self.sub_bacias[j].CME_PINORG
                    Q_anterior = Q_anterior + self.sub_bacias[j].Q_absoluta

                # j vai para a sub de jusante
                j = int(self.sub_bacias[j].Jusante) - 1

                # Atualiza os valores das constantes
                self.sub_bacias[j].Q_acumulada += Q_anterior
                self.sub_bacias[j].CME_DBO = ((CME_ANTERIOR_DBO * Area_anterior) + (self.sub_bacias[j].CME_DBO * self.sub_bacias[j].Area)) / (Area_anterior + self.sub_bacias[j].Area)
                self.sub_bacias[j].CME_NTK = ((CME_ANTERIOR_NTK * Area_anterior) + (self.sub_bacias[j].CME_NTK * self.sub_bacias[j].Area)) / (Area_anterior + self.sub_bacias[j].Area)
                self.sub_bacias[j].CME_NOX = ((CME_ANTERIOR_NOX * Area_anterior) + (self.sub_bacias[j].CME_NOX * self.sub_bacias[j].Area)) / (Area_anterior + self.sub_bacias[j].Area)
                self.sub_bacias[j].CME_PINORG = ((CME_ANTERIOR_PINORG * Area_anterior) + (self.sub_bacias[j].CME_PINORG * self.sub_bacias[j].Area)) / (Area_anterior + self.sub_bacias[j].Area)

            if not self.sub_bacias[j].Visitada:  # Se a subbacia nao tiver sido visitada
                self.sub_bacias[j].visita_sub()

    def calcula_CN(self, matriz_cn):
        j = 1
        numerador = 0
        denominador = 0

        for i in range(len(matriz_cn)):  # matriz_cn = [ID,Area,CN,Código]
            if matriz_cn[i][0] == j:  # se ID == j
                numerador = round(numerador + (matriz_cn[i][1] * matriz_cn[i][2]), 4)
                # numerador = numerados + (area*CN), aproximado com 4 casas decimais

                denominador = round(denominador + (matriz_cn[i][1]), 4)
                # denominador = denominador + area, aproximado com 4 casas decimais
            else:
                resultado = numerador / denominador
                j += 1
                self.vetor_CN.append(resultado)
                numerador = matriz_cn[i][1] * matriz_cn[i][2]  # numerador = area*CN
                denominador = matriz_cn[i][1]  # denominador = area

        resultado = numerador / denominador
        self.vetor_CN.append(resultado)
        # self.vetor_cn = vetor com calculos do CN

    def calcula_CME_pond(self):
        j = 0
        denominador = 0

        CME_DBO = 0
        CME_NTK = 0
        CME_NOX = 0
        CME_PINORG = 0

        # matriz_CME = [Codigo,Uso do Solo,CME_DBO,CME_NTK,CME_NOX,CME_PINORG]
        for i in range(len(self.matriz_usos)):  # matriz_usos = [ID,Area_codigo,Codigo]
            if self.matriz_usos[i][0] == (j + 1):  # Se ID == j+1
                CME_DBO += self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][2]
                # CME_DBO += Area_codigo * CME_DBO da (codigo-1)-esima linha de Entrada_CME.txt

                CME_NTK += self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][3]
                # CME_NTK += Area_codigo * CME_NTK da (codigo-1)-esima linha de Entrada_CME.txt

                CME_NOX += self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][4]
                # CME_NOX += Area_codigo * CME_NOX da (codigo-1)-esima linha de Entrada_CME.txt

                CME_PINORG += self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][5]
                # CME_PINORG += Area_codigo * CME_PINORG da (codigo-1)-esima linha de Entrada_CME.txt

                denominador += (self.matriz_usos[i][1])  # denominador += Area_codigo
            else:
                CME_DBO_POND = CME_DBO / denominador
                CME_NTK_POND = CME_NTK / denominador
                CME_NOX_POND = CME_NOX / denominador
                CME_PINORG_POND = CME_PINORG / denominador

                CME_DBO = self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][2]
                # CME_DBO = Area_codigo * CME_DBO da (codigo-1)-esima linha de Entrada_CME.txt

                CME_NTK = self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][3]
                # CME_NTK = Area_codigo * CME_NTK da (codigo-1)-esima linha de Entrada_CME.txt

                CME_NOX = self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][4]
                # CME_NOX = Area_codigo * CME_NOX da (codigo-1)-esima linha de Entrada_CME.txt

                CME_PINORG = self.matriz_usos[i][1] * self.matriz_CME[int(self.matriz_usos[i][2] - 1)][5]
                # CME_PINORG = Area_codigo * CME_PINORG da (codigo-1)-esima linha de Entrada_CME.txt
                
                denominador = self.matriz_usos[i][1]

                self.sub_bacias[j].CME_DBO = CME_DBO_POND
                self.sub_bacias[j].CME_NTK = CME_NTK_POND
                self.sub_bacias[j].CME_NOX = CME_NOX_POND
                self.sub_bacias[j].CME_PINORG = CME_PINORG_POND

                j = j + 1

        CME_DBO_POND = CME_DBO / denominador
        CME_NTK_POND = CME_NTK / denominador
        CME_NOX_POND = CME_NOX / denominador
        CME_PINORG_POND = CME_PINORG / denominador

        self.sub_bacias[j].CME_DBO = CME_DBO_POND
        self.sub_bacias[j].CME_NTK = CME_NTK_POND
        self.sub_bacias[j].CME_NOX = CME_NOX_POND
        self.sub_bacias[j].CME_PINORG = CME_PINORG_POND

    def calcula_matriz_cargas(self):
        matriz_cargas = []
        vetor_cargas = []
 
        for i in range(len(self.sub_bacias)):
            Carga_DBO = self.sub_bacias[i].Q_acumulada * (
                    ((self.sub_bacias[i].CME_DBO * 1000) / 1000000) * 86400)        
            Carga_NTK = self.sub_bacias[i].Q_acumulada * (
                    ((self.sub_bacias[i].CME_NTK * 1000) / 1000000) * 86400)
            Carga_NOX = self.sub_bacias[i].Q_acumulada * (
                    ((self.sub_bacias[i].CME_NOX * 1000) / 1000000) * 86400)
            Carga_PINORG = self.sub_bacias[i].Q_acumulada * (
                    ((self.sub_bacias[i].CME_PINORG * 1000) / 1000000) * 86400)

            vetor_cargas.append(Carga_DBO)
            vetor_cargas.append(Carga_NTK)
            vetor_cargas.append(Carga_NOX)
            vetor_cargas.append(Carga_PINORG)
            # vetor_cargas = [carga_DBO, carga_NTK, carga_NOX, carga_PINORG]

            matriz_cargas.append(vetor_cargas)
            vetor_cargas = []

        # matriz_cargas = matriz n° subbacias x 4, com vetores [carga_DBO, carga_NTK, carga_NOX, carga_PINORG]
        return matriz_cargas
