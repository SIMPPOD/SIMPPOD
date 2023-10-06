# -*- coding: utf-8 -*-
# Modulo: interface

from Leitura import *
from Gera_Gráficos import *
from Main import executa

from tkinter.messagebox import showerror, showinfo
from tkinter.font import Font
from tkinter import Tk, LEFT
from tkinter import Button, Checkbutton, Radiobutton
from tkinter import IntVar, StringVar
from tkinter import Canvas, Frame, Label
from tkinter import filedialog

from functools import partial

import matplotlib.backend_managers
matplotlib.use('TkAgg')

def le_arquivo(vetor_caminhos, label, indice):
    nome_do_arquivo = filedialog.askopenfilenames()
    if not str(nome_do_arquivo).__eq__(""):
        label["text"] = nome_do_arquivo
        vetor_caminhos[indice] = nome_do_arquivo

def le_saida(diretorio_saidas, label):
    nome_do_diretorio = filedialog.askdirectory()
    if not str(nome_do_diretorio).__eq__(""):
        label["text"] = nome_do_diretorio
        diretorio_saidas.set(nome_do_diretorio)
        
def reset_botao(vetor_caminhos, label, indice):
    vetor_caminhos[indice] = ""
    if indice == 0:
        label["text"] = "Selecione o Arquivo de Entrada do Rio Principal..."
    else:
        label["text"] = "Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)..."

def reset_saida(diretorio_saidas, label):
    diretorio_saidas.set("")
    label["text"] = "Selecione o caminho para as Saidas..."

def Janela_inicial():
    Tela = Tk()
    Tela.resizable(0, 0)
    janela_inicial = Frame(Tela, height=600, width=950, bg='#94B7D5')
    janela_inicial.place(x=0, y=0)

    titulo = Label(janela_inicial, text="SIMPPOD", bg='#94B7D5', font=('Arial', '75', 'bold'))
    length = Font(family='Arial', size=75, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=200)

    sub_titulo = Label(janela_inicial, text="Sistema Integrado de Modelagem de Poluição Pontual e Difusa", bg='#94B7D5', font=('Arial', '12'))
    length = Font(family='Arial', size=12).measure(sub_titulo["text"])
    sub_titulo.place(x=(950-length)/2, y=300)

    sobre = Button(janela_inicial, text="Sobre o SIMPPOD", command=Sobre)
    sobre.place(x=130, y=500)

    botao_simulacao = Button(janela_inicial, text="Simulações", command=partial(Janela_simulacao, janela_inicial, Tela))
    botao_simulacao.place(x=715, y=500)

    Tela["bg"] = '#94B7D5'
    Tela.title("SIMPPOD - Sistema Integrado de Modelagem de Poluição Pontual e Difusa")
    Tela.geometry("950x600")
    Tela.mainloop()

def Sobre():
    janela = Tk()
    janela.geometry("600x330")
    janela.resizable(0, 0)
    janela.title("SIMPPOD - Sistema Integrado de Modelagem de Poluição Pontual e Difusa")
    texto = "O SIMPPOD é um sistema de suporte a decisão, que permite ao usuário estimar a produção de cargas difusas, simular perfil de qualidade de água em rios a partir de entrada de fontes pontuais e difusas, e identificar os percentuais de remoção/redução necessários a serem aplicados a estas cargas de modo a garantir a classe de qualidade de água desejada pelo usuário.\n\nO SIMPPOD é portanto um sistema de suporte ao enquadramento e ao planejamento e gestão de recursos hídricos. É composto por um modelo de qualidade de água (Qual-UFMG), um modelo de estimativa de cargas difusas, e dois algoritmos de otimização para fontes pontuais e difusas (AGOFP e AGOFD, respectivamente).\n\nPara a otimização, o SIMPPOD dispõe de três opções de método, sendo estes diferentes modalidades de Algoritmos Genéticos, a saber:\n- AG Clássico: algoritmo genético com mutação;\n- AG+: algoritmo genético com mutação e elitismo;\n- BRKGA: algoritmo genético com chaves aleatórias viciadas."
    sobre = Label(janela, wraplength=600, pady=20, text=texto, font="Arial 12", justify=LEFT)
    sobre.pack()
    janela.mainloop()

def Muda_tela(janela_inicial, novo_frame):
    janela_inicial.pack_forget()
    janela_inicial = novo_frame
    janela_inicial.place(x=0, y=0)

