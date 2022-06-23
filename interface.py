# -*- coding: utf-8 -*-
# Modulo: interface

# Importacao de bibliotecas
from QUAL_UFMG import QUAL_UFMG
from SCS import SCS
from Leitura import Leitura
from Leitura_difusa import Leitura_difusa
from Main import Main_brkga

import tkinter
import tkinter.messagebox
from tkinter import Tk, TOP, BOTH, LEFT
from tkinter import Button, Checkbutton, Radiobutton
from tkinter import IntVar, StringVar
from tkinter import Canvas, Frame, Label
from tkinter import filedialog

from functools import partial

import time
import os

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.backend_managers
from matplotlib import pyplot as plt
import matplotlib.cm as cm

matplotlib.use('TkAgg')

# METODOS
def cria_vetor_restricao(indice, tam_rio, tam_cel, ph, classe):
    vetor_restricao = []
    for i in range(int(tam_rio/tam_cel)):
        if classe == 1.0:
            if indice == 0:
                vetor_restricao.append(3)
            elif indice == 1:
                vetor_restricao.append(6)
            elif indice == 3:
                if ph <= 7.5:
                    vetor_restricao.append(3.7)
                elif 7.5 < ph <= 8:
                    vetor_restricao.append(2)
                elif 8 < ph < 8.5:
                    vetor_restricao.append(1)
                elif ph >= 8.5:
                    vetor_restricao.append(0.5)
            elif indice == 4:
                vetor_restricao.append(1)
            elif indice == 5:
                vetor_restricao.append(10)
            elif indice == 6:
                vetor_restricao.append(0.1)
        elif classe == 2.0:
            if indice == 0:
                vetor_restricao.append(5)
            elif indice == 1:
                vetor_restricao.append(5)
            elif indice == 3:
                if ph <= 7.5:
                    vetor_restricao.append(3.7)
                elif 7.5 < ph <= 8:
                    vetor_restricao.append(2)
                elif 8 < ph < 8.5:
                    vetor_restricao.append(1)
                elif ph >= 8.5:
                    vetor_restricao.append(0.5)
            elif indice == 4:
                vetor_restricao.append(1)
            elif indice == 5:
                vetor_restricao.append(10)
            elif indice == 6:
                vetor_restricao.append(0.1)
        elif classe == 3.0:
            if indice == 0:
                    vetor_restricao.append(10)
            elif indice == 1:
                    vetor_restricao.append(4)
            elif indice == 3:
                if ph <= 7.5:
                    vetor_restricao.append(13.3)
                elif 7.5 < ph <= 8:
                    vetor_restricao.append(5.6)
                elif 8 < ph < 8.5:
                    vetor_restricao.append(2.2)
                elif ph >= 8.5:
                    vetor_restricao.append(1)
            elif indice == 4:
                vetor_restricao.append(1)
            elif indice == 5:
                vetor_restricao.append(10)
            elif indice == 6:
                vetor_restricao.append(0.15)
        elif classe == 4.0:
            if indice == 0:
                vetor_restricao.append(30)
            elif indice == 1:
                vetor_restricao.append(2)
            elif indice == 3:
                vetor_restricao.append(0)
            elif indice == 4:
                vetor_restricao.append(50)
            elif indice == 5:
                vetor_restricao.append(50)
            elif indice == 6:
                vetor_restricao.append(1)
    return vetor_restricao

# Metodo que gera os graficos de saida
def gera_grafico(serie_dados, indice, restricao, tam_cel, tam_rio, classe):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Concentração(mg/L) do Parâmetro ao Longo do Curso D'água (células)")
   
    # Plot do grafico
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    y = serie_dados
    num_cel = tam_rio / tam_cel
    x = []
    for i in range(int(num_cel)):
        x.append(int(i*tam_rio/num_cel))
    
    ax = fig.add_subplot(111, xlabel="Extensão [m]", ylabel="Concentração [mg/L]")
    ax.plot(x, y, 'b')

    if indice != 2 and indice < 6:
        ax.plot(x, restricao, 'r')
    
    menor = min(serie_dados)
    maior = max(serie_dados)
    media = sum(serie_dados)/len(serie_dados)

    fig.text(0.01, 1, 'Mínimo = ' + str(round(menor,4)) +
                        ' | Máximo = ' + str(round(maior,4)) +
                        ' | Média = ' + str(round(media,4)),
            horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes)

    # Titulo do grafico, de acordo com o componente
    if indice == 0:
        fig.suptitle("Demanda Bioquímica de Oxigênio")
        ax.legend(['DBO', 'Limite da Classe ' + str(classe)])
    elif indice == 1:
        fig.suptitle("Oxigênio Dissolvido")
        ax.legend(['OD', 'Limite da Classe ' + str(classe)])
    elif indice == 2:
        fig.suptitle("Nitrogênio Orgânico")
        ax.legend(['NORG'])
    elif indice == 3:
        fig.suptitle("Nitrogênio Amoniacal")
        ax.legend(['NH3', 'Limite da Classe ' + str(classe)])
    elif indice == 4:
        fig.suptitle("Nitrito")
        ax.legend(['Nitrito', 'Limite da Classe ' + str(classe)])
    elif indice == 5:
        fig.suptitle("Nitrato")
        ax.legend(['Nitrato', 'Limite da Classe ' + str(classe)])
    elif indice == 6:
        fig.suptitle("Fósforo Orgânico")
        ax.legend(['PORG'])
    else:
        fig.suptitle("Fósforo Inorgânico")
        ax.legend(['PINORG'])

    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()
    
# Metodo que gera o gráfico da FO
def gera_grafico_fo(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Função Objetivo ao Longo das Iterações")

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111, xlabel="Iteração", ylabel="FO (u)", title='Comportamento da FO')
    ax.plot(serie_dados, 'b')

    if iteracao_versao_rapida is not None:
        ax.axvline(x=iteracao_versao_rapida, ymin=0, ymax=1, color='g')
        ax.legend(['FO', 'Última Iteração no Modo Rápido'], loc='upper right')
    else:
        ax.legend(['FO'], loc='upper right')

    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# Metodo que gera o gráfico do tempo das iteracoes
def gera_grafico_tempo_iteracoes(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento do Tempo de Duração das Iterações")

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111, xlabel="Iteração", ylabel="Tempo (s)", title='Comportamento da Duração da Iteração')
    ax.plot(serie_dados, 'bo')

    if iteracao_versao_rapida is not None:
        ax.axvline(x=iteracao_versao_rapida, ymin=0, ymax=1, color='g')
        ax.legend(['Duração da iteração', 'Última Iteração no Modo Rápido'], loc='upper right')
    else:
        ax.legend(['Duração da iteração'], loc='upper right')

    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# Metodo que gera o gráfico dos filhos invalidos
def gera_grafico_filhos_invalidos(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Geração de Filhos Inválidos ao Longo das Iterações")

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111, xlabel="Iteração", ylabel="Filhos Inválidos (u)", title='Comportamento da Geração de Filhos Inválidos')
    ax.plot(serie_dados, 'b')

    if iteracao_versao_rapida is not None:
        ax.axvline(x=iteracao_versao_rapida, ymin=0, ymax=1, color='g')
        ax.legend(['Número de Filhos Inválidos', 'Última Iteração no Modo Rápido'], loc='upper right')
    else: 
        ax.legend(['Número de Filhos Inválidos'], loc='upper right')
        
    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# Metodo que gera o gráfico dos filhos invalidos
def gera_grafico_vazao(serie_dados, tam_cel, tam_rio):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Vazão")

    # Plot do grafico
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    y = serie_dados
    num_cel = tam_rio / tam_cel
    x = []
    for i in range(int(num_cel)):
        x.append(int(i*tam_rio/num_cel))   
    
    ax = fig.add_subplot(111, xlabel="Extensão [m]", ylabel="Vazão [m^3/s]", title="Comportamento da Vazão")
    ax.plot(x, y, 'b')
      
    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# Metodo que le e salva o caminho para um arquivo de entrada
def le_arquivo(vetor_caminhos, label, indice):
    nome_do_arquivo = filedialog.askopenfilenames()  # Abre uma janela para selecao de arquivos de entrada
    if not str(nome_do_arquivo).__eq__(""):
        label["text"] = nome_do_arquivo
        vetor_caminhos[indice] = nome_do_arquivo  # Salva o caminho do arquivo na respectiva posicao
    # Se o usuario abre e fecha a janela sem selecionar um arquivo, o texto do label permanece o mesmo

