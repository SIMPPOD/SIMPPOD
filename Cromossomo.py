# -*- coding: utf-8 -*-
# Modulo: Cromossomo

# Importacao de bibliotecas
from random import uniform
import numpy as np

def converte_float(valor):
    if valor.find("."):
        return valor.replace(".",",")

# Definicao da classe
class Cromossomo:

    # CONSTRUTOR
    def __init__(self, simula_difusa, tam_cromossomo):
        self.func_objetivo = 999999
        self.alelos = []
        self.alelos_codificados = []
        self.cenario = []
        self.simula_difusa = simula_difusa
        self.tam_cromossomo = tam_cromossomo

    # METODOS

    # Metodo que escreve a saida
    def Escreve_saida(self, caminho, tempo, vetor_invalidos):
        arq = open(caminho, "a+") 

        # Escrita do arquivo
        arq.write("Resultados da Otimização de Poluição Pontual: Identificação dos valores mínimos de redução necessários ao atendimento da classe de QA desejada \n")
        arq.write("Tempo de processamento (s):; " + converte_float(str(tempo)) + "\n")
        arq.write("Número de inválidos gerados:; " + str(vetor_invalidos) + "\n")

        if self.simula_difusa:
            arq.write("Eficiência de Tratamento/Redução:  \n\n")
            arq.write("ID subbacia; DBO; Amonia; Nitrito; P-inorg\n")
            for i in range(len(self.alelos)): 
                arq.write(str(self.cenario.sub_bacias[i].ID) + ";")
                for j in range(len(self.alelos[i])): 
                    arq.write(str(self.alelos[i][j]) + ";") 
                arq.write("\n")
        else:
            for i in range(len(self.alelos)): 
                arq.write("Eficiência de Tratamento/Redução:;" + converte_float(str(self.alelos[i])) + "\n")

        arq.write("Nota da F.O. para a melhor solucao:; " + converte_float(str(self.func_objetivo)) + "\n\n")
        arq.write("OBS: As eficiencias de tratamento/redução se encontram expressas em decimal.\n")
        arq.close()

    # Metodo que executa o QUAL_UFMG
    def exec_QualUFMG(self, qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes):
        if self.simula_difusa:
            self.cenario = qual_ufmg.executa(Rio, matriz_contribuicoes, matriz_reducao_pontual, True, self.alelos, scs, numFuncao, matriz_tipo_contribuicoes)
        else:
            matriz_reducao_pontual[0] = self.alelos
            matriz_reducao_difusa = []
            self.cenario = qual_ufmg.executa(Rio, matriz_contribuicoes, matriz_reducao_pontual, False, matriz_reducao_difusa, scs, numFuncao, matriz_tipo_contribuicoes)

    # Metodo que retorna a funcao objetivo
    def get_func_obj(self):
        return self.func_objetivo
        
    # Metodo que seta randomicamente os alelos de um cromossomo, respeitando sempre as eficiencias minimas pre estabelecidas
    def set_alelos_random(self, ef_minima, modo_otimizacao, numFuncao):
        if modo_otimizacao == 1 or modo_otimizacao == 2:
            aux = []

            # Fixar minimos e maximos de reducao
            if self.simula_difusa:
                for i in range(self.tam_cromossomo):
                    for j in range(4):
                        aux.append((round(uniform(0.0, 0.9), 4)))  # Numero randomico no intervalo [0, 0.9], com 4 casas decimais
                    self.alelos.append(aux)
                    aux = []
                # self.alelos = matriz tam_cromossomo x 4, com vetores de alelos

            else:
                if numFuncao == 5:
                    for i in range(self.tam_cromossomo):
                        aux.append((round(uniform(float(ef_minima[i]), 0.9), 4)))
                        aux.append((round(uniform(0.0, 0.9), 4)))
                        self.alelos.append(aux)
                        aux = []
                else:
                    for i in range(self.tam_cromossomo):
                        self.alelos.append((round(uniform(float(ef_minima[i]), 0.9), 4)))  # Numero randomico no intervalo [ef_minima, 0.9], com 4 casas decimais
                    # self.alelos = vetor tam_cromossomo x 1, com valores de alelos

        elif modo_otimizacao == 3:
            aux = []

            # Fixar minimos e maximos de reducao
            if self.simula_difusa:
                for i in range(self.tam_cromossomo):
                    for j in range(4):
                        aux.append((round(uniform(0.0, 1.0), 4)))  # Numero randomico no intervalo [0, 1], com 4 casas decimais
                    self.alelos_codificados.append(aux)
                    aux = []
                # self.alelos = matriz tam_cromossomo x 4, com vetores de alelos

            else:
                if numFuncao == 5:
                    for i in range(self.tam_cromossomo):
                        for j in range(2):
                            aux.append((round(uniform(0.0, 1.0), 4)))
                        self.alelos_codificados.append(aux)
                        aux = []
                else: 
                    for i in range(self.tam_cromossomo):
                        self.alelos_codificados.append((round(uniform(0.0, 1.0), 4)))  # Numero randomico no intervalo [0, 1], com 4 casas decimais
                    # self.alelos = vetor tam_cromossomo x 1, com valores de alelos

    # Metodo que seta os alelos com um vetor de reais previamente definido
    def set_alelos(self, alelos):
        self.alelos = alelos

    def decodificador(self, ef_minima, numFuncao):
        qtdAlelos = len(self.alelos_codificados)  # Numero de alelos no cromossomo
        intervalo_antes = 1/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 1]
        aux = []

        if numFuncao < 4 or numFuncao > 5:
            if self.simula_difusa:
                intervalo_depois = 0.9/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 0.9]
                for i in range(qtdAlelos): 
                    for j in range(4):
                        # Codificacao do alelo por regra de tres
                        aux.append(round((intervalo_depois*self.alelos_codificados[i][j])/intervalo_antes, 4)) 
                    self.alelos.append(aux)
                    aux = []              

            else:
                for i in range(qtdAlelos): 
                    intervalo_depois = (0.9 - float(ef_minima[i]))/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [ef_minima, 0.9]
                    # Codificacao do alelo por regra de tres
                    self.alelos.append(round((intervalo_depois*self.alelos_codificados[i])/intervalo_antes + ef_minima[i], 4)) 
        elif numFuncao == 4:
            intervalo_depois = 0.9/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [0, 0.9]
            for i in range(qtdAlelos):
                aux.append(round((intervalo_depois*self.alelos_codificados[i])/intervalo_antes, 4))
            self.alelos = aux
        elif numFuncao == 5:
            for i in range(qtdAlelos): 
                intervalo_depois = (0.9 - float(ef_minima[i]))/qtdAlelos  # Tamanho de cada sub intervalo dividido do intervalo [ef_minima, 0.9]
                # Codificacao do alelo por regra de tres
                aux.append(round((intervalo_depois*self.alelos_codificados[i][0])/intervalo_antes + ef_minima[i], 4))
                intervalo_depois = 0.9/qtdAlelos
                aux.append(round((intervalo_depois*self.alelos_codificados[i][1])/intervalo_antes, 4))
                self.alelos.append(aux)
                aux = []

    # Metodo que avalia a condicao do rio
    def isValido(self, Rio, numFuncao):
        if numFuncao < 4 or numFuncao > 5:
            if len(self.alelos) == 0: 
                return False
            elif self.simula_difusa:
                if Rio.classe == 1.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10 or self.cenario.Y_Pinorg[i] > 0.05:
                            # Se nitrito > 1 ou nitrato > 10 ou fosforo inorganico > 0.05
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 3.7:
                            # Se pH <= 7.5 e amonia > 3.7
                            return False
                        if 8 > Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 2:
                            # Se 7.5 < pH < 8 e amonia > 2
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 1:
                            # Se 8 < pH < 8.5 e amonia > 1
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 0.5:
                            # Se pH >= 8.5 e amonia > 0.5
                            return False
                elif Rio.classe == 2.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10:
                            # Se nitrito > 1 ou nitrato > 10
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 3.7:
                            # Se ph <= 7.5 e amonia > 3.7
                            return False
                        if 8 >= Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 50:
                            # Se 7.5 < pH <= 8 e amonia > 50
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 50:
                            # Se 8 < pH < 8.5 e amonia > 50
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 0.5:
                            # Se pH >= 8.5 e amonia > 0.5
                            return False
                elif Rio.classe == 3.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 1 or self.cenario.Y_Nnitra[i] > 10 or self.cenario.Y_Pinorg[i] > 0.075:
                            # Se nitrito > 1 ou nitrato > 10 ou fosforo inorganico > 0.075
                            return False
                        if Rio.PH <= 7.5 and self.cenario.Y_Namon[i] > 13.3:
                            # Se pH <= 7.5 e amonia > 13.3
                            return False
                        if 8 > Rio.PH > 7.5 and self.cenario.Y_Namon[i] > 5.6:
                            # Se 7.5 < pH < 8 e amonia > 5.6
                            return False
                        if 8.5 > Rio.PH > 8 and self.cenario.Y_Namon[i] > 2.2:
                            # Se 8 < pH < 8.5 e amonia > 2.2
                            return False
                        if Rio.PH >= 8.5 and self.cenario.Y_Namon[i] > 1:
                            # Se pH >= 8.5 e amonia > 1
                            return False
                elif Rio.classe == 4.0:
                    for i in range(len(self.cenario.Y_DBO)):
                        if self.cenario.Y_Nnitri[i] > 50 or self.cenario.Y_Nnitra[i] > 50 or self.cenario.Y_Pinorg[i] > 50:
                            # Se nitrito > 50 ou nitrato > 50 ou fosforo inorganico > 50
                            return False

            if Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 3 or self.cenario.Y_OD[i] < 6:
                        # Se DBO > 3 ou OD < 6
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 5 or self.cenario.Y_OD[i] <= 5:
                        # Se DBO > 5 ou OD <= 5
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 10 or self.cenario.Y_OD[i] < 4:
                        # Se DBO > 10 ou OD < 4
                        return False
            elif Rio.classe == 4.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 30 or self.cenario.Y_OD[i] < 2:
                        # Se DBO > 30 ou OD < 2
                        return False
            return True
        elif numFuncao == 4:
            if len(self.alelos) == 0:
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 3.7 com pH <= 7.5, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 2 com 7.5 <= pH <= 8.0, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 1 com 8.0 <= pH <= 8.5, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 0.5 com pH > 8.5, ou OD < 6
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 3.7 com pH <= 7.5, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 2 com 7.5 <= pH <= 8.0, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 1 com 8.0 <= pH <= 8.5, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 0.5 com pH > 8.5, ou OD < 5
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 13.3 and Rio.PH <= 7.5): # or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 13.3 com pH <= 7.5, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 5.6 and 7.5 <= Rio.PH <= 8.0): # or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 5.6 com 7.5 <= pH <= 8.0, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2.2 and 8.0 <= Rio.PH <= 8.5): # or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 2.2 com 8.0 <= pH <= 8.5, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1.0 and Rio.PH > 8.5): # or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 1.0 com pH > 8.5, ou OD < 4
                        return False
            elif Rio.classe == 4.0:
                return False
                
            return True
        elif numFuncao == 5:
            if len(self.alelos) == 0:
                return False
            elif Rio.classe == 1.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 3 or self.cenario.Y_OD[i] < 6:
                        # Se DBO > 3 ou OD < 6
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5) or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 3.7 com pH <= 7.5, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0) or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 2 com 7.5 <= pH <= 8.0, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5) or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 1 com 8.0 <= pH <= 8.5, ou OD < 6
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5) or self.cenario.Y_OD[i] < 6:
                        # Se Namon >= 0.5 com pH > 8.5, ou OD < 6
                        return False
            elif Rio.classe == 2.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 5 or self.cenario.Y_OD[i] <= 5:
                        # Se DBO > 5 ou OD <= 5
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 3.7 and Rio.PH <= 7.5) or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 3.7 com pH <= 7.5, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2 and 7.5 <= Rio.PH <= 8.0) or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 2 com 7.5 <= pH <= 8.0, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1 and 8.0 <= Rio.PH <= 8.5) or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 1 com 8.0 <= pH <= 8.5, ou OD < 5
                        return False
                    elif (self.cenario.Y_Namon[i] >= 0.5 and Rio.PH > 8.5) or self.cenario.Y_OD[i] < 5:
                        # Se Namon >= 0.5 com pH > 8.5, ou OD < 5
                        return False
            elif Rio.classe == 3.0:
                for i in range(len(self.cenario.Y_DBO)):
                    if self.cenario.Y_DBO[i] > 10 or self.cenario.Y_OD[i] < 4:
                        # Se DBO > 10 ou OD < 4
                        return False
                for i in range(len(self.cenario.Y_Namon)):
                    if (self.cenario.Y_Namon[i] >= 13.3 and Rio.PH <= 7.5) or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 13.3 com pH <= 7.5, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 5.6 and 7.5 <= Rio.PH <= 8.0) or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 5.6 com 7.5 <= pH <= 8.0, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 2.2 and 8.0 <= Rio.PH <= 8.5) or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 2.2 com 8.0 <= pH <= 8.5, ou OD < 4
                        return False
                    elif (self.cenario.Y_Namon[i] >= 1.0 and Rio.PH > 8.5) or self.cenario.Y_OD[i] < 4:
                        # Se Namon >= 1.0 com pH > 8.5, ou OD < 4
                        return False
            return True

    # Metodo que calcula a funcao objetivo com base no valor da equacao pre estabelecido
    def avalia_func_objetivo(self, matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs):
        cargas = []
        valor_funcao = 0
        carga_media = 0
        area_total = 0

        # Funcao simples que minimiza apenas as eficiencias sem medida de equidade
        if numFuncao == 1 or numFuncao == 4:
            self.func_objetivo = sum(self.alelos) 

        # Duas proximas funcoes objetivas utilizam os valores de carga media e de eficiencia media do cromossomo
        elif numFuncao == 2 or numFuncao == 3:
            # Construcao do vetor de cargas e calculo da carga media
            ef_media = ((sum(self.alelos))/len(self.alelos))  
            for j in range(len(matriz_contribuicoes)): 
                if matriz_contribuicoes[j][10] == 1:  # Se ExR for 1
                    carga = matriz_contribuicoes[j][8]*matriz_contribuicoes[j][0]  # Qe * DBO5e
                    cargas.append(carga)
                    carga_media += carga
                # cargas = vetor com Qe*DBO5e
                # carga_media = soma de Qe*DBO5E

                carga_media = carga_media/(len(cargas))

            if numFuncao == 2:
                for i in range(len(self.alelos)):
                    valor_funcao += abs((cargas[i]/carga_media) - (self.alelos[i]/ef_media))
                    # valor absoluto da i-esima carga pela carga media, menos o valor do i-esimo alelo pela eficiencia media
                self.func_objetivo = valor_funcao

            elif numFuncao == 3:
                for i in range(len(self.alelos)):
                    valor_funcao += abs((cargas[i]/self.alelos[i]) - (carga_media/ef_media))
                    # valor absoluto da i-esima carga pelo i-esimo alelo, menos o valor da carga media pela eficiencia media
                    self.func_objetivo = valor_funcao
            
        elif numFuncao == 5:
            for i in range(self.tam_cromossomo):
                valor_funcao += (vetor_pesos_pontual[0]*self.alelos[i][0]) + (vetor_pesos_pontual[1]*self.alelos[i][1])
            self.func_objetivo = valor_funcao
        
        elif numFuncao == 6: 
            for i in range(len(self.alelos)):
                for j in range(len(self.alelos[i])):
                    valor_funcao += vetor_pesos_difusa[j]*self.alelos[i][j]
            self.func_objetivo = valor_funcao
                
        elif numFuncao == 7:
            for i in range(len(scs.lista_subbacias)):
                area_total += scs.lista_subbacias[i].Area  # area da i-esima subbacia
                cargas = scs.calcula_matriz_cargas()
                # cargas = matriz [carga_DBO, carga_NTK, carga_NOX, carga_PINORG]

            for i in range(len(self.alelos)):
                for j in range(len(self.alelos[i])):
                    valor_funcao += (vetor_pesos_difusa[j]*cargas[i][j]*scs.lista_subbacias[i].Area*(1-self.alelos[i][j]))/area_total
            self.func_objetivo = valor_funcao

        return True