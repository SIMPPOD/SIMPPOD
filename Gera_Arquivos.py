from os import mkdir, path, remove
from shutil import rmtree
from platform import system

# METODO DE MANIPULACAO DE FLOAT
def converte_float(valor):
    if system() != 'Linux':
        if valor.find("."):
            return valor.replace(".",",")
    else: return valor

# METODOS DE CHECAGEM DE ARQUIVO E DIRETORIO
def checa_arquivo(arquivo):
    if path.isfile(arquivo):
        remove(arquivo)

def checa_diretorio(diretorio):
    if path.exists(diretorio):
        rmtree(diretorio)
        mkdir(diretorio)
    else:
        mkdir(diretorio)

# METODOS QUE CRIAM OS ARQUIVOS DE SAIDA     
def gera_saida_base_pontual(diretorio_saida, cenario_pontual, tam_rio, tam_cel, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)        
    Escreve_saida_QualUFMG(nome_arquivo, cenario_pontual, tam_rio, tam_cel)
    
def gera_saida_base_difusa(diretorio_saida, cenario_difusa, tam_rio, tam_cel, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Difusa.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_difusa, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Base.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_PD(nome_arquivo, cenario_difusa)

def gera_saida_base_pontual_difusa(diretorio_saida, cenario_pontual, cenario_difusa, tam_rio, tam_cel, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_pontual, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Difusa.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_difusa, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Base.csv"
    checa_arquivo(nome_arquivo)        
    Escreve_saida_PD(nome_arquivo, cenario_difusa)

def gera_saida_estimar_cargas(diretorio_saida, cenario_difusa, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Base.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_PD(nome_arquivo, cenario_difusa)

def gera_saida_otimizado_pontual(diretorio_saida, cenario_base_pontual, melhor_solucao_pontual, melhor_solucao_pontual_rapida, tam_rio, tam_cel, tempo_pontual, tempo_pontual_rapida, vetor_invalidos_pontual, vetor_invalidos_pontual_rapida, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Otimização-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_pontual, tempo_pontual, vetor_invalidos_pontual)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_base_pontual, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual Otimizada.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_pontual.cenario, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Otimização-Poluição Pontual-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_pontual_rapida, tempo_pontual_rapida, vetor_invalidos_pontual_rapida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual Otimizada-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_pontual_rapida.cenario, tam_rio, tam_cel) 

def gera_saida_otimizada_pontual_difusa(diretorio_saida, cenario_base_pontual, cenario_base_difusa, melhor_solucao_pontual, melhor_solucao_pontual_rapida, melhor_solucao_difusa, melhor_solucao_difusa_rapida, tam_rio, tam_cel, tempo_pontual, tempo_pontual_rapida, tempo_difusa, tempo_difusa_rapida, vetor_invalidos_pontual, vetor_invalidos_pontual_rapida, vetor_invalidos_difusa, vetor_invalidos_difusa_rapida, tributario):
    if tributario>=0:
        diretorio_saida += "/Tributario_" + str(tributario+1)
    else:
        diretorio_saida += "/RioPrincipal"
    checa_diretorio(diretorio_saida)

    nome_arquivo = diretorio_saida + "/Otimização-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_pontual, tempo_pontual, vetor_invalidos_pontual)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_base_pontual, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual Otimizada.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_pontual.cenario, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Otimização-Poluição Difusa.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_difusa, tempo_difusa, vetor_invalidos_difusa)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Difusa.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, cenario_base_difusa, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Difusa Otimizada.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_difusa.cenario, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Base.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_PD(nome_arquivo, cenario_base_difusa)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Otimizado.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_PD(nome_arquivo, melhor_solucao_difusa.cenario) 
    
    nome_arquivo = diretorio_saida + "/Otimização-Poluição Pontual-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_pontual_rapida, tempo_pontual_rapida, vetor_invalidos_pontual_rapida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Pontual Otimizada-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_pontual_rapida.cenario, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Otimização-Poluição Difusa-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_otimizacao(nome_arquivo, melhor_solucao_difusa_rapida, tempo_difusa_rapida, vetor_invalidos_difusa_rapida)

    nome_arquivo = diretorio_saida + "/Perfil de QA-Poluição Difusa Otimizada-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)
    Escreve_saida_QualUFMG(nome_arquivo, melhor_solucao_difusa_rapida.cenario, tam_rio, tam_cel)

    nome_arquivo = diretorio_saida + "/Poluição Difusa e CME Ponderada-Cenário Otimizado-Versão Rápida.csv"
    checa_arquivo(nome_arquivo)    
    Escreve_saida_PD(nome_arquivo, melhor_solucao_difusa_rapida.cenario)

# METODOS QUE ESCREVEM OS PERFIS DOS PARAMETROS NOS ARQUIVOS DE SAIDA
def Escreve_DBO(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("Concentração de DBO (mg/L): \n")

    for i in range(len(cenario.Y_DBO)):
        arq.write(converte_float(str(cenario.Y_DBO[i])))
        if i != (len(cenario.Y_DBO)-1):
            arq.write(";")
    arq.write("\n") 

def Escreve_OD(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("Concentração de OD (mg/L): \n")

    for i in range(len(cenario.Y_OD)):
        arq.write(converte_float(str(cenario.Y_OD[i]))) 
        if i != (len(cenario.Y_OD)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Norg(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("N-Orgânico (mg/L): \n")

    for i in range(len(cenario.Y_Norg)):
        arq.write(converte_float(str(cenario.Y_Norg[i]))) 
        if i != (len(cenario.Y_Norg)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Namon(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("N-Amônia Total (mg/L): \n")

    for i in range(len(cenario.Y_Namon)):
        arq.write(converte_float(str(cenario.Y_Namon[i]))) 
        if i != (len(cenario.Y_Namon)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Nnitri(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("N-Nitrito (mg/L): \n")

    for i in range(len(cenario.Y_Nnitri)):
        arq.write(converte_float(str(cenario.Y_Nnitri[i]))) 
        if i != (len(cenario.Y_Nnitri)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Nnitra(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("N-Nitrato (mg/L): \n")

    for i in range(len(cenario.Y_Nnitra)):
        arq.write(converte_float(str(cenario.Y_Nnitra[i]))) 
        if i != (len(cenario.Y_Nnitra)-1):
            arq.write(";") 
    arq.write("\n") 

def Escreve_Amonia_Livre(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("Amônia Livre (mg/L): \n")

    for i in range(len(cenario.Amonia[0])-1):
        arq.write(converte_float(str(cenario.Amonia[0][i])))
        if i != (len(cenario.Amonia[0])-1): 
            arq.write(";") 
    arq.write("\n") 

def Escreve_Amonia_Ionizada(arquivo, cenario):
    arq = open(arquivo, "a+")
    arq.write("N-Amônia Ionizada (mg/L): \n")

    for i in range(len(cenario.Amonia[1])-1): 
        arq.write(converte_float(str(cenario.Amonia[1][i])))
        if i != (len(cenario.Amonia[1])-1): 
            arq.write(";") 
    arq.write("\n")

def Escreve_Porg(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Fósforo Orgânico (mg/L): \n")

    for i in range(len(cenario.Y_Porg)):
        arq.write(converte_float(str(cenario.Y_Porg[i]))) 
        if i != (len(cenario.Y_Porg)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Pinorg(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Fósforo Inorgânico (mg/L): \n")

    for i in range(len(cenario.Y_Pinorg)):
        arq.write(converte_float(str(cenario.Y_Pinorg[i]))) 
        if i != (len(cenario.Y_Pinorg)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_K2(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Perfil de K2: \n")
    
    for i in range(len(cenario.PerfilK2)-1): 
        arq.write(converte_float(str(cenario.PerfilK2[i]))) 
        if i != (len(cenario.PerfilK2)-1):
            arq.write(";")  
    arq.write("\n") 

def Escreve_Kd(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Perfil de Kd: \n")

    for i in range(len(cenario.PerfilKd)-1):
        arq.write(converte_float(str(cenario.PerfilKd[i]))) 
        if i != (len(cenario.PerfilKd)-1): 
            arq.write(";") 
    arq.write("\n") 

def Escreve_Q(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Perfil de Vazão (m3/s): \n")

    for i in range(len(cenario.PerfilQ)): 
        arq.write(converte_float(str(cenario.PerfilQ[i])))
        if i != (len(cenario.PerfilQ)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_V(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Perfil de Velocidade (m/s): \n")

    for i in range(len(cenario.PerfilV)-1): 
        arq.write(converte_float(str(cenario.PerfilV[i])))
        if i != (len(cenario.PerfilV)-1): 
            arq.write(";")
    arq.write("\n") 

def Escreve_H(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Perfil de Profundidade (m): \n")

    for i in range(len(cenario.PerfilH)-1):
        arq.write(converte_float(str(cenario.PerfilH[i]))) 
        if i != (len(cenario.PerfilH)-1):
            arq.write(";") 
    arq.write("\n")

def Escreve_Extensao(arquivo, tam_rio, tam_cel):
    arq = open(arquivo, "a+") 
    arq.write("Extensão (km): \n")

    passo = 0 
    while passo*1000 <= int(tam_rio):
        arq.write(converte_float(str(passo)) + ";")
        passo = round(passo, 2) + tam_cel/1000
    arq.write("\n") 

def Escreve_Tempo(arquivo, cenario):
    arq = open(arquivo, "a+") 
    arq.write("Tempo (s): \n")

    for i in range(len(cenario.PerfilTempo)-1): 
        arq.write(converte_float(str(cenario.PerfilTempo[i])))  
        if i != (len(cenario.PerfilTempo)-1): 
            arq.write(";") 
    arq.write("\n") 

# METODO QUE ESCREVE O ARQUIVO DE SAIDA QUAL_UFMG
def Escreve_saida_QualUFMG(arquivo, cenario, tam_rio, tam_cel):
    Escreve_Extensao(arquivo, tam_rio, tam_cel) 
    Escreve_DBO(arquivo, cenario)
    Escreve_OD(arquivo, cenario)
    Escreve_Norg(arquivo, cenario) 
    Escreve_Namon(arquivo, cenario) 
    Escreve_Nnitri(arquivo, cenario)
    Escreve_Nnitra(arquivo, cenario) 
    Escreve_Amonia_Livre(arquivo, cenario) 
    Escreve_Amonia_Ionizada(arquivo, cenario) 
    Escreve_Porg(arquivo, cenario)
    Escreve_Pinorg(arquivo, cenario) 
    Escreve_K2(arquivo, cenario)
    Escreve_Kd(arquivo, cenario)  
    Escreve_Q(arquivo, cenario) 
    Escreve_V(arquivo, cenario)
    Escreve_H(arquivo, cenario) 
    Escreve_Tempo(arquivo, cenario)
    
# METODO QUE ESCREVE O ARQUIVO DE SAIDA PD
def Escreve_saida_PD(arquivo, cenario):
    arq = open(arquivo, "w")

    # Escrita das cargas
    arq.write("ID;Carga de DBO (Kg/dia);Carga de N-Amônia (Kg/dia);Carga de Nitrito (Kg/dia);Carga de P-inorgânico (Kg/dia);\n")        
    for i in range(len(cenario.matriz_cargas)):
        arq.write(converte_float(str(cenario.sub_bacias[i].ID)) + ";")
        for j in range(len(cenario.matriz_cargas[i])): 
            cenario.matriz_cargas[i][j] = str(cenario.matriz_cargas[i][j]) 
            arq.write(converte_float(cenario.matriz_cargas[i][j] + ";"))  
        arq.write("\n") 
    arq.write("\n")

    # Escrita das constantes
    arq.write("ID;CME DBO (mg/L);CS de OD (mg/L);CME N-Amônia (mg/L);CME Nitrito (mg/L);CME P-inorgânico (mg/L);Q acumulada (m3/s);Q distribuida (m3/s);TC (horas);\n")
    for i in range(len(cenario.sub_bacias)):
        cenario.sub_bacias[i].ID = str(cenario.sub_bacias[i].ID)
        cenario.sub_bacias[i].CME_DBO = str(cenario.sub_bacias[i].CME_DBO)
        cenario.sub_bacias[i].ODsat = str(cenario.sub_bacias[i].ODsat)
        cenario.sub_bacias[i].CME_NTK = str(cenario.sub_bacias[i].CME_NTK)
        cenario.sub_bacias[i].CME_NOX = str(cenario.sub_bacias[i].CME_NOX)
        cenario.sub_bacias[i].CME_PINORG = str(cenario.sub_bacias[i].CME_PINORG)
        cenario.sub_bacias[i].Q_acumulada = str(cenario.sub_bacias[i].Q_acumulada)
        cenario.sub_bacias[i].Q_distribuida = str(cenario.sub_bacias[i].Q_distribuida)
        cenario.sub_bacias[i].Tc = str(cenario.sub_bacias[i].Tc)
        
        arq.write(converte_float(cenario.sub_bacias[i].ID) + ";" + 
                    converte_float(cenario.sub_bacias[i].CME_DBO) + ";" + 
                    converte_float(cenario.sub_bacias[i].ODsat) + ";" + 
                    converte_float(cenario.sub_bacias[i].CME_NTK) + ";" + 
                    converte_float(cenario.sub_bacias[i].CME_NOX) + ";" + 
                    converte_float(cenario.sub_bacias[i].CME_PINORG) + ";" + 
                    converte_float(cenario.sub_bacias[i].Q_acumulada) + ";" + 
                    converte_float(cenario.sub_bacias[i].Q_distribuida) + ";" + 
                    converte_float(cenario.sub_bacias[i].Tc) + ";\n")


# METODO QUE ESCREVE O ARQUIVO DE SAIDA DA OTIMIZACAO
def Escreve_saida_otimizacao(arquivo, solucao_otimizada, tempo, vetor_invalidos):
    arq = open(arquivo, "a+")
    arq.write("Resultados da Otimização de Poluição Pontual: Identificação dos valores mínimos de redução necessários ao atendimento da classe de QA desejada \n")
    arq.write("Tempo de processamento (s):; " + converte_float(str(tempo)) + "\n")
    arq.write("Número de inválidos gerados:; " + str(vetor_invalidos) + "\n")

    if solucao_otimizada.simula_difusa:
        arq.write("Eficiência de Tratamento/Redução:  \n\n")
        arq.write("ID subbacia; DBO; Amonia; Nitrito; P-inorg\n")
        for i in range(len(solucao_otimizada.alelos)): 
            arq.write(str(solucao_otimizada.cenario.sub_bacias[i].ID) + ";")
            for j in range(len(solucao_otimizada.alelos[i])): 
                arq.write(str(solucao_otimizada.alelos[i][j]) + ";") 
            arq.write("\n")
    else:
        for i in range(len(solucao_otimizada.alelos)): 
            arq.write("Eficiência de Tratamento/Redução:;" + converte_float(str(solucao_otimizada.alelos[i])) + "\n")

    arq.write("Nota da F.O. para a melhor solucao:; " + converte_float(str(solucao_otimizada.func_objetivo)) + "\n\n")
    arq.write("OBS: As eficiencias de tratamento/redução se encontram expressas em decimal.\n")
    arq.close()