# Metodo que le e salva a pasta para os arquivos de saida
def le_saida(diretorio_saidas, label):
    nome_do_diretorio = filedialog.askdirectory()
    # Se o usuario abre e fecha a janela sem selecionar um arquivo, o texto do label permanece o mesmo
    if not str(nome_do_diretorio).__eq__(""):
        label["text"] = nome_do_diretorio
        diretorio_saidas.set(nome_do_diretorio)  # Abre uma janela para selecao de pasta para arquivos de saida
        
# Metodo que cria um botao de reset, que limpa os parametros de entrada
def reset_botao(vetor_caminhos, label, indice):
    vetor_caminhos[indice] = ""  # Delecao do caminho original

    # Retornando ao label anterior
    label["text"] = "Selecione a Entrada_"
    if indice == 0:
        label["text"] += "Hidro.txt..."
    elif indice == 1:
        label["text"] += "CME.txt..."
    elif indice == 2:
        label["text"] += "CN.txt..."
    elif indice == 3:
        label["text"] += "Usos.txt..."
    elif indice == 4:
        label["text"] += "Pontual.txt..."
    elif indice == 5:
        label["text"] += "Constantes.txt..."
    else:
        label["text"] += "Otimização.txt..."

def reset_saida(diretorio_saidas, label):
    diretorio_saidas.set("")  # Delecao do caminho original
    label["text"] = "Selecione o caminho para as Saidas..."  # Retornando ao label anterior

# Metodo que cria a janela "Sobre"
def Sobre():
    janela = Tk()  # Cria janela
    janela["bg"] = '#94B7D5'  # Define cor de fundo
    janela.title("SIMPPOD - Sistema de Modelagem de Poluição Pontual e Difusa")  # Adiciona titulo
    janela.geometry("400x500")  # Define dimensao
    selecao = Label(janela, text="O SIMPPOD é um sistema de suporte a decisão,\nque permite ao usuário estimar a produção\nde cargas difusas, simular perfil de\nqualidade de água em rios a partir\nde entrada de fontes pontuais e difusas.\nAlém de identificar os percentuais de\nremoção/redução necessários a serem\naplicados a estas cargas, de modo a\ngarantir a classe de qualidade de água\ndesejada pelos usuários.\nSendo portanto um sistema de suporte\nao enquadramento e ao planejamento e gestão\nde recursos hídricos.\nSendo composto por dois algoritmos\nde otimização (AGOFP e AGOFD), um modelo de\nqualidade de água (Qual-UFMG), um modelo hidrológico\ne também um modelo de estimativa de\ncargas difusas. Para a otimização o\nSIMPPOD dispõe de mais de uma opção de\nmétodo, sendo estes diferentes modalidades\nde Algoritmos Genéticos", bg='#94B7D5', font=('Arial', '12'))
    selecao.place(x=0, y=0)
    janela.mainloop()

# Metodo que muda a tela quando solicitado
def Muda_tela(janela_inicial, novo_frame):
    janela_inicial.pack_forget()
    janela_inicial = novo_frame
    janela_inicial.place(x=0, y=0)

