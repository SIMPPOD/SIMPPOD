# -*- coding: utf-8 -*-
# Modulo: Populacao

# Importacao de bibliotecas
from Cromossomo import Cromossomo
from random import uniform, randint
import random
import time

# Definicao da classe
class Populacao:

    # CONSTRUTOR
    def __init__(self, pe, tam_populacao, tam_cromossomo, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual,
                 ef_minima, numFuncao, simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes):
        self.ef_minima = ef_minima  # vetor com eficiencias minimas calculadas
        self.tam_populacao = int(tam_populacao)  # tam_populacao = matriz_brkga[1][0] -> numero de cromossomos na populacao
        self.tam_cromossomo = int(tam_cromossomo)  # numero de alelos por cromossomo
        self.lista_individuos = []  # populacao ordenada pelas FOs
        self.melhor_individuo_inicial = []  # primeiro individuo da populacao ordenada (individuo de menor FO)
        self.vetor_invalidos = [0, 0, 0]  # [individuos, filhos, mutantes]
        self.pe = pe  # porcentagem da populacao total que sera elite
        self.numFuncao = int(numFuncao)
        self.simula_difusa = simula_difusa  # booleano para modo de execucao (se pontual ou difuso)
        self.modo_otimizacao = modo_otimizacao
        self.vetor_pesos_pontual = vetor_pesos_pontual
        self.vetor_pesos_difusa = vetor_pesos_difusa
        self.matriz_tipo_contribuicoes = matriz_tipo_contribuicoes

        tempo_inicial = time.time()
        for i in range(int(tam_populacao)):  # Para cada individuo na populacao
            individuo = Cromossomo(simula_difusa, tam_cromossomo)  # Criacao de um individuo para a populacao
            individuo.set_alelos_random(ef_minima, modo_otimizacao, numFuncao)  # Seta randomicamente os alelos do individuo (cracao das chaves aleatorias)
            if modo_otimizacao == 3:
                individuo.decodificador(ef_minima, numFuncao)
            individuo.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes)  # Seta o cenario

            while not individuo.isValido(Rio, numFuncao):  # Enquanto o individuo for invalido
                self.vetor_invalidos[0] += 1  # Acrescenta 1 ao numero de individuos invalidos
                individuo = Cromossomo(simula_difusa, tam_cromossomo)  # Criacao de um novo individuo para a populacao
                individuo.set_alelos_random(ef_minima, modo_otimizacao, numFuncao)  # Seta randomicamente os alelos dos individuos (criacao das chaves aleatorias)
                if modo_otimizacao == 3:
                    individuo.decodificador(ef_minima, numFuncao)
                individuo.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes)  # Seta o cenario

            # Calcula a funcao objetivo com base no numFuncao
            individuo.avalia_func_objetivo(matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs)
            # individuo.alelos = matriz tam_cromossomo x 4 (difusa), ou tam_cromossomo x 1 (nao difusa)

            self.lista_individuos.append(individuo)  # Acrescenta o individuo a populacao
            # self.lista.individuos = lista no tam_populacao (no caso, 100 individuos)
        # self.lista_individuos = populacao total criada
        tempo_final = time.time()
        print("Tempo de criação da população inicial = " + str(tempo_final-tempo_inicial))

    # METODOS

    # Metodo que ordena a populacao
    def ordena_populacao(self):
        self.lista_individuos = sorted(self.lista_individuos, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO
        # self.lista_individuos = lista ordenada por crescencia da FO dos individuos

    # Metodo que realiza o cruzamento entre a populacao
    def cruzamento(self, ind1, ind2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs):
        filhos_invalidos = 0
        if self.modo_otimizacao == 1:
            if self.simula_difusa:  # Se simula_difusa for True
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    alelos_sub = []

                    for i in range(self.tam_cromossomo):  # Para cada vetor de alelos do individuo
                        alelos_sub = []
                        ponto_corte = randint(0,3)  # Numero inteiro randomico no intervalo [0,3]  int(random.random()*4)
                        if random.random() < 0.5:
                            for k in range(0,ponto_corte):
                                alelos_sub.append(ind1.alelos[i][k])  # Filho herda [0, ponto de corte] do pai 1
                            for k in range(ponto_corte,len(ind2.alelos[i])):
                                alelos_sub.append(ind2.alelos[i][k])  # Filho herda [ponto de corte:] do pai 2
                        else:
                            for k in range(0,ponto_corte):
                                alelos_sub.append(ind2.alelos[i][k])  # Filho herda [0, ponto de corte] do pai 2
                            for k in range(ponto_corte,len(ind1.alelos[i])):
                                alelos_sub.append(ind1.alelos[i][k])  # Filho herda [ponto de corte:] do pai 1
                    
                        # alelos_sub = lista de tamanho 4
                        alelos_filho.append(alelos_sub)
                    # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos
                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break
            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    alelos_filho = []
                    ponto_corte = randint(0,self.tam_cromossomo-1)  # int(random.random()*self.tam_cromossomo)
                    if self.numFuncao == 5:
                        alelos_sub = []
                        if random.random() < 0.5:
                            for i in range(0,ponto_corte):
                                alelos_sub.append(ind1.alelos[i][0])
                                alelos_sub.append(ind1.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                            for i in range(ponto_corte,len(ind2.alelos)):
                                alelos_sub.append(ind2.alelos[i][0])
                                alelos_sub.append(ind2.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                        else:
                            for i in range(0,ponto_corte):
                                alelos_sub.append(ind2.alelos[i][0])
                                alelos_sub.append(ind2.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                            for i in range(ponto_corte,len(ind1.alelos)):
                                alelos_sub.append(ind1.alelos[i][0])
                                alelos_sub.append(ind1.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                    else:
                        if random.random() < 0.5:
                            for i in range(0,ponto_corte):
                                alelos_filho.append(ind1.alelos[i])
                            for i in range(ponto_corte,len(ind2.alelos)):
                                alelos_filho.append(ind2.alelos[i])
                        else:
                            for i in range(0,ponto_corte):
                                alelos_filho.append(ind2.alelos[i])
                            for i in range(ponto_corte,len(ind1.alelos)):
                                alelos_filho.append(ind1.alelos[i])
                        # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos
                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break

        elif self.modo_otimizacao == 2:
            if self.simula_difusa:
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    for i in range(self.tam_cromossomo):
                        alelos_sub = []
                        for j in range(4):
                            aux = uniform(0.0, 1.0)  # Numero aleatorio no intervalo [0.0, 1.0]

                            # Acrescenta a j-esima posicao do alelo do i-esimo individuo da populacao
                            if aux < pe:
                                alelos_sub.append(ind1.alelos[i][j])
                            else:
                                alelos_sub.append(ind2.alelos[i][j])
                        # alelos_sub = lista de tamanho 4
                        alelos_filho.append(alelos_sub)
                    # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break

            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    alelos_filho = []
                    if self.numFuncao == 5:
                        alelos_sub = []
                        for i in range(self.tam_cromossomo):
                            aux = uniform(0.0, 1.0)
                            if aux < pe:
                                alelos_sub.append(ind1.alelos[i][0])
                                alelos_sub.append(ind1.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                            else:
                                alelos_sub.append(ind2.alelos[i][0])
                                alelos_sub.append(ind2.alelos[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []

                    else:
                        for i in range(self.tam_cromossomo):
                            aux = uniform(0.0, 1.0)  # Numero aleatorio no intervalo [0.0, 1.0]
                    
                            # Acrescenta o alelo do i-esimo individuo da populacao
                            if aux < pe:
                                alelos_filho.append(ind1.alelos[i])
                            else:
                                alelos_filho.append(ind2.alelos[i])
                        # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break

        elif self.modo_otimizacao == 3:
            if self.simula_difusa:
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    for i in range(self.tam_cromossomo):
                        alelos_sub = []
                        for j in range(4):
                            aux = uniform(0.0, 1.0)  # Numero aleatorio no intervalo [0.0, 1.0]

                            # Acrescenta a j-esima posicao do alelo do i-esimo individuo da populacao
                            if aux < pe:
                                alelos_sub.append(ind1.alelos_codificados[i][j])
                            else:
                                alelos_sub.append(ind2.alelos_codificados[i][j])
                        # alelos_sub = lista de tamanho 4
                        alelos_filho.append(alelos_sub)
                    # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos

                    filho.alelos_codificados = alelos_filho
                    filho.decodificador(self.ef_minima, self.numFuncao)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break

            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    alelos_filho = []
                    if self.numFuncao == 5:
                        alelos_sub = []
                        for i in range(self.tam_cromossomo):
                            aux = uniform(0.0, 1.0)
                            if aux < pe:
                                alelos_sub.append(ind1.alelos_codificados[i][0])
                                alelos_sub.append(ind1.alelos_codificados[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                            else:
                                alelos_sub.append(ind2.alelos_codificados[i][0])
                                alelos_sub.append(ind2.alelos_codificados[i][1])
                                alelos_filho.append(alelos_sub)
                                alelos_sub = []
                    else:
                        for i in range(self.tam_cromossomo):
                            aux = uniform(0.0, 1.0)  # Numero aleatorio no intervalo [0.0, 1.0]
                    
                            # Acrescenta o alelo do i-esimo individuo da populacao
                            if aux < pe:
                                alelos_filho.append(ind1.alelos_codificados[i])
                            else:
                                alelos_filho.append(ind2.alelos_codificados[i])
                        # alelos_filho = matriz tam_cromossomo x 4, com lista de alelos

                    filho.alelos_codificados = alelos_filho
                    filho.decodificador(self.ef_minima, self.numFuncao)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1  # Acrescenta 1 ao numero de filhos invalidos
                        filhos_invalidos += 1
                    else:
                        break

        # Calcula a funcao objetivo com base no numFuncao
        filho.avalia_func_objetivo(matriz_contribuicoes, self.numFuncao, self.vetor_pesos_pontual, self.vetor_pesos_difusa, scs)

        return [filho, filhos_invalidos]

    # Metodo que gera mutante na populacao
    def gera_mutante(self, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs):
        mutante = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um mutante
        mutante.set_alelos_random(self.ef_minima, self.modo_otimizacao, self.numFuncao)  # Seta randomicamente os alelos do mutante
        if self.modo_otimizacao == 3:
            mutante.decodificador(self.ef_minima, self.numFuncao)
        mutante.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

        while not mutante.isValido(Rio, self.numFuncao):  # Enquanto o mutante for invalido
            self.vetor_invalidos[2] += 1  # Acrescenta 1 ao numero de mutantes invalidos
            mutante = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo mutante
            mutante.set_alelos_random(self.ef_minima, self.modo_otimizacao, self.numFuncao)  # Seta randomicamente os alelos do mutante
            if self.modo_otimizacao == 3:
                mutante.decodificador(self.ef_minima, self.numFuncao)
            mutante.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes)  # Seta o cenario

        # Calcula a funcao objetivo com base no numFuncao
        mutante.avalia_func_objetivo(matriz_contribuicoes, self.numFuncao, self.vetor_pesos_pontual, self.vetor_pesos_difusa, scs)

        return mutante

    # Metodo que escolhe um individuo da populacao para realizar o cruzamento
    def escolhe_individuo(self, NE, isElite):
        if self.modo_otimizacao == 1:
            aux = randint(0, len(self.lista_individuos)-1)
            return self.lista_individuos[aux]
        elif self.modo_otimizacao == 2 or self.modo_otimizacao == 3:
            if isElite:
                aux2 = randint(0, NE * self.tam_populacao)  # Escolhe randomicamente um individuo da elite
                return self.lista_individuos[aux2]
            else:
                aux2 = randint(NE * self.tam_populacao, (self.tam_populacao - 1))  # Escolhe randomicamente um individuo da nao-elite
                return self.lista_individuos[aux2]

    # Metodo que seta o melhor individuo da populacao
    def set_melhor_inicial(self):
        self.melhor_individuo_inicial = self.lista_individuos[0]

    # Metodo que gera a proxima geracao da populacao       
    def gera_prox_geracao(self, NE, NC, NM, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs):
        tempo_inicial = time.time()
        total_filhos_invalidos = 0
        
        if self.modo_otimizacao == 1:
            cruzamentos = []  # Lista de filhos de cruzamentos entre um elite e um nao-elite
            mutantes = []  # Lista de mutantes da populacao

            for i in range(int((NC+NE)*self.tam_populacao)):  # i varia de 0 ao tamanho da populacao da nao-elite
                individuo1 = self.escolhe_individuo(None, None)  # Escolhe um individuo da populacao
                individuo2 = self.escolhe_individuo(None, None)  # Escolhe um individuo da populacao
                
                # Realiza o cruzamento entre os individuos criados
                [filho, filhos_invalidos] = self.cruzamento(individuo1, individuo2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs)
                total_filhos_invalidos += filhos_invalidos
                cruzamentos.append(filho)
                # cruzamentos = lista com filhos entre um elite e um nao-elite

            for i in range(int(NM * self.tam_populacao)):  # i varia de 0 ao tamanho da populacao mutante
                # Gera um mutante na populacao
                mutantes.append(self.gera_mutante(matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs))
                # mutantes = lista com mutantes gerados

            nova_geracao = cruzamentos + mutantes  # nova_geracao = lista com todos os individuos gerados
            nova_geracao = sorted(nova_geracao, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO
            self.lista_individuos = nova_geracao

        elif self.modo_otimizacao == 2 or self.modo_otimizacao == 3:
            elite = []  # Lista de individuos da elite
            cruzamentos = []  # Lista de filhos de cruzamentos entre um elite e um nao-elite
            mutantes = []  # Lista de mutantes da populacao

            for i in range(int(NE * self.tam_populacao)):
                elite.append(self.lista_individuos[i])  # Adiciona individuo da elite

            for i in range(int(NC * self.tam_populacao)):
                individuo1 = self.escolhe_individuo(NE, True)  # Escolhe um individuo da elite
                individuo2 = self.escolhe_individuo(NE, False)  # Escolhe um individuo da nao-elite

                # Realiza o cruzamento entre os individuos criados
                [filho, filhos_invalidos] = self.cruzamento(individuo1, individuo2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs)
                total_filhos_invalidos += filhos_invalidos
                cruzamentos.append(filho)
                # cruzamentos = lista com filhos entre um elite e um nao-elite

            for i in range(int(NM * self.tam_populacao)):
                # Gera um mutante na populacao
                mutantes.append(self.gera_mutante(matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs))
                # mutantes = lista com mutantes gerados

            nova_geracao = elite + cruzamentos + mutantes  # nova_geracao = lista com todos os individuos gerados
            nova_geracao = sorted(nova_geracao, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO
            self.lista_individuos = nova_geracao

        melhor_solucao = self.lista_individuos[0]  # Seleciona o melhor individuo da populacao
        tempo_final = time.time()

        return [melhor_solucao, self.vetor_invalidos, tempo_final-tempo_inicial, total_filhos_invalidos]
