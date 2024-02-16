﻿# -*- coding: utf-8 -*-
# Modulo: Cromossomo

from random import uniform, random

class Cromossomo:

    def __init__(self, simula_difusa, tam_cromossomo):
        self.func_objetivo = [999999]
        self.alelos = []
        self.alelos_codificados = []
        self.cenario = []
        self.simula_difusa = simula_difusa
        self.tam_cromossomo = tam_cromossomo

    def exec_QualUFMG(self, qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios):
        if self.simula_difusa:
            self.cenario = qual_ufmg.executa(caminho_curso, simulacao_curso, Rio, matriz_contribuicoes, matriz_reducao_pontual, True, self.alelos, scs, numFuncao, matriz_tipo_contribuicoes, celula_entrada_tributarios)

        else:
            matriz_reducao_pontual[0] = self.alelos
            matriz_reducao_difusa = []
            self.cenario = qual_ufmg.executa(caminho_curso, simulacao_curso, Rio, matriz_contribuicoes, matriz_reducao_pontual, False, matriz_reducao_difusa, scs, numFuncao, matriz_tipo_contribuicoes, celula_entrada_tributarios)

    def get_func_obj(self):
        return self.func_objetivo
        
    # Metodo que seta randomicamente os alelos de um cromossomo, respeitando sempre as eficiencias minimas pre estabelecidas
    def set_alelos_random(self, ef_minima, modo_otimizacao, numFuncao):
        if modo_otimizacao == 1 or modo_otimizacao == 2:
            aux = []

            # Fixar minimos e maximos de reducao
            if self.simula_difusa:
                for i in range(self.tam_cromossomo):
                    for j in range(5):
                        aux.append((round(uniform(0.0, 0.95), 4)))
                    self.alelos.append(aux)
                    aux = []
            else:
                if numFuncao == 3:
                    for i in range(self.tam_cromossomo):
                        aux.append((round(uniform(float(ef_minima[i]), 0.95), 4)))
                        aux.append((round(uniform(0.0, 0.95), 4)))
                        self.alelos.append(aux)
                        aux = []
                else:
                    for i in range(self.tam_cromossomo):
                        self.alelos.append((round(uniform(float(ef_minima[i]), 0.95), 4)))

        elif modo_otimizacao == 3:
            aux = []

            if self.simula_difusa:
                for i in range(self.tam_cromossomo):
                    for j in range(5):
                        aux.append((round(uniform(0.0, 1.0), 4)))
                    self.alelos_codificados.append(aux)
                    aux = []
            else:
                if numFuncao == 3:
                    for i in range(self.tam_cromossomo):
                        for j in range(2):
                            aux.append((round(uniform(0.0, 1.0), 4)))
                        self.alelos_codificados.append(aux)
                        aux = []
                else: 
                    for i in range(self.tam_cromossomo):
                        self.alelos_codificados.append((round(uniform(0.0, 1.0), 4)))
        
        elif modo_otimizacao == 4:
            aux = []

            if self.simula_difusa:
                for i in range(self.tam_cromossomo):
                    for j in range(5):
                        aux.append((round(uniform(0.0, 1.0), 4)))
                    self.alelos.append(aux)
                    aux = []
            else:
                if numFuncao == 3:
                    for i in range(self.tam_cromossomo):
                        aux.append((round(uniform(float(ef_minima[i]), 0.95), 4)))
                        aux.append((round(uniform(0.0, 0.95), 4)))
                        self.alelos.append(aux)
                        aux = []
                        
                else:
                    for i in range(self.tam_cromossomo):
                        self.alelos.append((round(uniform(float(ef_minima[i]), 0.95), 4)))

    def set_alelos(self, alelos):
        self.alelos = alelos

    def decodificador(self, ef_minima, numFuncao):
        qtdAlelos = len(self.alelos_codificados)
        intervalo_antes = 1/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 1]
        aux = []

        if numFuncao == 1 or numFuncao == 5 or numFuncao == 6 or numFuncao == 7:
            if self.simula_difusa:
                intervalo_depois = 0.95/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 0.9]
                for i in range(qtdAlelos): 
                    for j in range(5):
                        # Codificacao do alelo por regra de tres
                        aux.append(round((intervalo_depois*self.alelos_codificados[i][j])/intervalo_antes, 4)) 
                    self.alelos.append(aux)
                    aux = []              

            else:
                for i in range(qtdAlelos): 
                    intervalo_depois = (0.95 - float(ef_minima[i]))/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [ef_minima, 0.9]
                    # Codificacao do alelo por regra de tres
                    self.alelos.append(round((intervalo_depois*self.alelos_codificados[i])/intervalo_antes + ef_minima[i], 4)) 

        elif numFuncao == 2:
            intervalo_depois = 0.95/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 0.9]
            for i in range(qtdAlelos):
                aux.append(round((intervalo_depois*self.alelos_codificados[i])/intervalo_antes, 4))
            self.alelos = aux

        elif numFuncao == 3:
            for i in range(qtdAlelos): 
                intervalo_depois = (0.95 - float(ef_minima[i]))/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [ef_minima, 0.9]
                # Codificacao do alelo por regra de tres
                aux.append(round((intervalo_depois*self.alelos_codificados[i][0])/intervalo_antes + ef_minima[i], 4))
                intervalo_depois = 0.95/qtdAlelos
                aux.append(round((intervalo_depois*self.alelos_codificados[i][1])/intervalo_antes, 4))
                self.alelos.append(aux)
                aux = []

    # Metodo que avalia a condicao do rio
    def isValido(self, Rio, numFuncao):
        if numFuncao == 1:
            if len(self.alelos) == 0: 
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 3:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 6:
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 5:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 5:
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 10:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 4:
                        return False
            elif Rio.classe == 4.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 30 :
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 2:
                        return False
            return True
        
        elif numFuncao == 2:
            if len(self.alelos) == 0:
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 6:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 6:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 6:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 6:
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 5:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 5:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 5:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 5:
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 13.3 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 4:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 5.6 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 4:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2.2 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 4:
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1.0 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 4:
                        return False
            elif Rio.classe == 4.0:
                return False   
            return True
        
        elif numFuncao == 3:
            if len(self.alelos) == 0:
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 3:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 6:
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5):
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 5:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 5:
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5):
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 10:
                        return False
                for i in range(len(self.cenario.Y_OD)):
                    if self.cenario.Y_OD[i] < 4:
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 13.3 and Rio.PH <= 7.5):
                        return False
                    elif (self.cenario.Y_Namon[i] >= 5.6 and 7.5 <= Rio.PH <= 8.0): 
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2.2 and 8.0 <= Rio.PH <= 8.5): 
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1.0 and Rio.PH > 8.5):
                        return False
            return True
        
        elif numFuncao == 4:
            if len(self.alelos) == 0:
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_Coliformes)):
                    if self.cenario.Y_Coliformes[i] > 200:
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_Coliformes)):
                    if self.cenario.Y_Coliformes[i] > 1000:
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_Coliformes)):
                    if self.cenario.Y_Coliformes[i] > 2500:
                        return False
            elif Rio.classe == 4.0:
                return True
            return True
        
        elif numFuncao == 5 or numFuncao == 6:
            if len(self.alelos) == 0: 
                return False
            elif self.simula_difusa:
                if Rio.classe == 1.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10 or self.cenario.Y_Pinorg[i] > 0.05:
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 3.7:
                            return False
                        if 8 > Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 2:
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 1:
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 0.5:
                            return False
                    for i in range(len(self.cenario.Y_Coliformes)):
                        if self.cenario.Y_Coliformes[i] >= 200:
                            return False
                elif Rio.classe == 2.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10:
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 3.7:
                            return False
                        if 8 >= Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 50:
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 50:
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 0.5:
                            return False
                    for i in range(len(self.cenario.Y_Coliformes)):
                        if self.cenario.Y_Coliformes[i] >= 1000:
                            return False
                elif Rio.classe == 3.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10 or self.cenario.Y_Pinorg[i] > 0.075:
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 13.3:
                            return False
                        if 8 > Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 5.6:
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 2.2:
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 1:
                            return False
                    for i in range(len(self.cenario.Y_Coliformes)):
                        if self.cenario.Y_Coliformes[i] >= 2500:
                            return False
                elif Rio.classe == 4.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 50 or self.cenario.Y_Nnitra[i] > 50 or self.cenario.Y_Pinorg[i] > 50:
                            return False

            else:
                if Rio.classe == 1.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_DBO[i] > 3 or self.cenario.Y_OD[i] < 6:
                            return False
                elif Rio.classe == 2.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_DBO[i] > 5:
                            return False
                    for i in range(len(self.cenario.Y_OD)):
                        if self.cenario.Y_OD[i] < 5:
                            return False
                elif Rio.classe == 3.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_DBO[i] > 10 or self.cenario.Y_OD[i] < 4:
                            return False
                elif Rio.classe == 4.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_DBO[i] > 30 or self.cenario.Y_OD[i] < 2:
                            return False
                return True

    def avalia_func_objetivo(self, matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs):
        cargas = []
        valor_funcao = 0
        carga_media = 0
        area_total = 0

        # Funcao simples que minimiza apenas as eficiencias sem medida de equidade
        if numFuncao == 1 or numFuncao == 2 or numFuncao == 4:
            self.func_objetivo = [sum(self.alelos)]
            
        elif numFuncao == 3:
            for i in range(self.tam_cromossomo):
                valor_funcao += (vetor_pesos_pontual[0]*self.alelos[i][0]) + (vetor_pesos_pontual[1]*self.alelos[i][1])
            self.func_objetivo = [valor_funcao]

        # Duas proximas funcoes objetivas utilizam os valores de carga media e de eficiencia media do cromossomo
        elif numFuncao == 5 or numFuncao == 6:
            ef_media = ((sum(self.alelos))/len(self.alelos))  
            for j in range(len(matriz_contribuicoes)): 
                if matriz_contribuicoes[j][10] == 1:  # Se ExR for 1
                    carga = matriz_contribuicoes[j][8]*matriz_contribuicoes[j][0]  # Qe * DBO5e
                    cargas.append(carga)
                    carga_media += carga
                carga_media = carga_media/(len(cargas))

            if numFuncao == 5:
                for i in range(len(self.alelos)):
                    valor_funcao += abs((cargas[i]/carga_media) - (self.alelos[i]/ef_media))
                self.func_objetivo = [valor_funcao]

            elif numFuncao == 6:
                for i in range(len(self.alelos)):
                    valor_funcao += abs((cargas[i]/self.alelos[i]) - (carga_media/ef_media))
                    self.func_objetivo = [valor_funcao]
        
        elif numFuncao == 7:
            for i in range(len(self.alelos)):
                for j in range(len(self.alelos[i])):
                    valor_funcao += vetor_pesos_difusa[j]*self.alelos[i][j]
            self.func_objetivo = [valor_funcao]
                
        elif numFuncao == 8:
            for i in range(len(scs.lista_subbacias)):
                area_total += scs.lista_subbacias[i].Area
                cargas = scs.calcula_matriz_cargas()
                # cargas = matriz [carga_DBO, carga_NTK, carga_NOX, carga_PINORG]

            for i in range(len(self.alelos)):
                for j in range(len(self.alelos[i])):
                    valor_funcao += (vetor_pesos_difusa[j]*cargas[i][j]*scs.lista_subbacias[i].Area*(1-self.alelos[i][j]))/area_total
            self.func_objetivo = [valor_funcao]

        return True