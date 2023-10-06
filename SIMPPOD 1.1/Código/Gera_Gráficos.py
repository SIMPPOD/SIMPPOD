from tkinter import Tk, TOP, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

# METODO QUE CRIA A RESTRIÇÃO
def cria_vetor_restricao(indice, tam_rio, tam_cel, ph, classe):
    vetor_restricao = []
    for i in range(int(tam_rio/tam_cel)+1):
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
            elif indice == 8:
                vetor_restricao.append(200)
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
            elif indice == 8:
                vetor_restricao.append(1000)
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
            elif indice == 8:
                vetor_restricao.append(2500)
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

# METODO QUE GERA OS GRÁFICOS DE SAÍDA
def gera_grafico(serie_dados, indice, restricao, tam_cel, tam_rio, classe):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Concentração(mg/L) do Parâmetro ao Longo do Curso D'água (células)")

    # Plot do grafico
    fig = Figure(figsize=(6, 4), dpi=100)

    num_cel = tam_rio / tam_cel
    x = []
    for i in range(int(num_cel)+1):
        x.append(int(i*tam_rio/num_cel))

    
    if indice == 8: ax = fig.add_subplot(111, xlabel="Extensão [m]", ylabel="Concentração [mg/mL]")
    else: ax = fig.add_subplot(111, xlabel="Extensão [m]", ylabel="Concentração [mg/L]")

    ax.plot(x, serie_dados, 'b')

    if indice != 2 and indice != 7:
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
    elif indice == 7:
        fig.suptitle("Fósforo Inorgânico")
        ax.legend(['PINORG'])
    else:
        fig.suptitle("Coliformes")
        ax.legend(['Coliformes', 'Limite da Classe ' + str(classe)])

    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# METODO QUE GERA O GRÁFICO DO PERFIL DA VAZÃO
def gera_grafico_vazao(serie_dados, tam_cel, tam_rio):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Vazão ao Longo do Curso D'água (células)")

    # Plot do grafico
    fig = Figure(figsize=(6, 4), dpi=100)

    num_cel = tam_rio / tam_cel
    x = []
    for i in range(int(num_cel)+1):
        x.append(int(i*tam_rio/num_cel))

    ax = fig.add_subplot(111, xlabel="Extensão [m]", ylabel="Vazão [m^3/s]")
    fig.suptitle("Comportamento da Vazão")
    ax.plot(x, serie_dados, 'b')

    menor = min(serie_dados)
    maior = max(serie_dados)
    media = sum(serie_dados)/len(serie_dados)

    fig.text(0.01, 1, 'Mínimo = ' + str(round(menor,4)) +
                        ' | Máximo = ' + str(round(maior,4)) +
                        ' | Média = ' + str(round(media,4)),
            horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes)
    
    # Criacao da caixa de ferramentas
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, janela)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    janela.mainloop()

# METODO QUE GERA O GRÁFICO DO PERFIL DA FO
def gera_grafico_fo(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Função Objetivo ao Longo das Iterações")

    fig = Figure(figsize=(6, 4), dpi=100)
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

# METODO QUE GERA O GRÁFICO DO TEMPO DE CADA ITERAÇÃO DE OTIMIZAÇÃO
def gera_grafico_tempo_iteracoes(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento do Tempo de Duração das Iterações")

    fig = Figure(figsize=(6, 4), dpi=100)
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

# METODO QUE GERA O GRÁFICO DOS FILHOS INVÁLIDOS GERADOS EM CADA ITERAÇÃO DE OTIMIZAÇÃO
def gera_grafico_filhos_invalidos(serie_dados, iteracao_versao_rapida):
    # Criacao da janela
    janela = Tk()
    janela.wm_title("Comportamento da Geração de Filhos Inválidos ao Longo das Iterações")

    fig = Figure(figsize=(6, 4), dpi=100)
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