def executa(vetor_caminhos, diretorio_saidas, modo_execucao, label_caixa_texto, classe, modo_otimizacao):
    for i in range(len(vetor_caminhos)):
        vetor_caminhos[i] = list(vetor_caminhos[i])

    if modo_execucao.get() == "110":
        # Simula Qualidade de Água Pontual  --> gera CBP
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Poluição Pontual \n"
        #caminho_saida_pontual = diretorio_saidas + "\Perfil de QA-Poluição Pontual.csv"

        tempo_inicial = time.time()
        qual_ufmg = QUAL_UFMG()
        cenario_base_pontual = []

        for i in range(len(vetor_caminhos[5])):
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[4][i],
                                                                                                               vetor_caminhos[5][i], False, "",
                                                                                                               "", "", "", classe)
            # qual_ufmg.constroi_param_ini(pontual, constantes, simula_difusa, cn, hidro, cme, usos)

            cenario_bpontual = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes)
            # qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, simula_difusa, matriz_reducao_difusa, scs, numFuncaoP)

            nome_arquivo = diretorio_saidas + "\Perfil de QA-Poluição Pontual - Tributario " + str(i+1) + ".csv"
            Main_brkga.checa_arquivo(diretorio_saidas, nome_arquivo)
            cenario_bpontual.Escreve_saida_QualUFMG(nome_arquivo, tam_rio, tam_cel)

            tempo_final = time.time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "Saida dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial)
        
            # Criacao dos parametros do retorno
            cenario_otimizado_pontual = None
            cenario_base_difuso = None
            cenario_otimizado_difuso = None
            historico_foP = None
            historico_fo = None
            historico_tempo_iteracoesP = None
            historico_tempo_iteracoes = None
            historico_filhos_invalidosP = None
            historico_filhos_invalidos = None
            iteracao_versao_rapidaP = None
            iteracao_versao_rapida = None

            # Guardando perfil da vazao
            perfilQP = cenario_bpontual.PerfilQ
            perfilQ = None

            cenario_base_pontual.append(cenario_bpontual)
    
            print("Simulação de Qualidade de Água para poluição pontual concluída.\nGráficos e arquivos gerados.")

    elif modo_execucao.get() == "101":
        # Simula Qualidade de Água Difusa  --> gera CBD
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Simulação Qualidade de Água: Poluição Difusa \n"
        #caminho_saida = diretorio_saidas + "\Perfil de QA-Poluição Difusa.csv"

        qual_ufmg = QUAL_UFMG()
        cenario_base_difuso = []

        for i in range(len(vetor_caminhos[5])):
            # CRIACAO DO CENARIO BASE DIFUSO
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[4][i],
                                                                                                               vetor_caminhos[5][i], True,
                                                                                                               vetor_caminhos[2][i],
                                                                                                               vetor_caminhos[0][i],
                                                                                                               vetor_caminhos[1][i],
                                                                                                               vetor_caminhos[3][i], classe)
            # qual_ufmg.constroi_param_ini(pontual, constantes, simula_difusa, cn, hidro, cme, usos)

            cenario_bdifuso = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes)
            # qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, simula_difusa, matriz_reducao_difusa, scs)

            nome_arquivo = diretorio_saidas + "\Perfil de QA-Poluição Difusa - Tributario " + str(i+1) + ".csv"
            Main_brkga.checa_arquivo(diretorio_saidas, nome_arquivo)
            cenario_bdifuso.Escreve_saida_PD(nome_arquivo)

            cenario_base_pontual = None
            cenario_otimizado_pontual = None
            cenario_otimizado_difuso = None
            historico_foP = None
            historico_fo = None
            historico_tempo_iteracoesP = None
            historico_tempo_iteracoes = None
            historico_filhos_invalidosP = None
            historico_filhos_invalidos = None
            iteracao_versao_rapidaP = None
            iteracao_versao_rapida = None

            # Guardando perfil da vazao
            perfilQP = None
            perfilQ = cenario_bdifuso.PerfilQ

            cenario_base_difuso.append(cenario_bdifuso)

            print("Simulação de Qualidade de Água para poluição difusa concluída.\nGráficos e arquivos gerados.")

    elif modo_execucao.get() == "111":
        # Simula Qualidade de Água Difusa  --> gera CBP e CBD
        label_caixa_texto["text"] = label_caixa_texto["text"] + " Poluição Pontual + Poluição Difusa \n"

        qual_ufmg = QUAL_UFMG()
        cenario_base_pontual = []
        cenario_base_difuso = []

        for i in range(len(vetor_caminhos[5])):
            # CRIACAO DO CENARIO BASE DIFUSO
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[4][i],
                                                                                                               vetor_caminhos[5][i], True,
                                                                                                               vetor_caminhos[2][i],
                                                                                                               vetor_caminhos[0][i],
                                                                                                               vetor_caminhos[1][i],
                                                                                                               vetor_caminhos[3][i], classe)
            # qual_ufmg.constroi_param_ini(pontual, constantes, simula_difusa, cn, hidro, cme, usos)

            cenario_bdifuso = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes)
            # qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, simula_difusa, matriz_reducao_difusa, scs)

            nome_arquivo = diretorio_saidas + "\Perfil de QA-Poluição Difusa - Tributario " + str(i+1) + ".csv"
            Main_brkga.checa_arquivo(diretorio_saidas, nome_arquivo)
            cenario_bdifuso.Escreve_saida_PD(nome_arquivo)

            # CRIACAO DO CENARIO BASE PONTUAL
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[4][i],
                                                                                                           vetor_caminhos[5][i], False, "",
                                                                                                           "", "", "", classe)
            del scs  # Parametro nulo

            cenario_bpontual = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], [], None, matriz_tipo_contribuicoes)
            # qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, simula_difusa, matriz_reducao_difusa, scs)

            nome_arquivo = diretorio_saidas + "\Perfil de QA-Poluição Pontual - Tributario " + str(i+1) + ".csv"
            Main_brkga.checa_arquivo(diretorio_saidas, nome_arquivo)
            cenario_bpontual.Escreve_saida_QualUFMG(nome_arquivo, tam_rio, tam_cel)

            # Guardando perfil da vazao
            perfilQP = cenario_bpontual.PerfilQ
            perfilQ = cenario_bdifuso.PerfilQ

            cenario_base_pontual.append(cenario_bpontual)
            cenario_base_difuso.append(cenario_bdifuso)
        
            # Criacao dos parametros do retorno
            cenario_otimizado_pontual = None
            cenario_otimizado_difuso = None
            historico_foP = None
            historico_fo = None
            historico_tempo_iteracoesP = None
            historico_tempo_iteracoes = None
            historico_filhos_invalidosP = None
            historico_filhos_invalidos = None
            iteracao_versao_rapidaP = None
            iteracao_versao_rapida = None

            print("Simulação de Qualidade de Água para poluição pontual e difusa concluída.\nGráficos e arquivos gerados.")
    
    elif modo_execucao.get() == 2:
        # Apenas MODELO PD  --> nao gera graficos
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Modelo de Cargas Difusas \n"

        for i in range(len(vetor_caminhos[0])):
            scs = SCS(vetor_caminhos[2][i], vetor_caminhos[0][i], vetor_caminhos[1][i], vetor_caminhos[3][i])
            # scs = SCS(cn, hidro, CME, usos)

            leitor = Leitura()
            tam_cel = float(leitor.ler_tamanho_celula(vetor_caminhos[0][i]))
        
            [matriz_difusa, lista_subbacias, matriz_cargas] = scs.executa([], tam_cel)
            # [matriz_difusa, lista_subbacias, matriz_cargas] = scs.executa(matriz_reducao, tam_cel)

            # Delecao de variaveis nao utilizadas
            del matriz_difusa
            del lista_subbacias
            del matriz_cargas

            nome_arquivo = diretorio_saidas + "\Poluição Difusa e CME Ponderada-Cenário Base - Tributario " + str(i+1) + ".csv"
            Main_brkga.checa_arquivo(diretorio_saidas, nome_arquivo)
            scs.Escreve_saida_PD(nome_arquivo)
        
            # Criacao dos parametros do retorno
            cenario_base_pontual = None
            cenario_otimizado_pontual = None
            cenario_base_difuso = None
            cenario_otimizado_difuso = None
            historico_foP = None
            historico_fo = None
            historico_tempo_iteracoesP = None
            historico_tempo_iteracoes = None
            historico_filhos_invalidosP = None
            historico_filhos_invalidos = None
            iteracao_versao_rapidaP = None
            iteracao_versao_rapida = None
            tam_rio = None
            tam_cel = None
            ph = None
            perfilQP = None
            perfilQ = None

            print("Estimação de cargas difusas concluída.\nArquivos gerados.")
    
    elif modo_execucao.get() == "21":
        # Otimizacao modo pontual  --> gera CBP e COP
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Otimização de Cargas Pontuais \n"

        tributario = [None, None, None, None]
        for i in range(len(vetor_caminhos[4])):
            tributario.append(vetor_caminhos[4][i])
            tributario.append(vetor_caminhos[5][i])
            tributario.append(vetor_caminhos[6][i])

            copia = vetor_caminhos[6][i]
            ler = Leitura()
            [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] = ler.ler_otimizacao(copia)
            del vetor_pesos_pontual
            del vetor_pesos_difusa

            brkga = Main_brkga()
            [cenario_base_pontual, cenario_otimizado_pontual, cenario_base_difuso, cenario_otimizado_difuso,
            populacoes, historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes,
            historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQP, perfilQ] = brkga.executa(tributario, diretorio_saidas, modo_execucao.get(), classe, matriz_brkga[0][6], None, modo_otimizacao.get()) # Gera apenas as saidas pontuais
            del populacoes  # Variavel nao utilizada

            label_caixa_texto["text"] = label_caixa_texto["text"] + "Saidas gerada com sucesso!\n"
            numFuncao = None
    
    elif modo_execucao.get() == "22":
        # Otimizacao modo pontual + difuso  --> gera CBP, CBD, COP e COD
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Otimização de Cargas Difusas e Pontuais \n"

        tributario = [None, None, None, None]
        for i in range(len(vetor_caminhos[4])):
            tributario.append(vetor_caminhos[4][i])
            tributario.append(vetor_caminhos[5][i])
            tributario.append(vetor_caminhos[6][i])

            copia = vetor_caminhos[6][i]
            ler = Leitura()
            [matriz_brkga, vetor_pesos_pontual, vetor_pesos_difusa] = ler.ler_otimizacao(copia)
            del vetor_pesos_pontual
            del vetor_pesos_difusa

            tempo_inicial = time.time()

            brkga = Main_brkga()
            [cenario_base_pontual, cenario_otimizado_pontual, cenario_base_difuso, cenario_otimizado_difuso,
            populacoes, historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes,
            historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQP, perfilQ] = brkga.executa(tributario, diretorio_saidas, modo_execucao.get(), classe, matriz_brkga[0][6], matriz_brkga[1][6], modo_otimizacao.get())
            # brkga.executa(matriz_entrada, diretorio_saida, simula_difusa)
            # vetor_caminhos = [Hidro, CME, CN, Usos, Pontual, Constantes, BRKGA] 
        
            del populacoes  # Variavel nao utilizada

            tempo_final = time.time()

    return [cenario_base_pontual, cenario_otimizado_pontual, cenario_base_difuso, cenario_otimizado_difuso,
            historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes,
            historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQP, perfilQ]

# Metodo que define a janela para escolha de arquivos e pasta para simulacao
def Janela_simulacao(janela_inicial, Tela):
    classe = IntVar()
    modo_simulacao = IntVar()

    # Frame
    frame_simulacao = Frame(Tela, height=600, width=800, bg='#94B7D5')

    # Retangulos --> Areas demarcadas
    canvas_pontual = Canvas(frame_simulacao, height=50, width=796, bg='#94B7D5', highlightbackground="black")
    canvas_pd = Canvas(frame_simulacao, height=50, width=796, bg='#94B7D5', highlightbackground="black")
    canvas_brkga = Canvas(frame_simulacao, bg='#94B7D5', height=50, width=796, highlightbackground="black")
    canvas_selecao = Canvas(frame_simulacao, bg='#94B7D5', height=30, width=796, highlightbackground="black")

    selecao = Label(canvas_selecao, text="Selecione o modo de execução:", bg='#94B7D5', font=('Arial', '12'))

    # Checkbuttons  --> botoes de modo de execucao
    checa_pontual = Radiobutton(canvas_pontual, text="Simular Qualidade de Água",bg='#94B7D5', variable=modo_simulacao, value=1)
    checa_pd = Radiobutton(canvas_pd, text="Estimar Cargas Difusas", bg='#94B7D5', variable=modo_simulacao, value=2)
    checa_brkga = Radiobutton(canvas_brkga, text="Otimização", bg='#94B7D5', variable=modo_simulacao, value=3)

    # Botões
    botao_executa = Button(frame_simulacao, width=30, text="Executar", command=partial(Janela_Seleciona_Simulacao, janela_inicial, Tela, modo_simulacao))
    
    # Localizando todos os componentes
    canvas_selecao.place(x=0,y=28)
    canvas_pontual.place(x=0, y=60)
    canvas_pd.place(x=0, y=110)
    canvas_brkga.place(x=0, y=160)
    selecao.place(x=300, y=2)
    checa_pontual.place(x=2, y=2)
    checa_pd.place(x=2, y=2)
    checa_brkga.place(x=2, y=2)
    botao_executa.place(x=550, y=560)

    Muda_tela(janela_inicial, frame_simulacao)

