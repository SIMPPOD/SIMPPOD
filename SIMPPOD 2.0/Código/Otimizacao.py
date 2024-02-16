# -*- coding: utf-8 -*-
# Modulo: Otimizacao

from Populacao import Populacao
from QUAL_UFMG import QUAL_UFMG
from Leitura import *
from time import time
from NSGA2 import NSGA2

class Otimizacao:

    def __init__(self):
        self.matriz_reducao_pontual = []

    # Metodo que calcula a eficiencia minima de uma ete considerando apenas 120 mg de DBO podem entrar no curso d'agua
    @staticmethod
    def calcula_ef_minima(Rio, matriz_contribuicoes):
        ef_minima = []
        for i in range(len(matriz_contribuicoes)):
            if matriz_contribuicoes[i][11] == 1:  # se ExR = 1
                if i == 0 and matriz_contribuicoes[0][10] == 0:  # se N = 0 
                    ef = ((Rio.Qr * Rio.DBOr) + (matriz_contribuicoes[0][9] * matriz_contribuicoes[0][0]) - (5 * (Rio.Qr + matriz_contribuicoes[0][9]))) / (matriz_contribuicoes[0][9] * matriz_contribuicoes[0][0])
                    # ef = ( (Qr*DBOr) + (Qe*DBO5e) - (5*(Qr+Qe)) ) / (Qe*DBO5e)
                else:
                    ef = (matriz_contribuicoes[i][0] - 120)/matriz_contribuicoes[i][0]
                    # ef = (DBO5e - 120) / DBO5e
                            
                if ef < 0.6:
                    ef = 0.6
                    
                ef_minima.append(ef)

        return ef_minima
        
    # Metodo que executa a Otimização
    def executa(self, matriz_entradas, simula_difusa, modo_otimizacao, simulacao_curso, celula_entrada_tributarios):
        populacoes = []
        melhor_solucao = []
        melhores_solucoes = [] 
        historico = [] 
        historico_fo = []
        historico_tempo_iteracoes = []
        historico_filhos_invalidos = []
        iteracao_versao_rapida = None
        children = None
        evolution = None
        fim_rapida = None
        melhor_solucao_versao_rapida = None
        vetor_invalidos_rapida = None

        [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] = ler_entrada_otimizacao(matriz_entradas[0])
        [FO_pontual, FO_difusa] = [matriz_brkga[0][6], matriz_brkga[1][6]]

        cenario_base = QUAL_UFMG() 
        
        ini = time()
        
        if simula_difusa:
            print("Rodando otimização da poluição difusa...")

            [Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(matriz_entradas[0], simula_difusa)
            del matriz_reducao_pontual
            ef_minima = []

            cenario_sem_otimizacao = cenario_base.executa(matriz_entradas, simulacao_curso, Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, FO_difusa, matriz_tipo_contribuicoes, celula_entrada_tributarios)

            # Criação da população
            for i in range(int(matriz_brkga[1][1])):
                aux = Populacao(matriz_brkga[1][7], matriz_brkga[1][0], len(scs.sub_bacias), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[1][6], True, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes, matriz_entradas, simulacao_curso, celula_entrada_tributarios)
                # aux = Populacao(pe, tam_populacao, tam_cromossomo, Entrada_Pontual.txt, Rio, cenario_base, matriz_reducao_pontual, ef_minima, funcao objetivo, simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs)
                
                aux.ordena_populacao()
                aux.set_melhor_inicial() 
                populacoes.append(aux)
                print("Inválidos gerados na criação da população inicial difusa " + str(i+1) + ": " + str(aux.vetor_invalidos[0]))
            
            if modo_otimizacao == 4:
                NSGA2.NSGA2Utils.fast_nondominated_sort(aux)
                for front in aux.fronts: # para cada fronteira
                    NSGA2.Evolution.utils.calculate_crowding_distance(front) # calcula a distancia crowding de cada individuo na fronteira
                children = NSGA2.Evolution.utils.create_children(aux) # cria uma população de filhos de mesmo tamanho da população de pais

            # Execução das gerações
            for j in range(int(matriz_brkga[1][1])):
                contagem = 0
                for k in range(int(matriz_brkga[1][5])):
                    [melhor_solucao, vetor_invalidos, tempo_iteracao, total_filhos_invalidos] = populacoes[j].gera_prox_geracao(matriz_brkga[1][2], matriz_brkga[1][3], matriz_brkga[1][4], matriz_brkga[1][7], matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, scs, matriz_entradas, simulacao_curso, celula_entrada_tributarios, children)
                    # melhor_solucao = populacoes[j].gera_prox_geracao(NE, NC, NM, pe, Entrada_Pontual, Rio, cenario_base, matriz_reducao_pontual, scs)
                    print("Inválidos acumulados até a geração " + str(k+1) + ": " + str(vetor_invalidos))

                    historico.append(melhor_solucao)
                    historico_fo.append(melhor_solucao.func_objetivo)
                    historico_tempo_iteracoes.append(tempo_iteracao)
                    historico_filhos_invalidos.append(total_filhos_invalidos)
                    melhores_solucoes.append(melhor_solucao)

                    if k >= 5 and contagem == 0:
                        historico_fo_ordenadas = historico_fo.copy()
                        historico_fo_ordenadas.reverse()
                        historico_fo_ordenadas = historico_fo_ordenadas[0:5]
                        historico_fo_ordenadas.sort()
                        if 0.97*historico_fo_ordenadas[0] <= melhor_solucao.func_objetivo <= historico_fo_ordenadas[0]:
                            contagem = 1
                            fim_rapida = time()
                            iteracao_versao_rapida = k
                            print("Última iteração para versão rápida: " + str(k+1))
                            melhor_solucao_versao_rapida = melhores_solucoes[len(melhores_solucoes)-1]
                            vetor_invalidos_rapida = vetor_invalidos
            print("Otimização da poluição difusa encerrada.")

        else:
            print("Rodando otimização da poluição pontual...")
            [Rio, matriz_contribuicoes, self.matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(matriz_entradas[0], simula_difusa)
            ef_minima = self.calcula_ef_minima(Rio, matriz_contribuicoes)
            
            cenario_sem_otimizacao = cenario_base.executa(matriz_entradas, simulacao_curso, Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, FO_pontual, matriz_tipo_contribuicoes, celula_entrada_tributarios)
                                                        
            if self.matriz_reducao_pontual[1] == []:
                return [cenario_sem_otimizacao, None, None, None, tam_rio, tam_cel, None, None, None, None, None, None, ph, None, Rio]

            # Criação da população
            for i in range(int(matriz_brkga[0][1])):
                aux = Populacao(matriz_brkga[0][7], matriz_brkga[0][0], len(self.matriz_reducao_pontual[1]), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[0][6], simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes, matriz_entradas, simulacao_curso, celula_entrada_tributarios)
                # aux = Populacao(pe, tam_populacao, tam_cromossomo, Entrada_Pontual.txt, Rio, cenario_base, matriz_reducao_pontual, ef_minima, funcao objetivo, simula_difusa, vetor_pesos_pontual, vetor_difusa, scs)

                aux.ordena_populacao()
                aux.set_melhor_inicial()
                populacoes.append(aux)
                print("Inválidos gerados na criação da população inicial pontual " + str(i+1) + ": " + str(aux.vetor_invalidos[0]))

                if modo_otimizacao == 4:
                    problem = NSGA2.Problem([FO_pontual], 1, [(ef_minima,0.95), (0,0.95)], False, False)
                    NSGA2.NSGA2Utils.fast_nondominated_sort(aux)
                    for front in aux.fronts: # para cada fronteira
                        evolution = NSGA2.Evolution(problem, matriz_brkga[0][0], 2, 0.9, 2, 20)
                        evolution.utils.calculate_crowding_distance(front) # calcula a distancia crowding de cada individuo na fronteira
                    children = evolution.utils.create_children(aux.lista_individuos, matriz_contribuicoes, FO_pontual, vetor_pesos_pontual, vetor_pesos_difusa, scs, Rio, aux.vetor_invalidos, cenario_base, self.matriz_reducao_pontual, matriz_entradas, simulacao_curso, celula_entrada_tributarios, matriz_tipo_contribuicoes) # cria uma população de filhos de mesmo tamanho da população de pais
                    aux.lista_individuos.extend(children)
                      
            # Execução das gerações
            for j in range(int(matriz_brkga[0][1])):
                contagem = 0
                for k in range(int(matriz_brkga[0][5])):
                    [melhor_solucao, vetor_invalidos, tempo_iteracao, total_filhos_invalidos] = populacoes[j].gera_prox_geracao(matriz_brkga[0][2], matriz_brkga[0][3], matriz_brkga[0][4], matriz_brkga[0][7], matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, scs, matriz_entradas, simulacao_curso, celula_entrada_tributarios, children, evolution, aux.vetor_invalidos)
                    # melhor_solucao = populacoes[j].gera_prox_geracao(NE, NC, NM, pe, Entrada_Pontual, Rio, cenario_base, matriz_reducao_pontual, scs)
                    print("Inválidos acumulados até a geração " + str(k+1) + ": " + str(vetor_invalidos))

                    historico.append(melhor_solucao)
                    historico_fo.append(melhor_solucao.func_objetivo)
                    historico_tempo_iteracoes.append(tempo_iteracao)
                    historico_filhos_invalidos.append(total_filhos_invalidos)
                    melhores_solucoes.append(melhor_solucao)

                    if k >= 5 and iteracao_versao_rapida is None:
                        historico_fo_ordenadas = historico_fo.copy()
                        if historico_fo_ordenadas[-1][0] == historico_fo_ordenadas[-6][0]:
                            fim_rapida = time()
                            iteracao_versao_rapida = k
                            print("Última iteração para versão rápida: " + str(k+1))
                            melhor_solucao_versao_rapida = melhores_solucoes[len(melhores_solucoes)-1]
                            vetor_invalidos_rapida = vetor_invalidos                  
            print("Otimização da poluição pontual encerrada.")

        fim = time()
        tempo = fim-ini
        if fim_rapida is not None: tempo_rapida = fim_rapida-ini
        else: tempo_rapida = None
        return [cenario_sem_otimizacao, melhores_solucoes, tempo, tempo_rapida, tam_rio, tam_cel, vetor_invalidos, vetor_invalidos_rapida, historico_fo, historico_tempo_iteracoes, historico_filhos_invalidos, iteracao_versao_rapida, ph, melhor_solucao_versao_rapida, Rio]