def Janela_inicio(Tela):
    janela_inicial = Frame(Tela, height=600, width=950, bg='#94B7D5')
    janela_inicial.place(x=0, y=0)

    titulo = Label(janela_inicial, text="SIMPPOD", bg='#94B7D5', font=('Arial', '75', 'bold'))
    length = Font(family='Arial', size=75, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=200)

    sub_titulo = Label(janela_inicial, text="Sistema Integrado de Modelagem de Poluição Pontual e Difusa", bg='#94B7D5', font=('Arial', '12'))
    length = Font(family='Arial', size=12).measure(sub_titulo["text"])
    sub_titulo.place(x=(950-length)/2, y=300)

    sobre = Button(janela_inicial, text="Sobre o SIMPPOD", command=Sobre)
    sobre.place(x=130, y=500)

    botao_simulacao = Button(janela_inicial, text="Simulações", command=partial(Janela_simulacao, janela_inicial, Tela))
    botao_simulacao.place(x=715, y=500)

    Muda_tela(janela_inicial, janela_inicial)

def Janela_simulacao(janela_inicial, Tela):
    modo_simulacao = IntVar()

    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, text="Selecione o modo de execução:", bg='#94B7D5', font=('Arial', '18', 'bold'))
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)
    
    canvas_selecao = Canvas(frame, height=155, width=946, bg='#94B7D5', highlightbackground="black")
    canvas_selecao.place(x=0, y=100)
    checa_pontual = Radiobutton(canvas_selecao, text="Simular Qualidade de Água",bg='#94B7D5', font=('Arial', '14'),variable=modo_simulacao, value=1)
    checa_pontual.place(x=2, y=15)
    checa_pd = Radiobutton(canvas_selecao, text="Estimar Cargas Difusas", bg='#94B7D5', font=('Arial', '14'), variable=modo_simulacao, value=2)
    checa_pd.place(x=2, y=65)
    checa_brkga = Radiobutton(canvas_selecao, text="Otimização", bg='#94B7D5', font=('Arial', '14'), variable=modo_simulacao, value=3)   
    checa_brkga.place(x=2, y=115)

    label_simula = Label(frame, text="O que deseja simular?", bg='#94B7D5', font=('Arial', '14', 'bold'))
    label_simula.place(x=2,y=300)

    simula_rio = IntVar()
    checa_rio = Checkbutton(frame, text="Rio Principal", bg='#94B7D5', font=('Arial', '12'), variable=simula_rio)
    checa_rio.place(x=2, y=330)

    simula_tributarios = IntVar()
    checa_tributarios = Checkbutton(frame, text="Tributário(s)", bg='#94B7D5', font=('Arial', '12'), variable=simula_tributarios)
    checa_tributarios.place(x=150, y=330)

    botao_executa = Button(frame, width=30, text="Avançar", command=partial(Janela_Seleciona_Simulacao, janela_inicial, Tela, modo_simulacao, simula_rio, simula_tributarios))
    botao_executa.place(x=550, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_inicio, Tela))
    botao_voltar.place(x=130, y=500)

    Muda_tela(janela_inicial, frame)

def Janela_Seleciona_Simulacao(janela_inicial, Tela, modo_simulacao, simula_rio, simula_tributarios):
    if not simula_rio.get() and not simula_tributarios.get():
        Janela_Erro()

    elif modo_simulacao.get() == 1:
        Janela_Simula_Qualidade_Agua(janela_inicial, Tela, simula_rio, simula_tributarios)

    elif modo_simulacao.get() == 2:
        Janela_Estima_Cargas_Difusas(janela_inicial, Tela, modo_simulacao, simula_rio, simula_tributarios)

    elif modo_simulacao.get() == 3:
        Janela_Simula_Escolhe_Otimizacao(janela_inicial, Tela, simula_rio, simula_tributarios)

    else:
        Janela_Erro()

def Janela_Erro():
    showerror("Error", "ENTRADAS INVÁLIDAS!")