def Janela_Erro():
    tkinter.messagebox.showerror("Error", "ENTRADAS INVÁLIDAS!")

def Janela_Simula_Qualidade_Agua(janela_inicial, Tela):
    frame = Frame(Tela, height=600, width=800, bg='#94B7D5')
    canvas = Canvas(frame, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas.place(x=0, y=60)

    label = Label(frame, text="Simular Qualidade de Água:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label.place(x=0,y=0)

    simula_pontual = IntVar()
    checa_pontual = Checkbutton(canvas, text="Simular Perfil de Qualidade de Água - Poluição Pontual", bg='#94B7D5', variable=simula_pontual)
    checa_pontual.place(x=2, y=2)

    simula_difuso = IntVar()
    checa_difuso = Checkbutton(canvas, text="Simular Perfil de Qualidade de Água - Poluição Difusa", bg='#94B7D5', variable=simula_difuso)
    checa_difuso.place(x=2, y=40)

    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_Simula_Qualidade_Agua_Modo, janela_inicial, Tela, simula_pontual, simula_difuso))
    botao_executa.place(x=550, y=560)

    Muda_tela(janela_inicial, frame)    

def Janela_Simula_Qualidade_Agua_Modo(janela_inicial, Tela, simula_pontual, simula_difuso):
    modo_otimizacao = IntVar()
    modo_otimizacao.set(0)
    modo_execucao = StringVar()
    modo_execucao.set("1"+str(simula_pontual.get())+str(simula_difuso.get()))
    classe = IntVar()

    vetor_caminhos = ["", "", "", "", "", "", ""]
    diretorio_saidas = StringVar()
    frame_simulacao = Frame(Tela, height=600, width=800, bg='#94B7D5')

    canvas_entradas = Canvas(frame_simulacao, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas_saida = Canvas(frame_simulacao, bg='#94B7D5', height=30, width=796, highlightbackground="black")
    entradas = Label(frame_simulacao, text="Selecione os Arquivos de Entrada:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label_saidas = Label(canvas_saida, width=70, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    botao_saidas = Button(canvas_saida, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_reset_saida = Button(canvas_saida, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_executa = Button(frame_simulacao, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, classe, modo_otimizacao))

    canvas_entradas.place(x=0, y=60)
    canvas_saida.place(x=0, y=515)
    entradas.place(x=0, y=0)
    label_saidas.place(x=6, y=4)
    botao_saidas.place(x=650, y=4)
    botao_reset_saida.place(x=700, y=4)
    botao_executa.place(x=550, y=560)

    #label_classe = Label(canvas_entradas, text="Selecione a classe do rio:", bg='#94B7D5', font=('Arial', '12'))
    #classe1 = Radiobutton(canvas_entradas, text="Classe 1", bg='#94B7D5', variable=classe, value=1)
    #classe2 = Radiobutton(canvas_entradas, text="Classe 2", bg='#94B7D5', variable=classe, value=2)
    #classe3 = Radiobutton(canvas_entradas, text="Classe 3", bg='#94B7D5', variable=classe, value=3)
    #classe4 = Radiobutton(canvas_entradas, text="Classe 4", bg='#94B7D5', variable=classe, value=4)

    texto = Label(canvas_entradas, text="", bg='#94B7D5', font=('Arial', '12'))

    if modo_execucao.get() == "110":
        texto["text"] = "Simular Qualidade de Água: Poluição Pontual"
        texto.place(x=2, y=2)

        label_entrada_pontual = Label(canvas_entradas, width=70, text="Selecione a Entrada_Pontual.txt...", font=('Arial', '12'))
        label_entrada_constantes = Label(canvas_entradas, width=70, text="Selecione a Entrada_Constantes.txt...", font=('Arial', '12'))

        botao_entrada_pontual = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_pontual, 4))
        botao_entrada_constantes = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_constantes, 5))

        botao_reset_pontual = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_pontual, 4))
        botao_reset_constantes = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_constantes, 5))

        label_entrada_pontual.place(x=6, y=50)
        label_entrada_constantes.place(x=6, y=82)
        botao_entrada_pontual.place(x=650, y=50)
        botao_entrada_constantes.place(x=650, y=82)
        botao_reset_pontual.place(x=700, y=50)
        botao_reset_constantes.place(x=700, y=82)
        #label_classe.place(x=6, y=112)
        #classe1.place(x=6, y=137)
        #classe2.place(x=106, y=137)
        #classe3.place(x=206, y=137)
        #classe4.place(x=306, y=137)

        Muda_tela(janela_inicial, frame_simulacao)
    
    elif modo_execucao.get() == "101" or modo_execucao.get() == "111":
        if modo_execucao.get() == "101":
            texto["text"] = "Simular Qualidade de Água: Poluição Difusa"
        else:
            texto["text"] = "Simular Qualidade de Água: Poluição Pontual e Poluição Difusa"

        texto.place(x=2, y=2)

        label_entrada_hidro = Label(canvas_entradas, width=70, text="Selecione a Entrada_Hidro.txt...", font=('Arial', '12'))
        label_entrada_cme = Label(canvas_entradas, width=70, text="Selecione a Entrada_CME.txt...", font=('Arial', '12'))
        label_entrada_cn = Label(canvas_entradas, width=70, text="Selecione a Entrada_CN.txt...", font=('Arial', '12'))
        label_entrada_usos = Label(canvas_entradas, width=70, text="Selecione a Entrada_Usos.txt...", font=('Arial', '12'))
        label_entrada_pontual = Label(canvas_entradas, width=70, text="Selecione a Entrada_Pontual.txt...", font=('Arial', '12'))
        label_entrada_constantes = Label(canvas_entradas, width=70, text="Selecione a Entrada_Constantes.txt...", font=('Arial', '12'))

        botao_entrada_hidro = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_hidro, 0))
        botao_entrada_cme = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cme, 1))
        botao_entrada_cn = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cn, 2))
        botao_entrada_usos = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_usos, 3))
        botao_entrada_pontual = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_pontual, 4))
        botao_entrada_constantes = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_constantes, 5))

        botao_reset_hidro = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_hidro, 0))
        botao_reset_cme = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cme, 1))
        botao_reset_cn = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cn, 2))
        botao_reset_usos = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_usos, 3))
        botao_reset_pontual = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_pontual, 4))
        botao_reset_constantes = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_constantes, 5))

        label_entrada_hidro.place(x=6, y=50)
        label_entrada_cme.place(x=6, y=82)
        label_entrada_cn.place(x=6, y=114)
        label_entrada_usos.place(x=6, y=146)
        label_entrada_pontual.place(x=6, y=178)
        label_entrada_constantes.place(x=6, y=210)
        botao_entrada_hidro.place(x=650, y=50)
        botao_reset_hidro.place(x=700, y=50)
        botao_entrada_cme.place(x=650, y=82)
        botao_reset_cme.place(x=700, y=82)
        botao_entrada_cn.place(x=650, y=114)
        botao_reset_cn.place(x=700, y=114)
        botao_entrada_usos.place(x=650, y=146)
        botao_reset_usos.place(x=700, y=146)
        botao_entrada_pontual.place(x=650, y=178)
        botao_reset_pontual.place(x=700, y=178)
        botao_entrada_constantes.place(x=650, y=210)
        botao_reset_constantes.place(x=700, y=210)
        #label_classe.place(x=6, y=240)
        #classe1.place(x=6, y=265)
        #classe2.place(x=106, y=265)
        #classe3.place(x=206, y=265)
        #classe4.place(x=306, y=265)

        Muda_tela(janela_inicial, frame_simulacao)
    
    else:
        Janela_Erro()

