# -*- coding: utf-8 -*-
# Modulo: Leitura
from pandas import read_excel

# METODOS

# METODO DE LEITURA DO ARQUIVO ENTRADA PONTUAL
@staticmethod
def ler_entrada_pontual(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada Pontual")

    matriz_contribuicoes = []
    matriz_reducoes = [[], []]
    matriz_tipo_contribuicoes = []

    for i in range(df.shape[0]):
        contribuicao = df.values[i]
        matriz_tipo_contribuicoes.append(contribuicao[df.shape[1]-1])
           
        if contribuicao[10] == 1:  # Se ExR for 1
            if contribuicao[11] != 0:  # Se %R nao for 0
                contribuicao[11] = contribuicao[11]/100 
                matriz_reducoes[0].append(contribuicao[11])
            matriz_reducoes[1].append(contribuicao[9])
        matriz_contribuicoes.append(contribuicao.tolist())

    return [matriz_contribuicoes, matriz_reducoes, matriz_tipo_contribuicoes]

# METODO DE LEITURA DO ARQUIVO ENTRADA CONSTANTES
@staticmethod       
def ler_entrada_constantes(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada Constantes")

    constantes = []

    for i in range(df.shape[0]):
        constante = df.values[i]
        constantes.append(constante[1])

    return constantes

# METODO DE LEITURA DO ARQUIVO ENTRADA HIDRO
@staticmethod
def ler_entrada_hidro(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada Hidro")

    matriz = []
    
    for i in range(df.shape[0]):
        valores = df.values[i][:df.shape[1]-2]
        matriz.append(valores.tolist())
    
    fator = df.values[0, df.shape[1]-2]
    tam_celula = df.values[0, df.shape[1]-1]

    return [matriz,tam_celula,fator]

# METODO DE LEITURA DO ARQUIVO ENTRADA CN
@staticmethod        
def ler_entrada_cn(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada CN")

    matriz = []

    for i in range(df.shape[0]):
        valores = df.values[i]   
        matriz.append(valores.tolist())

    return matriz

# METODO DE LEITURA DO ARQUIVO ENTRADA CME
@staticmethod
def ler_entrada_cme(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada CME")

    matriz = []

    for i in range(df.shape[0]):
        valores = df.values[i]
        matriz.append(valores.tolist())

    return matriz

# METODO DE LEITURA DO ARQUIVO ENTRADA USOS
@staticmethod        
def ler_entrada_usos(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada Usos")

    matriz = []

    for i in range(df.shape[0]):
        valores = df.values[i]    
        matriz.append(valores.tolist())

    return matriz

# METODO DE LEITURA DO ARQUIVO ENTRADA OTIMIZAÇÃO
@staticmethod
def ler_entrada_otimizacao(arquivo):
    df = read_excel(arquivo, sheet_name="Entrada Otimização")

    vetor_pesos_pontual = []
    vetor_pesos_difusa = [] 
    matriz_brkga = [] 

    for i in range(df.shape[0]):
        valores = df.values[i]
        matriz_brkga.append(valores.tolist())

    for i in range(8,10):
        vetor_pesos_pontual.append(matriz_brkga[0][i])
    for j in range(8,12):
        vetor_pesos_difusa.append(matriz_brkga[1][j])

    return [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] 