def Janela_Simula_Qualidade_Agua(janela_inicial, Tela, simula_rio, simula_tributarios):
    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, text="Simular Qualidade de Água:", bg='#94B7D5', font=('Arial', '18', 'bold'))
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas_selecao = Canvas(frame, height=105, width=946, bg='#94B7D5', highlightbackground="black")
    canvas_selecao.place(x=0, y=100)

    simula_pontual = IntVar()
    checa_pontual = Checkbutton(canvas_selecao, text="Simular Perfil de Qualidade de Água - Poluição Pontual", bg='#94B7D5', font=('Arial', '14'), variable=simula_pontual)
    checa_pontual.place(x=2, y=15)

    simula_difuso = IntVar()
    checa_difuso = Checkbutton(canvas_selecao, text="Simular Perfil de Qualidade de Água - Poluição Difusa", bg='#94B7D5', font=('Arial', '14'), variable=simula_difuso)
    checa_difuso.place(x=2, y=65)

    botao_executa = Button(frame, width=30, text="Avançar", command=partial(Janela_Simula_Qualidade_Agua_Modo, janela_inicial, Tela, simula_pontual, simula_difuso, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_simulacao, janela_inicial, Tela))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    Muda_tela(janela_inicial, frame)    

def Janela_Simula_Qualidade_Agua_Modo(janela_inicial, Tela, simula_pontual, simula_difuso, simula_rio, simula_tributarios):
    modo_otimizacao = IntVar()
    modo_otimizacao.set(0)
    modo_execucao = StringVar()
    modo_execucao.set("1"+str(simula_pontual.get())+str(simula_difuso.get()))
    vetor_caminhos = ["", ""]
    diretorio_saidas = StringVar()

    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, bg='#94B7D5', font=('Arial', '18', 'bold'))
    if modo_execucao.get() == "110":
        titulo["text"] = "Simular Qualidade de Água: Poluição Pontual"    
    elif modo_execucao.get() == "101":
        titulo["text"] = "Simular Qualidade de Água: Poluição Difusa"
    elif modo_execucao.get() == "111":
        titulo["text"] = "Simular Qualidade de Água: Poluição Pontual e Poluição Difusa" 
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas_entradas = Canvas(frame, height=320, width=946, bg='#94B7D5', highlightbackground="black")
    if simula_rio.get() and not simula_tributarios.get():
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)
    
    elif not simula_rio.get() and simula_tributarios.get():
        label_tributarios = Label(canvas_entradas, text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=20)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=54)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=50)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=50)

    else:
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)

        label_tributarios = Label(canvas_entradas,text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=130)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=164)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=160)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=160)

    label_saida = Label(canvas_entradas, text="Saídas:", bg='#94B7D5', font=('Arial', '12', 'bold'))
    label_saida.place(x=6, y=240)
    label_saidas = Label(canvas_entradas, width=87, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    label_saidas.place(x=6, y=274)
    botao_saidas = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_saidas.place(x=800, y=270)
    botao_reset_saida = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_reset_saida.place(x=870, y=270)

    canvas_entradas.place(x=0, y=100)
    
    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, modo_otimizacao, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_Simula_Qualidade_Agua, janela_inicial, Tela, simula_rio, simula_tributarios))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    if modo_execucao.get() != "110" and modo_execucao.get() != "101" and modo_execucao.get() != "111":
        Janela_Erro()
    else: 
        Muda_tela(janela_inicial, frame)

def Janela_Estima_Cargas_Difusas(janela_inicial, Tela, modo_execucao, simula_rio, simula_tributarios):
    modo_otimizacao = IntVar()
    modo_otimizacao.set("0")
    vetor_caminhos = ["", ""]
    diretorio_saidas = StringVar()
    
    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, bg='#94B7D5', text="Estimar Cargas Difusas", font=('Arial', '18', 'bold'))
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas_entradas = Canvas(frame, height=320, width=946, bg='#94B7D5', highlightbackground="black")
    if simula_rio.get() and not simula_tributarios.get():
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)
    
    elif not simula_rio.get() and simula_tributarios.get():
        label_tributarios = Label(canvas_entradas, text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=20)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=54)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=50)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=50)

    else:
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)

        label_tributarios = Label(canvas_entradas,text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=130)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=164)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=160)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=160)

    label_saida = Label(canvas_entradas, text="Saídas:", bg='#94B7D5', font=('Arial', '12', 'bold'))
    label_saida.place(x=6, y=240)
    label_saidas = Label(canvas_entradas, width=87, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    label_saidas.place(x=6, y=274)
    botao_saidas = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_saidas.place(x=800, y=270)
    botao_reset_saida = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_reset_saida.place(x=870, y=270)

    canvas_entradas.place(x=0, y=100)

    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, modo_otimizacao, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_simulacao, janela_inicial, Tela))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    Muda_tela(janela_inicial, frame)