def Janela_Simula_Escolhe_Otimizacao(janela_inicial, Tela):
    frame = Frame(Tela, height=600, width=800, bg='#94B7D5')
    canvas = Canvas(frame, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas.place(x=0, y=60)

    label = Label(frame, text="Otimização:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label.place(x=0,y=0)

    modo_otimizacao = IntVar()
    checa_ag = Radiobutton(canvas, text="Otimização com AG1", bg='#94B7D5', variable=modo_otimizacao, value=1)
    checa_ag.place(x=2, y=2)

    checa_agm = Radiobutton(canvas, text="Otimização com AG2", bg='#94B7D5', variable=modo_otimizacao, value=2)
    checa_agm.place(x=2, y=40)

    checa_brkga = Radiobutton(canvas, text="Otimização com BRKGA", bg='#94B7D5', variable=modo_otimizacao, value=3)
    checa_brkga.place(x=2, y=78)

    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_Simula_Otimizacao, janela_inicial, Tela, modo_otimizacao))
    botao_executa.place(x=550, y=560)

    Muda_tela(janela_inicial, frame)

def Janela_Simula_Otimizacao(janela_inicial, Tela, modo_otimizacao):
    frame = Frame(Tela, height=600, width=800, bg='#94B7D5')
    canvas = Canvas(frame, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas.place(x=0, y=60)

    if modo_otimizacao.get() == 1:
        label = Label(frame, text="Otimização com AG1:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    elif modo_otimizacao.get() == 2:
        label = Label(frame, text="Otimização com AG2:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    else:
        label = Label(frame, text="Otimização com BRKGA:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label.place(x=0,y=0)

    modo_simulacao = IntVar()
    checa_pontual = Radiobutton(canvas, text="Otimização de Fontes Pontuais", bg='#94B7D5', variable=modo_simulacao, value=1)
    checa_pontual.place(x=2, y=2)

    checa_difuso = Radiobutton(canvas, text="Otimização de Fontes Pontuais e de Fontes Difusas", bg='#94B7D5', variable=modo_simulacao, value=2)
    checa_difuso.place(x=2, y=40)

    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_Simula_Otimizacao_Modo, janela_inicial, Tela, modo_simulacao, modo_otimizacao))
    botao_executa.place(x=550, y=560)

    if modo_otimizacao.get() == 0:
        Janela_Erro()
    else:
        Muda_tela(janela_inicial, frame)

def Janela_Simula_Otimizacao_Modo(janela_inicial, Tela, modo_simulacao, modo_otimizacao):
    modo_execucao = StringVar()
    modo_execucao.set("2"+str(modo_simulacao.get()))
    classe = IntVar()

    vetor_caminhos = ["", "", "", "", "", "", ""]
    diretorio_saidas = StringVar()
    frame_simulacao = Frame(Tela, height=600, width=800, bg='#94B7D5')

    canvas_entradas = Canvas(frame_simulacao, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas_saida = Canvas(frame_simulacao, bg='#94B7D5', height=30, width=796, highlightbackground="black")
    entradas = Label(frame_simulacao, text="Selecione os Arquivos de Entrada:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label_saidas = Label(canvas_saida, width=70, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    botao_saidas = Button(canvas_saida, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_reset_saida = Button(canvas_saida, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_executa = Button(frame_simulacao, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, classe, modo_otimizacao))

    canvas_entradas.place(x=0, y=60)
    canvas_saida.place(x=0, y=515)
    entradas.place(x=0, y=0)
    label_saidas.place(x=6, y=4)
    botao_saidas.place(x=650, y=4)
    botao_reset_saida.place(x=700, y=4)
    botao_executa.place(x=550, y=560)

    #label_classe = Label(canvas_entradas, text="Selecione a classe do rio:", bg='#94B7D5', font=('Arial', '12'))
    #classe1 = Radiobutton(canvas_entradas, text="Classe 1", bg='#94B7D5', variable=classe, value=1)
    #classe2 = Radiobutton(canvas_entradas, text="Classe 2", bg='#94B7D5', variable=classe, value=2)
    #classe3 = Radiobutton(canvas_entradas, text="Classe 3", bg='#94B7D5', variable=classe, value=3)
    #classe4 = Radiobutton(canvas_entradas, text="Classe 4", bg='#94B7D5', variable=classe, value=4)

    texto = Label(canvas_entradas, text="", bg='#94B7D5', font=('Arial', '12'))

    if modo_execucao.get() == "21":
        if modo_otimizacao.get() == 1:
            texto["text"] = "Otimização de Fontes Pontuais com AG1"
        elif modo_otimizacao.get() == 2:
            texto["text"] = "Otimização de Fontes Pontuais com AG2"
        else:
            texto["text"] = "Otimização de Fontes Pontuais com BRKGA"
        texto.place(x=2, y=2)

        label_entrada_pontual = Label(canvas_entradas, width=70, text="Selecione a Entrada_Pontual.txt...", font=('Arial', '12'))
        label_entrada_constantes = Label(canvas_entradas, width=70, text="Selecione a Entrada_Constantes.txt...", font=('Arial', '12'))
        label_entrada_otimizacao = Label(canvas_entradas, width=70, text="Selecione a Entrada_Otimização.txt...", font=('Arial', '12'))

        botao_entrada_pontual = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_pontual, 4))
        botao_entrada_constantes = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_constantes, 5))
        botao_entrada_otimizacao = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_otimizacao, 6))

        botao_reset_pontual = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_pontual, 4))
        botao_reset_constantes = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_constantes, 5))
        botao_reset_otimizacao = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_otimizacao, 6))

        label_entrada_pontual.place(x=6, y=50)
        label_entrada_constantes.place(x=6, y=82)
        label_entrada_otimizacao.place(x=6, y=114)
        botao_entrada_pontual.place(x=650, y=50)
        botao_entrada_constantes.place(x=650, y=82)
        botao_entrada_otimizacao.place(x=650, y=114)
        botao_reset_pontual.place(x=700, y=50)
        botao_reset_constantes.place(x=700, y=82)
        botao_reset_otimizacao.place(x=700, y=114)
        #label_classe.place(x=6, y=144)
        #classe1.place(x=6, y=169)
        #classe2.place(x=106, y=169)
        #classe3.place(x=206, y=169)
        #classe4.place(x=306, y=169)

        Muda_tela(janela_inicial, frame_simulacao)
    
    elif modo_execucao.get() == "22":
        if modo_otimizacao.get() == 1:
            texto["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com AG1"
        elif modo_otimizacao.get() == 2:
            texto["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com AG2"
        else:
            texto["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com BRKGA"
        texto.place(x=2, y=2)

        label_entrada_hidro = Label(canvas_entradas, width=70, text="Selecione a Entrada_Hidro.txt...", font=('Arial', '12'))
        label_entrada_cme = Label(canvas_entradas, width=70, text="Selecione a Entrada_CME.txt...", font=('Arial', '12'))
        label_entrada_cn = Label(canvas_entradas, width=70, text="Selecione a Entrada_CN.txt...", font=('Arial', '12'))
        label_entrada_usos = Label(canvas_entradas, width=70, text="Selecione a Entrada_Usos.txt...", font=('Arial', '12'))
        label_entrada_pontual = Label(canvas_entradas, width=70, text="Selecione a Entrada_Pontual.txt...", font=('Arial', '12'))
        label_entrada_constantes = Label(canvas_entradas, width=70, text="Selecione a Entrada_Constantes.txt...", font=('Arial', '12'))
        label_entrada_otimizacao = Label(canvas_entradas, width=70, text="Selecione a Entrada_Otimização.txt...", font=('Arial', '12'))

        botao_entrada_hidro = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_hidro, 0))
        botao_entrada_cme = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cme, 1))
        botao_entrada_cn = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cn, 2))
        botao_entrada_usos = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_usos, 3))
        botao_entrada_pontual = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_pontual, 4))
        botao_entrada_constantes = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_constantes, 5))
        botao_entrada_otimizacao = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_otimizacao, 6))

        botao_reset_hidro = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_hidro, 0))
        botao_reset_cme = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cme, 1))
        botao_reset_cn = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cn, 2))
        botao_reset_usos = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_usos, 3))
        botao_reset_pontual = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_pontual, 4))
        botao_reset_constantes = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_constantes, 5))
        botao_reset_otimizacao = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_otimizacao, 6))

        label_entrada_hidro.place(x=6, y=50)
        label_entrada_cme.place(x=6, y=82)
        label_entrada_cn.place(x=6, y=114)
        label_entrada_usos.place(x=6, y=146)
        label_entrada_pontual.place(x=6, y=178)
        label_entrada_constantes.place(x=6, y=210)
        label_entrada_otimizacao.place(x=6, y=242)
        botao_entrada_hidro.place(x=650, y=50)
        botao_reset_hidro.place(x=700, y=50)
        botao_entrada_cme.place(x=650, y=82)
        botao_reset_cme.place(x=700, y=82)
        botao_entrada_cn.place(x=650, y=114)
        botao_reset_cn.place(x=700, y=114)
        botao_entrada_usos.place(x=650, y=146)
        botao_reset_usos.place(x=700, y=146)
        botao_entrada_pontual.place(x=650, y=178)
        botao_reset_pontual.place(x=700, y=178)
        botao_entrada_constantes.place(x=650, y=210)
        botao_reset_constantes.place(x=700, y=210)
        botao_entrada_otimizacao.place(x=650, y=242)
        botao_reset_otimizacao.place(x=700, y=242)
        #label_classe.place(x=6, y=272)
        #classe1.place(x=6, y=297)
        #classe2.place(x=106, y=297)
        #classe3.place(x=206, y=297)
        #classe4.place(x=306, y=297)

        Muda_tela(janela_inicial, frame_simulacao)
    
    else:
        Janela_Erro()

