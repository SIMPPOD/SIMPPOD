# -*- coding: utf-8 -*-
# Modulo: Leitura

# Definicao da classe
class Leitura (object):
    # METODOS

    # Metodo que le o arquivo Entrada_Pontual.txt
    @staticmethod
    def ler_contribuicao_pontual(Caminho):
        leitor = open(Caminho)  

        leitor.readline()
        leitor.readline()
        leitor.readline()

        matriz_contribuicoes = []
        matriz_reducoes = [[], []]
        matriz_tipo_contribuicoes = []
        
        for x in leitor: 
            contribuicao = x.split(' ')  
            matriz_tipo_contribuicoes.append(contribuicao[-1][0])
            for i in range(len(contribuicao)-1):  
                contribuicao[i] = float(contribuicao[i]) 
            if contribuicao[10] == 1:  # Se ExR for 1
                if contribuicao[11] != 0:  # Se %R nao for 0
                    contribuicao[11] = contribuicao[11]/100 
                    matriz_reducoes[0].append(contribuicao[11])
                matriz_reducoes[1].append(contribuicao[9])
            matriz_contribuicoes.append(contribuicao)
        
        # matriz_reducoes[0] = vetor de %R
        # matriz_reducoes[1] = vetor de N
        # matriz_contribuicoes = matriz com vetores de contribuicoes

        return [matriz_contribuicoes, matriz_reducoes, matriz_tipo_contribuicoes]

    # Metodo que le o arquivo Entrada_Constantes.txt
    @staticmethod       
    def ler_constantes(Caminho):
        leitor = open(Caminho) 

        constantes = []
        for x in leitor:
            leitura = x.split(' ')
            constantes.append(float(leitura[0]))

        return constantes

    @staticmethod
    def ler_tamanho_celula(Caminho):
        leitor = open(Caminho)
        leitor.readline() 
        
        x = leitor.readline().split(' ')

        return x[0]
    
    # Leitura do arquivo Entrada_BRKGA.txt
    @staticmethod
    def ler_otimizacao(Caminho):
        vetor_pesos_pontual = []
        vetor_pesos_difusa = [] 
        matriz_brkga = [] 


        leitor_brkga = open(Caminho)
        leitor_brkga.readline() 
        
        for x in leitor_brkga:
            vetor_brkga = x.split(' ') 
            for i in range(len(vetor_brkga)):
                vetor_brkga[i] = float(vetor_brkga[i])
            matriz_brkga.append(vetor_brkga)

        for i in range(8,10):
            vetor_pesos_pontual.append(matriz_brkga[0][i])
        for j in range(8,12):
            vetor_pesos_difusa.append(matriz_brkga[1][j])

        return [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa]      