def Janela_Simula_Escolhe_Otimizacao(janela_inicial, Tela, simula_rio, simula_tributarios):
    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, text="Simular Modelo de Otimização:", bg='#94B7D5', font=('Arial', '18', 'bold'))
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas = Canvas(frame, height=155, width=946, bg='#94B7D5', highlightbackground="black")
    canvas.place(x=0, y=100)

    modo_otimizacao = IntVar()
    checa_ag = Radiobutton(canvas, text="Otimização com AG Clássico", bg='#94B7D5', font=('Arial', '14'), variable=modo_otimizacao, value=1)
    checa_ag.place(x=2, y=15)

    checa_agm = Radiobutton(canvas, text="Otimização com AG+", bg='#94B7D5', font=('Arial', '14'), variable=modo_otimizacao, value=2)
    checa_agm.place(x=2, y=65)

    checa_brkga = Radiobutton(canvas, text="Otimização com BRKGA", bg='#94B7D5', font=('Arial', '14'), variable=modo_otimizacao, value=3)
    checa_brkga.place(x=2, y=115)

    botao_executa = Button(frame, width=30, text="Avançar", command=partial(Janela_Simula_Otimizacao, janela_inicial, Tela, modo_otimizacao, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_simulacao, janela_inicial, Tela))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    Muda_tela(janela_inicial, frame)

def Janela_Simula_Otimizacao(janela_inicial, Tela, modo_otimizacao, simula_rio, simula_tributarios):
    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, bg='#94B7D5', font=('Arial', '18', 'bold'))
    if modo_otimizacao.get() == 1:
        titulo["text"] = "Otimização com AG Clássico:"
    elif modo_otimizacao.get() == 2:
        titulo["text"] = "Otimização com AG+:"
    else:
        titulo["text"] = "Otimização com BRKGA:"
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas = Canvas(frame, height=105, width=946, bg='#94B7D5', highlightbackground="black")
    canvas.place(x=0, y=100)

    modo_simulacao = IntVar()
    checa_pontual = Radiobutton(canvas, text="Otimização de Fontes Pontuais", bg='#94B7D5', font=('Arial', '14'), variable=modo_simulacao, value=1)
    checa_pontual.place(x=2, y=15)

    checa_difuso = Radiobutton(canvas, text="Otimização de Fontes Pontuais e de Fontes Difusas", bg='#94B7D5', font=('Arial', '14'), variable=modo_simulacao, value=2)
    checa_difuso.place(x=2, y=65)

    botao_executa = Button(frame, width=30, text="Avançar", command=partial(Janela_Simula_Otimizacao_Modo, janela_inicial, Tela, modo_simulacao, modo_otimizacao, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_Simula_Escolhe_Otimizacao, janela_inicial, Tela, simula_rio, simula_tributarios))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    if modo_otimizacao.get() == 0:
        Janela_Erro()
    else:
        Muda_tela(janela_inicial, frame)

