# -*- coding: utf-8 -*-
# Modulo: Otimizacao

# Importacao de bibliotecas
from Populacao import Populacao
from QUAL_UFMG import QUAL_UFMG
from Leitura import Leitura
import time
import os

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
    def executa(self, matriz_entradas, simula_difusa, classe, numFuncao, modo_otimizacao, diretorio_saida):
        caminho_pontual = matriz_entradas[4]  # Entrada_Pontual.txt
        caminho_constantes = matriz_entradas[5]  # Entrada_Constantes.txt
        caminho_brkga = matriz_entradas[6]  # Entrada_BRKGA.txt
        caminho_hidro = ''
        caminho_cme = ''
        caminho_cn = ''
        caminho_usos = ''

        populacoes = []  # Lista de populacoes
        melhor_solucao = []
        melhores_solucoes = []  # Lista com melhores solucoes
        historico = []  # Lista com solucoes
        historico_fo = []
        historico_tempo_iteracoes = []
        historico_filhos_invalidos = []
        iteracao_versao_rapida = None

        ler = Leitura()
        [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] = ler.ler_otimizacao(caminho_brkga)

        cenario_base = QUAL_UFMG()  # Objeto sem atributos
        
        ini = time.time()
        
        if simula_difusa:
            print("Rodando otimização da poluição difusa...")
            # Atribuicao dos arquivos
            caminho_hidro = matriz_entradas[0]  # Entrada_Hidro.txt
            caminho_cme = matriz_entradas[1]  # Entrada_CME.txt
            caminho_cn = matriz_entradas[2]  # Entrada_CN.txt
            caminho_usos = matriz_entradas[3]  # Entrada_Usos.txt

            [Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(caminho_pontual, caminho_constantes, simula_difusa, caminho_cn, caminho_hidro, caminho_cme, caminho_usos, classe)
            del matriz_reducao_pontual  # Matriz nao utilizada
            ef_minima = []

            cenario_sem_otimizacao = cenario_base.executa(Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, numFuncao, matriz_tipo_contribuicoes)

            # Criação da população
            for i in range(int(matriz_brkga[1][1])):  # para cada populacao
                aux = Populacao(matriz_brkga[1][7], matriz_brkga[1][0], len(scs.lista_subbacias), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[1][6], True, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes)
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
                            fim = time.time()
                            iteracao_versao_rapida = k
                            print("Última iteração para versão rápida: " + str(k+1))
                            self.gera_saida_rapida_difusa(diretorio_saida, cenario_sem_otimizacao, melhores_solucoes, fim-ini, tam_rio, tam_cel, vetor_invalidos)
            print("Otimização da poluição difusa encerrada.")

        else:
            print("Rodando otimização da poluição pontual...")
            [Rio, matriz_contribuicoes, self.matriz_reducao_pontual, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = cenario_base.constroi_param_ini(caminho_pontual, caminho_constantes, simula_difusa, caminho_cn, caminho_hidro, caminho_cme, caminho_usos, classe)
            ef_minima = self.calcula_ef_minima(Rio, matriz_contribuicoes)

            cenario_sem_otimizacao = cenario_base.executa(Rio, matriz_contribuicoes, self.matriz_reducao_pontual, simula_difusa, [], scs, numFuncao, matriz_tipo_contribuicoes)
            
            for i in range(int(matriz_brkga[0][1])):  # para cada populacao
                aux = Populacao(matriz_brkga[0][7], matriz_brkga[0][0], len(self.matriz_reducao_pontual[1]), matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, ef_minima, matriz_brkga[0][6], simula_difusa, vetor_pesos_pontual, vetor_pesos_difusa, scs, modo_otimizacao, matriz_tipo_contribuicoes)
                # aux = Populacao(pe, tam_populacao, tam_cromossomo, Entrada_Pontual.txt, Rio, cenario_base, matriz_reducao_pontual, ef_minima, funcao objetivo, simula_difusa, vetor_pesos_pontual, vetor_difusa, scs)

                aux.ordena_populacao()  # Populacao ordenada pela FO
                aux.set_melhor_inicial()  # Melhor individuo = Populacao[0]
                populacoes.append(aux)  # populacoes = lista com populacoes criadas
                print("Inválidos gerados na criação da população inicial pontual " + str(i+1) + ": " + str(aux.vetor_invalidos[0]))
    
            for j in range(int(matriz_brkga[0][1])):  # para cada populacao
                contagem = 0
                for k in range(int(matriz_brkga[0][5])):  # k varia de 0 ao valor de niter
                    [melhor_solucao, vetor_invalidos, tempo_iteracao, total_filhos_invalidos] = populacoes[j].gera_prox_geracao(matriz_brkga[0][2], matriz_brkga[0][3], matriz_brkga[0][4], matriz_brkga[0][7], matriz_contribuicoes, Rio, cenario_base, self.matriz_reducao_pontual, scs)
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
                            fim = time.time()
                            iteracao_versao_rapida = k
                            print("Última iteração para versão rápida: " + str(k+1))
                            self.gera_saida_rapida_pontual(diretorio_saida, cenario_sem_otimizacao, melhores_solucoes, fim-ini, tam_rio, tam_cel, vetor_invalidos)
            print("Otimização da poluição pontual encerrada.")

        fim = time.time()
        return [cenario_sem_otimizacao, melhores_solucoes, populacoes, fim-ini, tam_rio, tam_cel, vetor_invalidos, historico_fo, historico_tempo_iteracoes, historico_filhos_invalidos, iteracao_versao_rapida, ph]

    def gera_saida_rapida_pontual(self, diretorio_saida, cenario_base_pontual, melhores_solucoes, tempo, tam_rio, tam_cel, vetor_invalidos):
        caminho_saida_brkga_pontual = diretorio_saida + "\Otimização-Poluição Pontual-Versão Rápida.csv"
        caminho_saida_qual_ufmg_otimizado_pontual = diretorio_saida + "\Perfil de QA-Poluição Pontual Otimizada-Versão Rápida.csv"

        self.checa_arquivo(diretorio_saida,"Otimização-Poluição Pontual-Versão Rápida.csv")
        self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Pontual Otimizada-Versão Rápida.csv")

        matriz_saidas = [caminho_saida_brkga_pontual, None, caminho_saida_qual_ufmg_otimizado_pontual]  
        
        melhor_solucao = melhores_solucoes[len(melhores_solucoes)-1]
        cenario_otimizado_pontual = melhor_solucao.cenario
        melhor_solucao.Escreve_saida(matriz_saidas[0], tempo, vetor_invalidos)
        cenario_otimizado_pontual.Escreve_saida_QualUFMG(matriz_saidas[2], tam_rio, tam_cel)
    
    def gera_saida_rapida_difusa(self, diretorio_saida, cenario_base_difuso, melhores_solucoes, tempo, tam_rio, tam_cel, vetor_invalidos):
        caminho_saida_brkga_difuso = diretorio_saida + "\Otimização-Poluição Difusa-Versão Rápida.csv"
        caminho_saida_qual_ufmg_otimizado_difuso = diretorio_saida + "\Perfil de QA-Poluição Difusa Otimizada-Versão Rápida.csv"
        caminho_saida_pd_otimizado = diretorio_saida + "\Poluição Difusa e CME Ponderada-Cenário Otimizado-Versão Rápida.csv"

        self.checa_arquivo(diretorio_saida,"Otimização-Poluição Difusa-Versão Rápida.csv")
        self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Difusa Otimizada-Versão Rápida.csv")
        self.checa_arquivo(diretorio_saida,"Poluição Difusa e CME Ponderada-Cenário Otimizado-Versão Rápida.csv")

        matriz_saidas = [0, 0, 0, caminho_saida_brkga_difuso, None,
                         caminho_saida_qual_ufmg_otimizado_difuso, None, caminho_saida_pd_otimizado]  
        
        melhor_solucao = melhores_solucoes[len(melhores_solucoes)-1]
        cenario_otimizado_difuso = melhor_solucao.cenario
        melhor_solucao.Escreve_saida(matriz_saidas[3], tempo, vetor_invalidos)
        cenario_otimizado_difuso.Escreve_saida_QualUFMG(matriz_saidas[5], tam_rio, tam_cel)
        cenario_otimizado_difuso.Escreve_saida_PD(matriz_saidas[7])

    @staticmethod
    def checa_arquivo(diretorio_saidas, arquivo):
        dir = os.listdir(diretorio_saidas)
        if arquivo in dir:
            os.remove('{}/{}'.format(diretorio_saidas, arquivo))