def Janela_Estima_Cargas_Difusas(janela_inicial, Tela, modo_execucao):
    modo_otimizacao = IntVar()
    modo_otimizacao.set("0")
    vetor_caminhos = ["", "", "", "", "", "", ""]
    diretorio_saidas = StringVar()
    frame_simulacao = Frame(Tela, height=600, width=800, bg='#94B7D5')

    canvas_entradas = Canvas(frame_simulacao, height=455, width=796, bg='#94B7D5', highlightbackground="black")
    canvas_saida = Canvas(frame_simulacao, bg='#94B7D5', height=30, width=796, highlightbackground="black")
    entradas = Label(frame_simulacao, text="Selecione os Arquivos de Entrada:", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label_saidas = Label(canvas_saida, width=70, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    botao_saidas = Button(canvas_saida, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_reset_saida = Button(canvas_saida, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_executa = Button(frame_simulacao, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, None, modo_otimizacao))

    canvas_entradas.place(x=0, y=60)
    canvas_saida.place(x=0, y=515)
    entradas.place(x=0, y=0)
    label_saidas.place(x=6, y=4)
    botao_saidas.place(x=650, y=4)
    botao_reset_saida.place(x=700, y=4)
    botao_executa.place(x=550, y=560)

    texto = Label(canvas_entradas, text="", bg='#94B7D5', font=('Arial', '12'))
    texto["text"] = "Estimar Cargas Difusas"
    texto.place(x=2, y=2)

    label_entrada_hidro = Label(canvas_entradas, width=70, text="Selecione a Entrada_Hidro.txt...", font=('Arial', '12'))
    label_entrada_cme = Label(canvas_entradas, width=70, text="Selecione a Entrada_CME.txt...", font=('Arial', '12'))
    label_entrada_cn = Label(canvas_entradas, width=70, text="Selecione a Entrada_CN.txt...", font=('Arial', '12'))
    label_entrada_usos = Label(canvas_entradas, width=70, text="Selecione a Entrada_Usos.txt...", font=('Arial', '12'))

    botao_entrada_hidro = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_hidro, 0))
    botao_entrada_cme = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cme, 1))
    botao_entrada_cn = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_cn, 2))
    botao_entrada_usos = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_usos, 3))

    botao_reset_hidro = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_hidro, 0))
    botao_reset_cme = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cme, 1))
    botao_reset_cn = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_cn, 2))
    botao_reset_usos = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_usos, 3))
    
    label_entrada_hidro.place(x=6, y=50)
    label_entrada_cme.place(x=6, y=81)
    label_entrada_cn.place(x=6, y=113)
    label_entrada_usos.place(x=6, y=145)
    botao_entrada_hidro.place(x=650, y=50)
    botao_reset_hidro.place(x=700, y=50)
    botao_entrada_cme.place(x=650, y=82)
    botao_reset_cme.place(x=700, y=82)
    botao_entrada_cn.place(x=650, y=114)
    botao_reset_cn.place(x=700, y=114)
    botao_entrada_usos.place(x=650, y=146)
    botao_reset_usos.place(x=700, y=146)

    Muda_tela(janela_inicial, frame_simulacao)


def Janela_Seleciona_Simulacao(janela_inicial, Tela, modo_simulacao):
    if modo_simulacao.get() == 1:
        Janela_Simula_Qualidade_Agua(janela_inicial, Tela)

    elif modo_simulacao.get() == 2:
        Janela_Estima_Cargas_Difusas(janela_inicial, Tela, modo_simulacao)

    elif modo_simulacao.get() == 3:
        Janela_Simula_Escolhe_Otimizacao(janela_inicial, Tela)

    else:
        Janela_Erro()

def Checa_Parametros_Entrada(vetor_caminhos, diretorio_saidas, modo_execucao, classe):
    if diretorio_saidas.get() == "":
        Janela_Erro()
        return 1
    elif modo_execucao.get() == "110" and (vetor_caminhos[4] == "" or vetor_caminhos[5] == ""):
        Janela_Erro()
        return 1
    elif modo_execucao.get() == "101" and (vetor_caminhos[0] == "" or vetor_caminhos[1] == "" or vetor_caminhos[2] == "" or vetor_caminhos[3] == "" or vetor_caminhos[4] == "" or vetor_caminhos[5] == ""):
        Janela_Erro()
        return 1
    elif modo_execucao.get() == 2 and (vetor_caminhos[0] == "" or vetor_caminhos[1] == "" or vetor_caminhos[2] == "" or vetor_caminhos[3] == ""):
        Janela_Erro()
        return 1
    elif modo_execucao.get() == "21" and (vetor_caminhos[4] == "" or vetor_caminhos[5] == "" or vetor_caminhos[6] == ""):
        Janela_Erro()
        return 1
    elif modo_execucao.get() == "22" and (vetor_caminhos.__contains__("")):
        Janela_Erro()
        return 1
    #elif classe is not None and classe.get() == 0:
        #Janela_Erro()
        #return 1
    return 0             

