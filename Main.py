# -*- coding: utf-8 -*-
# Modulo: Main

# Importacao de bibliotecas
from Otimizacao import Otimizacao
import os

# Definicao da classe
class Main_brkga:

    # METODOS

    @staticmethod
    def checa_arquivo(diretorio_saidas, arquivo):
        dir = os.listdir(diretorio_saidas)
        if arquivo in dir:
            os.remove('{}/{}'.format(diretorio_saidas, arquivo))

    # Metodo que gera a matriz de saidas
    def gera_matriz_saida(self, diretorio_saida, modo_execucao):
        if modo_execucao == "21":
            caminho_saida_brkga_pontual = diretorio_saida + "\Otimização-Poluição Pontual.csv"
            caminho_saida_qual_ufmg_base_pontual = diretorio_saida + "\Perfil de QA-Poluição Pontual.csv"
            caminho_saida_qual_ufmg_otimizado_pontual = diretorio_saida + "\Perfil de QA-Poluição Pontual Otimizada.csv"
            
            self.checa_arquivo(diretorio_saida,"Otimização-Poluição Pontual.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Pontual.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Pontual Otimizada.csv")

            matriz_saidas = [caminho_saida_brkga_pontual, caminho_saida_qual_ufmg_base_pontual, caminho_saida_qual_ufmg_otimizado_pontual]

        elif modo_execucao == "22":
            caminho_saida_brkga_pontual = diretorio_saida + "\Otimização-Poluição Pontual.csv"
            caminho_saida_qual_ufmg_base_pontual = diretorio_saida + "\Perfil de QA-Poluição Pontual.csv"
            caminho_saida_qual_ufmg_otimizado_pontual = diretorio_saida + "\Perfil de QA-Poluição Pontual Otimizada.csv"
            caminho_saida_brkga_difuso = diretorio_saida + "\Otimização-Poluição Difusa.csv"
            caminho_saida_qual_ufmg_base_difuso = diretorio_saida + "\Perfil de QA-Poluição Difusa.csv"
            caminho_saida_qual_ufmg_otimizado_difuso = diretorio_saida + "\Perfil de QA-Poluição Difusa Otimizada.csv"
            caminho_saida_pd_base = diretorio_saida + "\Poluição Difusa e CME Ponderada-Cenário Base.csv"
            caminho_saida_pd_otimizado = diretorio_saida + "\Poluição Difusa e CME Ponderada-Cenário Otimizado.csv"

            self.checa_arquivo(diretorio_saida,"Otimização-Poluição Pontual.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Pontual.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Pontual Otimizada.csv")
            self.checa_arquivo(diretorio_saida,"Otimização-Poluição Difusa.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Difusa.csv")
            self.checa_arquivo(diretorio_saida,"Perfil de QA-Poluição Difusa Otimizada.csv")
            self.checa_arquivo(diretorio_saida,"Poluição Difusa e CME Ponderada-Cenário Base.csv")
            self.checa_arquivo(diretorio_saida,"Poluição Difusa e CME Ponderada-Cenário Otimizado.csv")

            matriz_saidas = [caminho_saida_brkga_pontual, caminho_saida_qual_ufmg_base_pontual, caminho_saida_qual_ufmg_otimizado_pontual,
                             caminho_saida_brkga_difuso, caminho_saida_qual_ufmg_base_difuso, caminho_saida_qual_ufmg_otimizado_difuso,
                             caminho_saida_pd_base, caminho_saida_pd_otimizado]            

        return matriz_saidas

    def executa(self, matriz_entradas, diretorio_saida, modo_execucao, classe, numFuncaoP, numFuncaoD, modo_otimizacao):
        matriz_saidas = self.gera_matriz_saida(diretorio_saida, modo_execucao)
        brkga = Otimizacao()

        if modo_execucao == "21":
            [cenario_base_pontual, melhores_solucoesP, populacoes, tempo, tam_rio, tam_cel, vetor_invalidos, historico_foP, historico_tempo_iteracoesP, historico_filhos_invalidosP, iteracao_versao_rapidaP, ph] = brkga.executa(matriz_entradas, False, classe, numFuncaoP, modo_otimizacao, diretorio_saida)
            historico_fo = None
            historico_tempo_iteracoes = None
            historico_filhos_invalidos = None
            iteracao_versao_rapida = None

            melhor_solucaoP = melhores_solucoesP[len(melhores_solucoesP)-1]

            cenario_otimizado_pontual = melhor_solucaoP.cenario
            cenario_base_difuso = []
            cenario_otimizado_difuso = []

            # Gerando saida BRKGA
            melhor_solucaoP.Escreve_saida(matriz_saidas[0], tempo, vetor_invalidos)

            # Gerando saidas QUAL_UFMG
            cenario_base_pontual.Escreve_saida_QualUFMG(matriz_saidas[1], tam_rio, tam_cel)
            cenario_otimizado_pontual.Escreve_saida_QualUFMG(matriz_saidas[2], tam_rio, tam_cel)

            # Guardando perfil da vazao
            perfilQP = melhor_solucaoP.cenario.PerfilQ
            perfilQ = None

        elif modo_execucao == "22":
            # Roda cenario pontual
            [cenario_base_pontual, melhores_solucoesP, populacoesP, tempoP, tam_rio, tam_cel, vetor_invalidosP, historico_foP, historico_tempo_iteracoesP, historico_filhos_invalidosP, iteracao_versao_rapidaP, ph] = brkga.executa(matriz_entradas, False, classe, numFuncaoP, modo_otimizacao, diretorio_saida)
            del populacoesP 

            melhor_solucaoP = melhores_solucoesP[len(melhores_solucoesP)-1]

            brkga.matriz_reducao_pontual[0] = melhor_solucaoP.alelos
            cenario_otimizado_pontual = melhor_solucaoP.cenario  # Melhor solucao pontual

            # Gerando saidas do cenario pontual
            melhor_solucaoP.Escreve_saida(matriz_saidas[0], tempoP, vetor_invalidosP)
            cenario_base_pontual.Escreve_saida_QualUFMG(matriz_saidas[1], tam_rio, tam_cel)
            cenario_otimizado_pontual.Escreve_saida_QualUFMG(matriz_saidas[2], tam_rio, tam_cel)

            # Roda cenario difuso
            [cenario_base_difuso, melhores_solucoes, populacoes, tempo, tam_rio, tam_cel, vetor_invalidos, historico_fo, historico_tempo_iteracoes, historico_filhos_invalidos, iteracao_versao_rapida, ph] = brkga.executa(matriz_entradas, True, classe, numFuncaoD, modo_otimizacao, diretorio_saida)
            
            melhor_solucao = melhores_solucoes[len(melhores_solucoes)-1]
            
            cenario_otimizado_difuso = melhor_solucao.cenario  # Melhor solucao difusa

            # Gerando saidas do cenario difuso
            melhor_solucao.Escreve_saida(matriz_saidas[3], tempo, vetor_invalidos)
            cenario_base_difuso.Escreve_saida_QualUFMG(matriz_saidas[4], tam_rio, tam_cel)
            cenario_otimizado_difuso.Escreve_saida_QualUFMG(matriz_saidas[5], tam_rio, tam_cel)
            cenario_base_difuso.Escreve_saida_PD(matriz_saidas[6])
            cenario_otimizado_difuso.Escreve_saida_PD(matriz_saidas[7])

            # Guardando perfil da vazao
            perfilQP = melhor_solucaoP.cenario.PerfilQ
            perfilQ = melhor_solucao.cenario.PerfilQ

        return [cenario_base_pontual, cenario_otimizado_pontual, cenario_base_difuso, cenario_otimizado_difuso, populacoes, historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes, historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida, tam_rio, tam_cel, ph, perfilQP, perfilQ]