def Janela_Simula_Otimizacao_Modo(janela_inicial, Tela, modo_simulacao, modo_otimizacao, simula_rio, simula_tributarios):
    modo_execucao = StringVar()
    modo_execucao.set("2"+str(modo_simulacao.get()))
    vetor_caminhos = ["", ""]
    diretorio_saidas = StringVar()

    frame = Frame(Tela, height=600, width=950, bg='#94B7D5')

    titulo = Label(frame, bg='#94B7D5', font=('Arial', '18', 'bold'))
    if modo_execucao.get() == "21":
        if modo_otimizacao.get() == 1:
            titulo["text"] = "Otimização de Fontes Pontuais com AG Clássico"
        elif modo_otimizacao.get() == 2:
            titulo["text"] = "Otimização de Fontes Pontuais com AG+"
        else:
            titulo["text"] = "Otimização de Fontes Pontuais com BRKGA"
   
    elif modo_execucao.get() == "22":
        if modo_otimizacao.get() == 1:
            titulo["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com AG Clássico"
        elif modo_otimizacao.get() == 2:
            titulo["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com AG+"
        else:
            titulo["text"] = "Otimização de Fontes Pontuais e de Fontes Difusas com BRKGA"
    length = Font(family='Arial', size=18, weight='bold').measure(titulo["text"])
    titulo.place(x=(950-length)/2, y=35)

    canvas_entradas = Canvas(frame, height=320, width=946, bg='#94B7D5', highlightbackground="black")
    if simula_rio.get() and not simula_tributarios.get():
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)
    
    elif not simula_rio.get() and simula_tributarios.get():
        label_tributarios = Label(canvas_entradas, text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=20)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=54)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=50)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=50)

    else:
        label_rio = Label(canvas_entradas, text="Rio Principal:", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_rio.place(x=6, y=20)
        label_entrada_rio = Label(canvas_entradas, width=87, text="Selecione o Arquivo de Entrada do Rio Principal...", font=('Arial', '12'))
        label_entrada_rio.place(x=6, y=54)
        botao_entrada_rio = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_rio, 0))
        botao_entrada_rio.place(x=800, y=50)
        botao_reset_rio = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_rio, 0))
        botao_reset_rio.place(x=870, y=50)

        label_tributarios = Label(canvas_entradas,text="Tributário(s):", bg='#94B7D5', font=('Arial', '12', 'bold'))
        label_tributarios.place(x=6, y=130)
        label_entrada_tributarios = Label(canvas_entradas, width=87, text="Selecione o(s) Arquivo(s) de Entrada do(s) Tributário(s)...", font=('Arial', '12'))
        label_entrada_tributarios.place(x=6, y=164)
        botao_entrada_tributarios = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_arquivo, vetor_caminhos, label_entrada_tributarios, 1))
        botao_entrada_tributarios.place(x=800, y=160)
        botao_reset_tributarios = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_botao, vetor_caminhos, label_entrada_tributarios, 1))
        botao_reset_tributarios.place(x=870, y=160)

    label_saida = Label(canvas_entradas, text="Saídas:", bg='#94B7D5', font=('Arial', '12', 'bold'))
    label_saida.place(x=6, y=240)
    label_saidas = Label(canvas_entradas, width=87, text="Selecione o caminho para as Saidas...", font=('Arial', '12'))
    label_saidas.place(x=6, y=274)
    botao_saidas = Button(canvas_entradas, width=5, text="Abrir", command=partial(le_saida, diretorio_saidas, label_saidas))
    botao_saidas.place(x=800, y=270)
    botao_reset_saida = Button(canvas_entradas, width=5, text="Reset", command=partial(reset_saida, diretorio_saidas, label_saidas))
    botao_reset_saida.place(x=870, y=270)

    canvas_entradas.place(x=0, y=100)
    
    botao_executa = Button(frame, width=30, text="Executar", command=partial(Janela_saidas, janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, modo_otimizacao, simula_rio, simula_tributarios))
    botao_executa.place(x=650, y=500)

    botao_voltar = Button(frame, width=30, text="Voltar", command=partial(Janela_Simula_Otimizacao, janela_inicial, Tela, modo_otimizacao, simula_rio, simula_tributarios))
    botao_voltar.place(x=30, y=500)

    botao_home = Button(frame, width=30, text="Início", command=partial(Janela_inicio, Tela))
    botao_home.place(x=340, y=500)

    if modo_execucao.get() != "21" and modo_execucao.get() != "22":
        Janela_Erro()
    else:
        Muda_tela(janela_inicial, frame)