def Janela_saidas(janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, classe, modo_otimizacao):
    if Checa_Parametros_Entrada(vetor_caminhos, diretorio_saidas, modo_execucao, classe) == 0:
        diretorio_saidas = diretorio_saidas.get()

        frame_saidas = Frame(Tela, height=600, width=800, bg='#94B7D5')
        canvas_saidas = Canvas(frame_saidas, height=150, width=794, highlightbackground="black")
        canvas_saidas.place(x=0,y=30)
        label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))
        label_caixa_textos.place(x=2, y=2)

        Muda_tela(janela_inicial, frame_saidas)
        label_caixa_textos["text"] = label_caixa_textos["text"] + "Simulação Finalizada!\n"

        canvas_nova_simulacao = Canvas(frame_saidas, height=25, width=794, bg='#94B7D5', highlightbackground="black")
        canvas_nova_simulacao.place(x=0,y=550)
        botao_nova_simuacao = Button(canvas_nova_simulacao, width=30, text="Nova Simulação", command=partial(Janela_simulacao, janela_inicial, Tela))
        botao_nova_simuacao.place(x=575, y=2)

        if modo_execucao.get() != 2:
            leitor = Leitura()
            constantes = leitor.ler_constantes(vetor_caminhos[5][0])
            classe = constantes[37]

        if modo_execucao.get() == "110":
            canvas_graficos = Canvas(frame_saidas, height=280, width=794, bg='#94B7D5', highlightbackground="black")

            canvas_historico = Canvas(frame_saidas, height=70, width=794, bg='#94B7D5', highlightbackground="black")
            canvas_historico.place(x=0,y=180)

            label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
            label_vazao.place(x=2, y=2)
            botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
            botao_vazaoP.place(x=2, y=30)

            # Labels
            saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
            label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
            label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

            # Botões
            # cenario base pontual
            botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # Localizando todos os componentes
            canvas_graficos.place(x=0, y=250)
            saidas.place(x=0, y=0)
            label_graf.place(x=2, y=2)
            label_gbp.place(x=2, y=25)
            label_caixa_textos.place(x=2, y=2)
            botao_cbp_DBO.place(x=8, y=55)
            botao_cbp_OD.place(x=105, y=55)
            botao_cbp_NORG.place(x=205, y=55)
            botao_cbp_NAMON.place(x=305, y=55)
            botao_cbp_NNITR.place(x=405, y=55)
            botao_cbp_NNITRA.place(x=505, y=55)
            botao_cbp_PORG.place(x=605, y=55)
            botao_cbp_PINORG.place(x=705, y=55)

        elif modo_execucao.get() == "101":
            canvas_graficos = Canvas(frame_saidas, height=280, width=794, bg='#94B7D5', highlightbackground="black")

            canvas_historico = Canvas(frame_saidas, height=70, width=794, bg='#94B7D5', highlightbackground="black")
            canvas_historico.place(x=0,y=180)

            label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
            label_vazao.place(x=2, y=2)
            botao_vazao = Button(canvas_historico, width=11, text="Difuso")
            botao_vazao.place(x=2, y=30)

            # Labels
            saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
            label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
            label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
            label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

            # Botões
            # cenario base difuso
            botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # Localizando todos os componentes
            canvas_graficos.place(x=0, y=250)
            saidas.place(x=0, y=0)
            label_graf.place(x=2, y=2)
            label_gbd.place(x=2, y=25)
            label_caixa_textos.place(x=2, y=2)
            botao_cbd_DBO.place(x=8, y=55)
            botao_cbd_OD.place(x=105, y=55)
            botao_cbd_NORG.place(x=205, y=55)
            botao_cbd_NAMON.place(x=305, y=55)
            botao_cbd_NNITR.place(x=405, y=55)
            botao_cbd_NNITRA.place(x=505, y=55)
            botao_cbd_PORG.place(x=605, y=55)
            botao_cbd_PINORG.place(x=705, y=55)

        elif modo_execucao.get() == "111":
            canvas_graficos = Canvas(frame_saidas, height=280, width=794, bg='#94B7D5', highlightbackground="black")

            canvas_historico = Canvas(frame_saidas, height=70, width=794, bg='#94B7D5', highlightbackground="black")
            canvas_historico.place(x=0,y=180)

            label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
            label_vazao.place(x=2, y=2)
            botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
            botao_vazaoP.place(x=2, y=30)
            botao_vazao = Button(canvas_historico, width=11, text="Difuso")
            botao_vazao.place(x=102, y=30)

            # Labels
            saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
            label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
            label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
            label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

            # cenario base pontual
            botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # cenario base difuso
            botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            canvas_graficos.place(x=0, y=250)
            saidas.place(x=0, y=0)
            label_graf.place(x=2, y=2)
            label_gbp.place(x=2, y=25)
            label_gbd.place(x=2, y=85)
            label_caixa_textos.place(x=2, y=2)
            botao_cbp_DBO.place(x=8, y=55)
            botao_cbp_OD.place(x=105, y=55)
            botao_cbp_NORG.place(x=205, y=55)
            botao_cbp_NAMON.place(x=305, y=55)
            botao_cbp_NNITR.place(x=405, y=55)
            botao_cbp_NNITRA.place(x=505, y=55)
            botao_cbp_PORG.place(x=605, y=55)
            botao_cbp_PINORG.place(x=705, y=55)
            botao_cbd_DBO.place(x=8, y=115)
            botao_cbd_OD.place(x=105, y=115)
            botao_cbd_NORG.place(x=205, y=115)
            botao_cbd_NAMON.place(x=305, y=115)
            botao_cbd_NNITR.place(x=405, y=115)
            botao_cbd_NNITRA.place(x=505, y=115)
            botao_cbd_PORG.place(x=605, y=115)
            botao_cbd_PINORG.place(x=705, y=115)

        elif modo_execucao.get() == "21":
            canvas_graficos = Canvas(frame_saidas, height=280, width=794, bg='#94B7D5', highlightbackground="black")

            canvas_historico = Canvas(frame_saidas, height=70, width=794, bg='#94B7D5', highlightbackground="black")
            canvas_historico.place(x=0,y=180)

            label_fo = Label(canvas_historico, text="Gráfico da FO:", bg='#94B7D5', font=('Arial', '13'))
            label_fo.place(x=2, y=2)
            botao_foP = Button(canvas_historico, width=11, text="Pontual")
            botao_foP.place(x=2, y=30)

            label_tempo = Label(canvas_historico, text="Duração das Iterações:", bg='#94B7D5', font=('Arial', '13'))
            label_tempo.place(x=202, y=2)
            botao_tempoP = Button(canvas_historico, width=11, text="Pontual")
            botao_tempoP.place(x=202, y=30)

            label_invalidos = Label(canvas_historico, text="Filhos Inválidos:", bg='#94B7D5', font=('Arial', '13'))
            label_invalidos.place(x=402, y=2)
            botao_invalidosP = Button(canvas_historico, width=11, text="Pontual")
            botao_invalidosP.place(x=402, y=30)

            label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
            label_vazao.place(x=602, y=2)
            botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
            botao_vazaoP.place(x=602, y=30)

            # Labels
            saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
            label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
            label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_gop = Label(canvas_graficos, text="Cenário Otimizado Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

            # Botões
            # cenario base pontual
            botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # cenario otimizado pontual
            botao_cop_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cop_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cop_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cop_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cop_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cop_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cop_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cop_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # Localizando todos os componentes
            canvas_graficos.place(x=0, y=250)
            saidas.place(x=0, y=0)
            label_graf.place(x=2, y=2)
            label_gbp.place(x=2, y=25)
            label_gop.place(x=2, y=85)
            label_caixa_textos.place(x=2, y=2)
            botao_cbp_DBO.place(x=8, y=55)
            botao_cbp_OD.place(x=105, y=55)
            botao_cbp_NORG.place(x=205, y=55)
            botao_cbp_NAMON.place(x=305, y=55)
            botao_cbp_NNITR.place(x=405, y=55)
            botao_cbp_NNITRA.place(x=505, y=55)
            botao_cbp_PORG.place(x=605, y=55)
            botao_cbp_PINORG.place(x=705, y=55)
            botao_cop_DBO.place(x=8, y=115)
            botao_cop_OD.place(x=105, y=115)
            botao_cop_NORG.place(x=205, y=115)
            botao_cop_NAMON.place(x=305, y=115)
            botao_cop_NNITR.place(x=405, y=115)
            botao_cop_NNITRA.place(x=505, y=115)
            botao_cop_PORG.place(x=605, y=115)
            botao_cop_PINORG.place(x=705, y=115)
        
        elif modo_execucao.get() == "22":
            canvas_graficos = Canvas(frame_saidas, height=280, width=794, bg='#94B7D5', highlightbackground="black")

            canvas_historico = Canvas(frame_saidas, height=70, width=794, bg='#94B7D5', highlightbackground="black")
            canvas_historico.place(x=0,y=180)

            label_fo = Label(canvas_historico, text="Gráfico da FO:", bg='#94B7D5', font=('Arial', '13'))
            label_fo.place(x=2, y=2)
            botao_foP = Button(canvas_historico, width=11, text="Pontual")
            botao_foP.place(x=2, y=30)
            botao_fo = Button(canvas_historico, width=11, text="Difusa")
            botao_fo.place(x=102, y=30)

            label_tempo = Label(canvas_historico, text="Duração das Iterações:", bg='#94B7D5', font=('Arial', '13'))
            label_tempo.place(x=202, y=2)
            botao_tempoP = Button(canvas_historico, width=11, text="Pontual")
            botao_tempoP.place(x=202, y=30)
            botao_tempo = Button(canvas_historico, width=11, text="Difusa")
            botao_tempo.place(x=302, y=30)

            label_invalidos = Label(canvas_historico, text="Filhos Inválidos:", bg='#94B7D5', font=('Arial', '13'))
            label_invalidos.place(x=402, y=2)
            botao_invalidosP = Button(canvas_historico, width=11, text="Pontual")
            botao_invalidosP.place(x=402, y=30)
            botao_invalidos = Button(canvas_historico, width=11, text="Difusa")
            botao_invalidos.place(x=502, y=30)

            label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
            label_vazao.place(x=602, y=2)
            botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
            botao_vazaoP.place(x=602, y=30)
            botao_vazao = Button(canvas_historico, width=11, text="Difuso")
            botao_vazao.place(x=702, y=30)

            # Labels
            saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
            label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
            label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_gop = Label(canvas_graficos, text="Cenário Otimizado Pontual:", bg='#94B7D5', font=('Arial', '11'))
            label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
            label_god = Label(canvas_graficos, text="Cenário Otimizado Difuso:", bg='#94B7D5', font=('Arial', '11'))
            label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

            # Botões
            # cenario base pontual
            botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # cenario otimizado pontual
            botao_cop_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cop_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cop_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cop_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cop_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cop_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cop_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cop_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # cenario base difuso
            botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # cenario otimizado difuso
            botao_cod_DBO = Button(canvas_graficos, width=11, text="DBO")
            botao_cod_OD = Button(canvas_graficos, width=11, text="OD")
            botao_cod_NORG = Button(canvas_graficos, width=11, text="Norg")
            botao_cod_NAMON = Button(canvas_graficos, width=11, text="Namon")
            botao_cod_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
            botao_cod_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
            botao_cod_PORG = Button(canvas_graficos, width=11, text="Porg")
            botao_cod_PINORG = Button(canvas_graficos, width=11, text="Pinorg")

            # Localizando todos os componentes
            canvas_graficos.place(x=0, y=250)
            saidas.place(x=0, y=0)
            label_graf.place(x=2, y=2)
            label_gbp.place(x=2, y=25)
            label_gop.place(x=2, y=85)
            label_gbd.place(x=2, y=145)
            label_god.place(x=2, y=205)
            label_caixa_textos.place(x=2, y=2)
            botao_cbp_DBO.place(x=8, y=55)
            botao_cbp_OD.place(x=105, y=55)
            botao_cbp_NORG.place(x=205, y=55)
            botao_cbp_NAMON.place(x=305, y=55)
            botao_cbp_NNITR.place(x=405, y=55)
            botao_cbp_NNITRA.place(x=505, y=55)
            botao_cbp_PORG.place(x=605, y=55)
            botao_cbp_PINORG.place(x=705, y=55)
            botao_cop_DBO.place(x=8, y=115)
            botao_cop_OD.place(x=105, y=115)
            botao_cop_NORG.place(x=205, y=115)
            botao_cop_NAMON.place(x=305, y=115)
            botao_cop_NNITR.place(x=405, y=115)
            botao_cop_NNITRA.place(x=505, y=115)
            botao_cop_PORG.place(x=605, y=115)
            botao_cop_PINORG.place(x=705, y=115)
            botao_cbd_DBO.place(x=8, y=175)
            botao_cbd_OD.place(x=105, y=175)
            botao_cbd_NORG.place(x=205, y=175)
            botao_cbd_NAMON.place(x=305, y=175)
            botao_cbd_NNITR.place(x=405, y=175)
            botao_cbd_NNITRA.place(x=505, y=175)
            botao_cbd_PORG.place(x=605, y=175)
            botao_cbd_PINORG.place(x=705, y=175)
            botao_cod_DBO.place(x=8, y=235)
            botao_cod_OD.place(x=105, y=235)
            botao_cod_NORG.place(x=205, y=235)
            botao_cod_NAMON.place(x=305, y=235)
            botao_cod_NNITR.place(x=405, y=235)
            botao_cod_NNITRA.place(x=505, y=235)
            botao_cod_PORG.place(x=605, y=235)
            botao_cod_PINORG.place(x=705, y=235)
        
        [cenario_base_pontual, cenario_otimizado_pontual, cenario_base_difuso, cenario_otimizado_difuso,
        historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes,
        historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida,
        tam_rio, tam_cel, ph, perfilQP, perfilQ] = executa(vetor_caminhos, diretorio_saidas, modo_execucao, label_caixa_textos, classe, modo_otimizacao)

        if modo_execucao.get() != 2:
            restricao_DBO = cria_vetor_restricao(0, tam_rio, tam_cel, ph, classe)
            restricao_OD = cria_vetor_restricao(1, tam_rio, tam_cel, ph, classe)
            restricao_NAMON = cria_vetor_restricao(3, tam_rio, tam_cel, ph, classe)
            restricao_NNITR = cria_vetor_restricao(4, tam_rio, tam_cel, ph, classe)
            restricao_NNITRA = cria_vetor_restricao(5, tam_rio, tam_cel, ph, classe)
            restricao_PORG = cria_vetor_restricao(6, tam_rio, tam_cel, ph, classe)

        if modo_execucao.get() == "110":
            # cenario vazao
            botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)

            # cenario base pontual
            botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG
        
        elif modo_execucao.get() == "101":
            # cenario vazao
            botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

            # cenario base difuso
            botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG
        
        elif modo_execucao.get() == "111":
            # cenario vazao
            botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)
            botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

            # cenario base pontual
            botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG"

            # cenario base difuso
            botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difuso[0].Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG
        
        elif modo_execucao.get() == "21":
            # cenario fo
            botao_foP["command"] = partial(gera_grafico_fo, historico_foP, iteracao_versao_rapidaP)

            # cenario do tempo das iteracoes
            botao_tempoP["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoesP, iteracao_versao_rapidaP)

            # cenario filhos invalidos
            botao_invalidosP["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidosP, iteracao_versao_rapidaP)

            # cenario vazao
            botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)

            # cenario base pontual
            botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual.Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

            # cenario otimizado pontual
            botao_cop_DBO["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cop_OD["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cop_NORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cop_NAMON["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cop_NNITR["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cop_NNITRA["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cop_PORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cop_PINORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

        elif modo_execucao.get() == "22":
            # cenario fo
            botao_foP["command"] = partial(gera_grafico_fo, historico_foP, iteracao_versao_rapidaP)
            botao_fo["command"] = partial(gera_grafico_fo, historico_fo, iteracao_versao_rapida)

            # cenario do tempo das iteracoes
            botao_tempoP["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoesP, iteracao_versao_rapidaP)
            botao_tempo["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoes, iteracao_versao_rapida)

            # cenario filhos invalidos
            botao_invalidosP["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidosP, iteracao_versao_rapidaP)
            botao_invalidos["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidos, iteracao_versao_rapida)

            # cenario vazao
            botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)
            botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

            # cenario base pontual
            botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual.Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

            # cenario otimizado pontual
            botao_cop_DBO["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cop_OD["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cop_NORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cop_NAMON["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cop_NNITR["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cop_NNITRA["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cop_PORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cop_PINORG["command"] = partial(gera_grafico, cenario_otimizado_pontual.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

            # cenario base difuso
            botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difuso.Y_DBO[0], 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difuso.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difuso.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difuso.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difuso.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difuso.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difuso.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difuso.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

            # cenario otimizado difuso
            botao_cod_DBO["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_DBO[0], 0,restricao_DBO, tam_cel, tam_rio, classe)  # DBO
            botao_cod_OD["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_DBO[2], 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
            botao_cod_NORG["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Nitr[0], 2, None, tam_cel, tam_rio, classe)  # NORG
            botao_cod_NAMON["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Nitr[1], 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
            botao_cod_NNITR["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Nitr[2], 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
            botao_cod_NNITRA["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Nitr[3], 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
            botao_cod_PORG["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Fosf[0], 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
            botao_cod_PINORG["command"] = partial(gera_grafico, cenario_otimizado_difuso.Y_Fosf[1], 7, None, tam_cel, tam_rio, classe)  # PINORG

def Janela_inicial():
    Tela = Tk()
    janela_inicial = Frame(Tela, height=600, width=800, bg='#94B7D5')

    titulo = Label(janela_inicial, text="SIMPPOD", bg='#94B7D5', font=('Arial', '75', 'bold'))
    sub_titulo = Label(janela_inicial, text="Sistema de Modelagem de Poluição Pontual e Difusa", bg='#94B7D5', font=('Arial', '12'))

    sobre = Button(janela_inicial, text="Sobre o SIMPPOD", command=Sobre)
    botao_simulacao = Button(janela_inicial, text="Simulações", command=partial(Janela_simulacao, janela_inicial, Tela))

    janela_inicial.place(x=0, y=0)

    titulo.place(x=170, y=200)
    sub_titulo.place(x=210, y=300)
    botao_simulacao.place(x=600, y=500)
    sobre.place(x=75, y=500)

    Tela["bg"] = '#94B7D5'
    Tela.title("SIMPPOD - Sistema de Modelagem de Poluição Pontual e Difusa")
    Tela.geometry("800x600")
    Tela.mainloop()

Janela_inicial()
