# -*- coding: utf-8 -*-
# Modulo: Populacao

from Cromossomo import Cromossomo
from random import uniform, randint
from NSGA2 import NSGA2
import random
import time

class Populacao:

    def __init__(self, pe, tam_populacao, tam_cromossomo, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual,
                 ef_minima, numFuncao, simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao,
                 matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios):
        self.ef_minima = ef_minima 
        self.tam_populacao = int(tam_populacao)
        self.tam_cromossomo = int(tam_cromossomo) 
        self.lista_individuos = []
        self.melhor_individuo_inicial = []
        self.vetor_invalidos = [0, 0, 0]  # [individuos, filhos, mutantes]
        self.pe = pe  # porcentagem da populacao total que sera elite
        self.numFuncao = int(numFuncao)
        self.simula_difusa = simula_difusa  # booleano para modo de execucao (se pontual ou difuso)
        self.modo_otimizacao = modo_otimizacao
        self.vetor_pesos_pontual = vetor_pesos_pontual
        self.vetor_pesos_difusa = vetor_pesos_difusa
        self.matriz_tipo_contribuicoes = matriz_tipo_contribuicoes
        if modo_otimizacao == 4:
            self.fronts = None

        tempo_inicial = time.time()
        while len(self.lista_individuos) < int(tam_populacao):
            individuo = Cromossomo(simula_difusa, tam_cromossomo)
            individuo.set_alelos_random(ef_minima, modo_otimizacao, numFuncao)
            if modo_otimizacao == 3: individuo.decodificador(ef_minima, numFuncao)
            individuo.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)
            if individuo.isValido(Rio, numFuncao):
                individuo.avalia_func_objetivo(matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs)
                self.lista_individuos.append(individuo)
            else: 
                self.vetor_invalidos[0] += 1
        tempo_final = time.time()
        print("Tempo de criação da população inicial = " + str(tempo_final-tempo_inicial))

    def ordena_populacao(self):
        self.lista_individuos = sorted(self.lista_individuos, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO

    def cruzamento(self, ind1, ind2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios):
        filhos_invalidos = 0
        if self.modo_otimizacao == 1:
            if self.simula_difusa: 
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)  # Criacao de um novo filho
                    alelos_sub = []

                    for i in range(self.tam_cromossomo): 
                        alelos_sub = []
                        ponto_corte = randint(0,3)
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
                    
                        alelos_filho.append(alelos_sub)

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)  # Seta o cenario

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1
                        filhos_invalidos += 1
                    else:
                        break
            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)
                    alelos_filho = []
                    ponto_corte = randint(0,self.tam_cromossomo-1)
                    if self.numFuncao == 3:
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

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios) 

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1 
                        filhos_invalidos += 1
                    else:
                        break

        elif self.modo_otimizacao == 2:
            if self.simula_difusa:
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo) 
                    for i in range(self.tam_cromossomo):
                        alelos_sub = []
                        for j in range(5):
                            aux = uniform(0.0, 1.0)
                            if aux < pe:
                                alelos_sub.append(ind1.alelos[i][j])
                            else:
                                alelos_sub.append(ind2.alelos[i][j])
                        alelos_filho.append(alelos_sub)

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1
                        filhos_invalidos += 1
                    else:
                        break

            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)
                    alelos_filho = []
                    if self.numFuncao == 3:
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
                            aux = uniform(0.0, 1.0) 
                    
                            if aux < pe:
                                alelos_filho.append(ind1.alelos[i])
                            else:
                                alelos_filho.append(ind2.alelos[i])

                    filho.set_alelos(alelos_filho)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1
                        filhos_invalidos += 1
                    else:
                        break

        elif self.modo_otimizacao == 3:
            if self.simula_difusa:
                while True:
                    alelos_filho = []
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)
                    for i in range(self.tam_cromossomo):
                        alelos_sub = []
                        for j in range(5):
                            aux = uniform(0.0, 1.0) 

                            if aux < pe:
                                alelos_sub.append(ind1.alelos_codificados[i][j])
                            else:
                                alelos_sub.append(ind2.alelos_codificados[i][j])
                        alelos_filho.append(alelos_sub)

                    filho.alelos_codificados = alelos_filho
                    filho.decodificador(self.ef_minima, self.numFuncao)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)

                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1 
                        filhos_invalidos += 1
                    else:
                        break

            else:
                while True:
                    filho = Cromossomo(self.simula_difusa, self.tam_cromossomo)
                    alelos_filho = []
                    if self.numFuncao == 3:
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
                            aux = uniform(0.0, 1.0)
                    
                            if aux < pe:
                                alelos_filho.append(ind1.alelos_codificados[i])
                            else:
                                alelos_filho.append(ind2.alelos_codificados[i])

                    filho.alelos_codificados = alelos_filho
                    filho.decodificador(self.ef_minima, self.numFuncao)
                    filho.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)
                    if not filho.isValido(Rio, self.numFuncao):
                        self.vetor_invalidos[1] += 1
                        filhos_invalidos += 1
                    else:
                        break

        filho.avalia_func_objetivo(matriz_contribuicoes, self.numFuncao, self.vetor_pesos_pontual, self.vetor_pesos_difusa, scs)

        return [filho, filhos_invalidos]

    def gera_mutante(self, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios):
        mutante = Cromossomo(self.simula_difusa, self.tam_cromossomo) 
        mutante.set_alelos_random(self.ef_minima, self.modo_otimizacao, self.numFuncao) 
        if self.modo_otimizacao == 3:
            mutante.decodificador(self.ef_minima, self.numFuncao)
        mutante.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios) 

        while not mutante.isValido(Rio, self.numFuncao):
            self.vetor_invalidos[2] += 1
            mutante = Cromossomo(self.simula_difusa, self.tam_cromossomo)
            mutante.set_alelos_random(self.ef_minima, self.modo_otimizacao, self.numFuncao)
            if self.modo_otimizacao == 3:
                mutante.decodificador(self.ef_minima, self.numFuncao)
            mutante.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, self.numFuncao, self.matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios) 

        mutante.avalia_func_objetivo(matriz_contribuicoes, self.numFuncao, self.vetor_pesos_pontual, self.vetor_pesos_difusa, scs)

        return mutante

    # Metodo que escolhe um individuo da populacao para realizar o cruzamento
    def escolhe_individuo(self, NE, isElite):
        if self.modo_otimizacao == 1:
            aux = randint(0, len(self.lista_individuos)-1)
            return self.lista_individuos[aux]
        elif self.modo_otimizacao == 2 or self.modo_otimizacao == 3 or self.modo_otimizacao == 4:
            if isElite:
                aux2 = randint(0, NE * self.tam_populacao)  # Escolhe randomicamente um individuo da elite
                return self.lista_individuos[aux2]
            else:
                aux2 = randint(NE * self.tam_populacao, (self.tam_populacao - 1))  # Escolhe randomicamente um individuo da nao-elite
                return self.lista_individuos[aux2]

    def set_melhor_inicial(self):
        self.melhor_individuo_inicial = self.lista_individuos[0]
      
    def gera_prox_geracao(self, NE, NC, NM, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios, children, evolution, vetor_invalidos):
        tempo_inicial = time.time()
        total_filhos_invalidos = 0
        
        if self.modo_otimizacao == 1:
            cruzamentos = []  # Lista de filhos de cruzamentos entre um elite e um nao-elite
            mutantes = []

            for i in range(int((NC+NE)*self.tam_populacao)):  # i varia de 0 ao tamanho da populacao da nao-elite
                individuo1 = self.escolhe_individuo(None, None) 
                individuo2 = self.escolhe_individuo(None, None) 
                
                [filho, filhos_invalidos] = self.cruzamento(individuo1, individuo2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios)
                total_filhos_invalidos += filhos_invalidos
                cruzamentos.append(filho)

            for i in range(int(NM * self.tam_populacao)):  # i varia de 0 ao tamanho da populacao mutante
                mutantes.append(self.gera_mutante(matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios))

            nova_geracao = cruzamentos + mutantes 
            nova_geracao = sorted(nova_geracao, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO
            self.lista_individuos = nova_geracao
            melhor_solucao = self.lista_individuos[0]

        elif self.modo_otimizacao == 2 or self.modo_otimizacao == 3:
            elite = [] 
            cruzamentos = []  # Lista de filhos de cruzamentos entre um elite e um nao-elite
            mutantes = [] 

            for i in range(int(NE * self.tam_populacao)):
                elite.append(self.lista_individuos[i]) 

            for i in range(int(NC * self.tam_populacao)):
                individuo1 = self.escolhe_individuo(NE, True)  # Escolhe um individuo da elite
                individuo2 = self.escolhe_individuo(NE, False)  # Escolhe um individuo da nao-elite

                [filho, filhos_invalidos] = self.cruzamento(individuo1, individuo2, pe, matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios)
                total_filhos_invalidos += filhos_invalidos
                cruzamentos.append(filho)

            for i in range(int(NM * self.tam_populacao)):
                mutantes.append(self.gera_mutante(matriz_contribuicoes, Rio, qual_ufmg, matriz_reducao_pontual, scs, caminho_curso, simulacao_curso, celula_entrada_tributarios))

            nova_geracao = elite + cruzamentos + mutantes 
            nova_geracao = sorted(nova_geracao, key=Cromossomo.get_func_obj)  # Ordena a populacao pela FO
            self.lista_individuos = nova_geracao
            melhor_solucao = self.lista_individuos[0]
        
        elif self.modo_otimizacao == 4:
            self.population = NSGA2.Population(self.lista_individuos) # pais e filhos
            evolution.utils.fast_nondominated_sort(self.population) # monta as novas fronteiras
            new_population = NSGA2.Population([]) # cria uma população auxiliar vazia
            front_num = 0 # numero da fronteira a ser analisada
            while front_num + 1 < len(self.population.fronts) and len(new_population.lista_individuos) + len(self.population.fronts[front_num]) <= self.tam_populacao: # enquanto a soma da nova população com os individous da fronteira for menor que o tamanho desejado
                evolution.utils.calculate_crowding_distance(self.population.fronts[front_num]) # calcula a distancia crowding de cada individuo da fronteira
                new_population.lista_individuos.extend(self.population.fronts[front_num]) # faz a união da nova população com os individuos dessa fronteira
                front_num += 1 # passa para a próxima fronteira
            evolution.utils.calculate_crowding_distance(self.population.fronts[front_num]) # calcula a distancia crowding dos melhores individuos 
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True) # ordena a próxima fronteira de forma decrescente no valor de distancia crowding
            new_population.lista_individuos.extend(self.population.fronts[front_num][0:self.tam_populacao - len(new_population.lista_individuos)]) # adiciona os individuos com maiores distancia crowding
            returned_population = self.population # retorna a populacao de pais e filhos
            self.population = new_population # atualiza a proxima geração com os individuos das primeiras fronteiras e com os de maior distancia crowding
            evolution.utils.fast_nondominated_sort(self.population) # monta as novas fronteiras da nova geração
            for front in self.population.fronts: # para cada nova fronteira
                evolution.utils.calculate_crowding_distance(front) # calcula a distancia crowding de cada individuo na fronteira
            children = evolution.utils.create_children(self.population.lista_individuos, matriz_contribuicoes, self.numFuncao, self.vetor_pesos_pontual, self.vetor_pesos_difusa, scs, Rio, vetor_invalidos, qual_ufmg, matriz_reducao_pontual, caminho_curso, simulacao_curso, celula_entrada_tributarios, self.matriz_tipo_contribuicoes) # cria os filhos da nova geração
            
            arquivo = "./saidas.csv"
            arq = open(arquivo, "a+")
            for i in range(len(returned_population.fronts)):
                arq.write("Front " + str(i) + " = ")
                for individuo in returned_population.fronts[i]:
                    arq.write(str(individuo.func_objetivo) + " ")
                arq.write("\n")
            arq.write("\n")

            melhor_solucao = returned_population.fronts[0][0]
            total_filhos_invalidos += vetor_invalidos[1]
            self.population.lista_individuos.extend(children)
            self.lista_individuos = self.population.lista_individuos
            
        tempo_final = time.time()

        return [melhor_solucao, self.vetor_invalidos, tempo_final-tempo_inicial, total_filhos_invalidos]