def Janela_saidas(janela_inicial, Tela, vetor_caminhos, diretorio_saidas, modo_execucao, modo_otimizacao, simula_rio, simula_tributarios):
    diretorio_saidas = diretorio_saidas.get()

    frame_saidas = Frame(Tela, height=600, width=950, bg='#94B7D5')
    canvas_saidas = Canvas(frame_saidas, width=946, highlightbackground="black")
    canvas_saidas.place(x=0,y=30)
    label_caixa_textos = Label(canvas_saidas, justify=LEFT, font=('Arial', '10'))
    label_caixa_textos.place(x=2, y=2)
    
    label_caixa_textos["text"] = "\nSimulação Finalizada!\n"

    canvas_nova_simulacao = Canvas(frame_saidas, height=25, width=946, bg='#94B7D5', highlightbackground="black")
    canvas_nova_simulacao.place(x=0,y=550)
    botao_nova_simuacao = Button(canvas_nova_simulacao, width=30, text="Nova Simulação", command=(Tela.destroy and partial(Janela_simulacao, janela_inicial, Tela)))
    botao_nova_simuacao.place(x=700, y=2)

    if diretorio_saidas == "" or (simula_rio.get() and vetor_caminhos[0] == "") or (simula_tributarios.get() and vetor_caminhos[1] == ""):
        Janela_Erro()
    else:
        [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
        historico_foP, historico_fo, historico_tempo_iteracoesP, historico_tempo_iteracoes,
        historico_filhos_invalidosP, historico_filhos_invalidos, iteracao_versao_rapidaP, iteracao_versao_rapida,
        tam_rio, tam_cel, ph, perfilQP, perfilQ] = executa(vetor_caminhos, diretorio_saidas, modo_execucao, label_caixa_textos, modo_otimizacao, simula_rio, simula_tributarios)

        Muda_tela(janela_inicial, frame_saidas)

        if simula_rio.get() or (not simula_rio.get() and len(vetor_caminhos[1]) == 1):
            if modo_execucao.get() != 2:
                if simula_rio.get():
                    constantes = ler_entrada_constantes(vetor_caminhos[0])
                else:
                    constantes = ler_entrada_constantes(vetor_caminhos[1][0])
                classe = int(constantes[2])
                restricao_DBO = cria_vetor_restricao(0, tam_rio, tam_cel, ph, classe)
                restricao_OD = cria_vetor_restricao(1, tam_rio, tam_cel, ph, classe)
                restricao_NAMON = cria_vetor_restricao(3, tam_rio, tam_cel, ph, classe)
                restricao_NNITR = cria_vetor_restricao(4, tam_rio, tam_cel, ph, classe)
                restricao_NNITRA = cria_vetor_restricao(5, tam_rio, tam_cel, ph, classe)
                restricao_PORG = cria_vetor_restricao(6, tam_rio, tam_cel, ph, classe)
                restricao_COL = cria_vetor_restricao(8, tam_rio, tam_cel, ph, classe)

            if modo_execucao.get() == "110":
                canvas_graficos = Canvas(frame_saidas, height=280, width=944, bg='#94B7D5', highlightbackground="black")

                canvas_historico = Canvas(frame_saidas, height=70, width=944, bg='#94B7D5', highlightbackground="black")
                canvas_historico.place(x=0,y=180)

                label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
                label_vazao.place(x=2, y=2)
                botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
                botao_vazaoP.place(x=2, y=30)

                saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
                label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
                label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

                botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbp_COL = Button(canvas_graficos, width=11, text="Coliformes")

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
                botao_cbp_COL.place(x=805,y=55)

                botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)

                botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbp_COL["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)
            
            elif modo_execucao.get() == "101":
                canvas_graficos = Canvas(frame_saidas, height=280, width=944, bg='#94B7D5', highlightbackground="black")

                canvas_historico = Canvas(frame_saidas, height=70, width=944, bg='#94B7D5', highlightbackground="black")
                canvas_historico.place(x=0,y=180)

                label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
                label_vazao.place(x=2, y=2)
                botao_vazao = Button(canvas_historico, width=11, text="Difuso")
                botao_vazao.place(x=2, y=30)

                saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
                label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
                label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
                label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

                botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbd_COL = Button(canvas_graficos, width=11, text="Coliformes")

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
                botao_cbd_COL.place(x=805,y=55)

                botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

                botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbd_COL["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)
            
            elif modo_execucao.get() == "111":
                canvas_graficos = Canvas(frame_saidas, height=280, width=944, bg='#94B7D5', highlightbackground="black")

                canvas_historico = Canvas(frame_saidas, height=70, width=944, bg='#94B7D5', highlightbackground="black")
                canvas_historico.place(x=0,y=180)

                label_vazao = Label(canvas_historico, text="Gráfico da Vazão:", bg='#94B7D5', font=('Arial', '13'))
                label_vazao.place(x=2, y=2)
                botao_vazaoP = Button(canvas_historico, width=11, text="Pontual")
                botao_vazaoP.place(x=2, y=30)
                botao_vazao = Button(canvas_historico, width=11, text="Difuso")
                botao_vazao.place(x=102, y=30)

                saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
                label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
                label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
                label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

                botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbp_COL = Button(canvas_graficos, width=11, text="Coliformes")

                botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbd_COL = Button(canvas_graficos, width=11, text="Coliformes")

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
                botao_cbp_COL.place(x=805,y=55)
                botao_cbd_DBO.place(x=8, y=115)
                botao_cbd_OD.place(x=105, y=115)
                botao_cbd_NORG.place(x=205, y=115)
                botao_cbd_NAMON.place(x=305, y=115)
                botao_cbd_NNITR.place(x=405, y=115)
                botao_cbd_NNITRA.place(x=505, y=115)
                botao_cbd_PORG.place(x=605, y=115)
                botao_cbd_PINORG.place(x=705, y=115)
                botao_cbd_COL.place(x=805,y=115)
            
                botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)
                botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

                botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbp_COL["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

                botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbd_COL["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)
            

            elif modo_execucao.get() == "21":
                canvas_graficos = Canvas(frame_saidas, height=280, width=944, bg='#94B7D5', highlightbackground="black")

                canvas_historico = Canvas(frame_saidas, height=70, width=944, bg='#94B7D5', highlightbackground="black")
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

                saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
                label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
                label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_gop = Label(canvas_graficos, text="Cenário Otimizado Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

                botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbp_COL = Button(canvas_graficos, width=11, text="Coliformes")

                botao_cop_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cop_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cop_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cop_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cop_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cop_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cop_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cop_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cop_COL = Button(canvas_graficos, width=11, text="Coliformes")

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
                botao_cbp_COL.place(x=805,y=55)
                botao_cop_DBO.place(x=8, y=115)
                botao_cop_OD.place(x=105, y=115)
                botao_cop_NORG.place(x=205, y=115)
                botao_cop_NAMON.place(x=305, y=115)
                botao_cop_NNITR.place(x=405, y=115)
                botao_cop_NNITRA.place(x=505, y=115)
                botao_cop_PORG.place(x=605, y=115)
                botao_cop_PINORG.place(x=705, y=115)
                botao_cop_COL.place(x=805,y=115)

                botao_foP["command"] = partial(gera_grafico_fo, historico_foP[0], iteracao_versao_rapidaP)

                botao_tempoP["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoesP[0], iteracao_versao_rapidaP)

                botao_invalidosP["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidosP[0], iteracao_versao_rapidaP)

                botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP[0], tam_cel, tam_rio)

                botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbp_COL["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

                botao_cop_DBO["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cop_OD["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cop_NORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cop_NAMON["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cop_NNITR["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cop_NNITRA["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cop_PORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cop_PINORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cop_COL["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)
            
            elif modo_execucao.get() == "22":
                canvas_graficos = Canvas(frame_saidas, height=280, width=944, bg='#94B7D5', highlightbackground="black")

                canvas_historico = Canvas(frame_saidas, height=70, width=944, bg='#94B7D5', highlightbackground="black")
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

                saidas = Label(frame_saidas, text="Saidas:", bg='#94B7D5', font=('Arial', '14', 'bold'))
                label_graf = Label(canvas_graficos, text="Graficos:", bg='#94B7D5', font=('Arial', '13'))
                label_gbp = Label(canvas_graficos, text="Cenário Base Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_gop = Label(canvas_graficos, text="Cenário Otimizado Pontual:", bg='#94B7D5', font=('Arial', '11'))
                label_gbd = Label(canvas_graficos, text="Cenário Base Difuso:", bg='#94B7D5', font=('Arial', '11'))
                label_god = Label(canvas_graficos, text="Cenário Otimizado Difuso:", bg='#94B7D5', font=('Arial', '11'))
                label_caixa_textos = Label(canvas_saidas, text=" ", justify=LEFT, font=('Arial', '10'))

                botao_cbp_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbp_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbp_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbp_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbp_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbp_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbp_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbp_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbp_COL = Button(canvas_graficos, width=11, text="Coliformes")

                botao_cop_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cop_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cop_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cop_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cop_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cop_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cop_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cop_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cop_COL = Button(canvas_graficos, width=11, text="Coliformes")

                botao_cbd_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cbd_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cbd_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cbd_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cbd_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cbd_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cbd_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cbd_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cbd_COL = Button(canvas_graficos, width=11, text="Coliformes")

                botao_cod_DBO = Button(canvas_graficos, width=11, text="DBO")
                botao_cod_OD = Button(canvas_graficos, width=11, text="OD")
                botao_cod_NORG = Button(canvas_graficos, width=11, text="Norg")
                botao_cod_NAMON = Button(canvas_graficos, width=11, text="Namon")
                botao_cod_NNITR = Button(canvas_graficos, width=11, text="Nnitr")
                botao_cod_NNITRA = Button(canvas_graficos, width=11, text="Nnitra")
                botao_cod_PORG = Button(canvas_graficos, width=11, text="Porg")
                botao_cod_PINORG = Button(canvas_graficos, width=11, text="Pinorg")
                botao_cod_COL = Button(canvas_graficos, width=11, text="Coliformes")

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
                botao_cbp_COL.place(x=805,y=55)
                botao_cop_DBO.place(x=8, y=115)
                botao_cop_OD.place(x=105, y=115)
                botao_cop_NORG.place(x=205, y=115)
                botao_cop_NAMON.place(x=305, y=115)
                botao_cop_NNITR.place(x=405, y=115)
                botao_cop_NNITRA.place(x=505, y=115)
                botao_cop_PORG.place(x=605, y=115)
                botao_cop_PINORG.place(x=705, y=115)
                botao_cop_COL.place(x=805,y=115)
                botao_cbd_DBO.place(x=8, y=175)
                botao_cbd_OD.place(x=105, y=175)
                botao_cbd_NORG.place(x=205, y=175)
                botao_cbd_NAMON.place(x=305, y=175)
                botao_cbd_NNITR.place(x=405, y=175)
                botao_cbd_NNITRA.place(x=505, y=175)
                botao_cbd_PORG.place(x=605, y=175)
                botao_cbd_PINORG.place(x=705, y=175)
                botao_cbd_COL.place(x=805,y=175)
                botao_cod_DBO.place(x=8, y=235)
                botao_cod_OD.place(x=105, y=235)
                botao_cod_NORG.place(x=205, y=235)
                botao_cod_NAMON.place(x=305, y=235)
                botao_cod_NNITR.place(x=405, y=235)
                botao_cod_NNITRA.place(x=505, y=235)
                botao_cod_PORG.place(x=605, y=235)
                botao_cod_PINORG.place(x=705, y=235)
                botao_cod_COL.place(x=805,y=235)

                botao_foP["command"] = partial(gera_grafico_fo, historico_foP, iteracao_versao_rapidaP)
                botao_fo["command"] = partial(gera_grafico_fo, historico_fo, iteracao_versao_rapida)

                botao_tempoP["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoesP, iteracao_versao_rapidaP)
                botao_tempo["command"] = partial(gera_grafico_tempo_iteracoes, historico_tempo_iteracoes, iteracao_versao_rapida)

                botao_invalidosP["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidosP, iteracao_versao_rapidaP)
                botao_invalidos["command"] = partial(gera_grafico_filhos_invalidos, historico_filhos_invalidos, iteracao_versao_rapida)

                botao_vazaoP["command"] = partial(gera_grafico_vazao, perfilQP, tam_cel, tam_rio)
                botao_vazao["command"] = partial(gera_grafico_vazao, perfilQ, tam_cel, tam_rio)

                botao_cbp_DBO["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbp_OD["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbp_NORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbp_NAMON["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbp_NNITR["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbp_NNITRA["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbp_PORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbp_PINORG["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbp_COL["command"] = partial(gera_grafico, cenario_base_pontual[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

                botao_cop_DBO["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cop_OD["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cop_NORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cop_NAMON["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cop_NNITR["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cop_NNITRA["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cop_PORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cop_PINORG["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cop_COL["command"] = partial(gera_grafico, melhor_solucao_pontual[0].cenario.Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

                botao_cbd_DBO["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_DBO, 0, restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cbd_OD["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cbd_NORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cbd_NAMON["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cbd_NNITR["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cbd_NNITRA["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cbd_PORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cbd_PINORG["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cbd_COL["command"] = partial(gera_grafico, cenario_base_difusa[0].Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

                botao_cod_DBO["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_DBO, 0,restricao_DBO, tam_cel, tam_rio, classe)  # DBO
                botao_cod_OD["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_OD, 1, restricao_OD, tam_cel, tam_rio, classe)  # OD
                botao_cod_NORG["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Norg, 2, None, tam_cel, tam_rio, classe)  # NORG
                botao_cod_NAMON["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Namon, 3, restricao_NAMON, tam_cel, tam_rio, classe)  # NAMON
                botao_cod_NNITR["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Nnitri, 4, restricao_NNITR, tam_cel, tam_rio, classe)  # NNITRI
                botao_cod_NNITRA["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Nnitra, 5, restricao_NNITRA, tam_cel, tam_rio, classe)  # NNITRA
                botao_cod_PORG["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Porg, 6, restricao_PORG, tam_cel, tam_rio, classe)  # PORG
                botao_cod_PINORG["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Pinorg, 7, None, tam_cel, tam_rio, classe)  # PINORG
                botao_cod_COL["command"] = partial(gera_grafico, melhor_solucao_difusa[0].cenario.Y_Coliformes, 8, restricao_COL, tam_cel, tam_rio, classe)

Janela_inicial()