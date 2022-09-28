# -*- coding: utf-8 -*-
# Modulo: Otimizacao

# Importacao de bibliotecas
from asyncio.windows_events import NULL
from Populacao import Populacao
from QUAL_UFMG import QUAL_UFMG
from Leitura import *
from time import time

# Definicao da classe
class Otimizacao:
    
    # CONSTRUTOR
    def __init__(self):
        self.matriz_reducao_pontual = []

    # METODOS

    # Metodo que calcula a eficiencia minima de uma ete considerando apenas 120 mg de DBO podem entrar no curso d'agua
    @staticmethod
    def calcula_ef_minima(Rio, matriz_contribuicoes):
        ef_minima = []
        for i in range(len(matriz_contribuicoes)):  # para cada linha do arquivo
            if matriz_contribuicoes[i][10] == 1:  # se ExR = 1
                if i == 0 and matriz_contribuicoes[0][9] == 0:  # se N = 0 na primeira linha
                    ef = ((Rio.Qr * Rio.DBOr) + (matriz_contribuicoes[0][8] * matriz_contribuicoes[0][0]) - (5 * (Rio.Qr + matriz_contribuicoes[0][8]))) / (matriz_contribuicoes[0][8] * matriz_contribuicoes[0][0])
                    # ef = ( (Qr*DBOr) + (Qe*DBO5e) - (5*(Qr+Qe)) ) / (Qe*DBO5e)
                else:
                    ef = (matriz_contribuicoes[i][0] - 120)/matriz_contribuicoes[i][0]
                    # ef = (DBO5e - 120) / DBO5e
                            
                if ef < 0.6:
                    ef = 0.6
                    
                ef_minima.append(ef)
        # ef_minima = lista com ef calculadas

        return ef_minima
        
    # Metodo que executa o BRKGA
    def executa(self, matriz_entradas, simula_difusa, modo_otimizacao, tributarios, celula_entrada_tributarios):
        populacoes = []  # Lista de populacoes
        melhor_solucao = []
        melhores_solucoes = []  # Lista com melhores solucoes
        historico = []  # Lista com solucoes
        historico_fo = []
        historico_tempo_iteracoes = []
        historico_filhos_invalidos = []
        iteracao_versao_rapida = None

        [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] = ler_entrada_otimizacao(matriz_entradas)
        [FO_pontual, FO_difusa] = [matriz_brkga[0][6], matriz_brkga[1][6]]

        cenario_base = QUAL_UFMG()  # Objeto sem atributos
        
        ini = time()
        
        if simula_difusa:
            print("Rodando otimização da poluição difusa...")

            [Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(matriz_entradas, simula_difusa)
            del matriz_reducao_pontual  # Matriz nao utilizada
            ef_minima = []

            cenario_sem_otimizacao = cenario_base.executa(Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, FO_difusa, matriz_tipo_contribuicoes)
            
            # Criação da população
            for i in range(int(matriz_brkga[1][1])):  # para cada populacao
                aux = Populacao(matriz_brkga[1][7], matriz_brkga[1][0], len(scs.sub_bacias), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[1][6], True, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes)
                # aux = Populacao(pe, tam_populacao, tam_cromossomo, Entrada_Pontual.txt, Rio, cenario_base, matriz_reducao_pontual, ef_minima, funcao objetivo, simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs)
                
                aux.ordena_populacao()  # Populacao ordenada pela FO
                aux.set_melhor_inicial()  # Melhor individuo = Populacao[0]
                populacoes.append(aux)  # populacoes = lista com populacoes ordenadas
                print("Inválidos gerados na criação da população inicial difusa " + str(i+1) + ": " + str(aux.vetor_invalidos[0]))
            
            # Execução das gerações
            for j in range(int(matriz_brkga[1][1])):  # para cada populacao
                contagem = 0
                for k in range(int(matriz_brkga[1][5])):  # k varia de 0 ao valor de niter
                    [melhor_solucao, vetor_invalidos, tempo_iteracao, total_filhos_invalidos] = populacoes[j].gera_prox_geracao(matriz_brkga[1][2], matriz_brkga[1][3], matriz_brkga[1][4], matriz_brkga[1][7], matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, scs)
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
            [Rio, matriz_contribuicoes, self.matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(matriz_entradas, simula_difusa)
            ef_minima = self.calcula_ef_minima(Rio, matriz_contribuicoes)

            cenario_sem_otimizacao = cenario_base.executa(Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, FO_pontual, matriz_tipo_contribuicoes, tributarios, celula_entrada_tributarios)
            if self.matriz_reducao_pontual[1] == []:
                return [cenario_sem_otimizacao, None, None, None, tam_rio, tam_cel, None, None, None, None, None, None, ph, None, Rio]

            for i in range(int(matriz_brkga[0][1])):  # para cada populacao
                aux = Populacao(matriz_brkga[0][7], matriz_brkga[0][0], len(self.matriz_reducao_pontual[1]), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[0][6], simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes, tributarios, celula_entrada_tributarios)
                # aux = Populacao(pe, tam_populacao, tam_cromossomo, Entrada_Pontual.txt, Rio, cenario_base, matriz_reducao_pontual, ef_minima, funcao objetivo, simula_difusa, vetor_pesos_pontual, vetor_difusa, scs)

                aux.ordena_populacao()  # Populacao ordenada pela FO
                aux.set_melhor_inicial()  # Melhor individuo = Populacao[0]
                populacoes.append(aux)  # populacoes = lista com populacoes criadas
                print("Inválidos gerados na criação da população inicial pontual " + str(i+1) + ": " + str(aux.vetor_invalidos[0]))

            for j in range(int(matriz_brkga[0][1])):  # para cada populacao
                contagem = 0
                for k in range(int(matriz_brkga[0][5])):  # k varia de 0 ao valor de niter
                    [melhor_solucao, vetor_invalidos, tempo_iteracao, total_filhos_invalidos] = populacoes[j].gera_prox_geracao(matriz_brkga[0][2], matriz_brkga[0][3], matriz_brkga[0][4], matriz_brkga[0][7], matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, scs, tributarios, celula_entrada_tributarios)
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
            print("Otimização da poluição pontual encerrada.")

        fim = time()
        tempo = fim-ini
        tempo_rapida = fim_rapida-ini
        return [cenario_sem_otimizacao, melhores_solucoes, tempo, tempo_rapida, tam_rio, tam_cel, vetor_invalidos, vetor_invalidos_rapida, historico_fo, historico_tempo_iteracoes, historico_filhos_invalidos, iteracao_versao_rapida, ph, melhor_solucao_versao_rapida, Rio]