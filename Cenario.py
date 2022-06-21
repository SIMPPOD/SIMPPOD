# -*- coding: utf-8 -*-
# Modulo: Cenario

def converte_float(valor):
    if valor.find("."):
        return valor.replace(".",",")

# Definicao da classe
class Cenario:

    # CONSTRUTOR
    def __init__(self, Y_DBO, Y_Nitr, Y_Fosf, Amonia, PerfilK2, PerfilKd, PerfilQ, PerfilV, PerfilH, PerfilCs, PerfilTempo, matriz_contribuicoes):
        # Valores calculados em Euler
        self.Y_DBO = Y_DBO  # Matriz [DBO, deficit de OD, OD]
        self.Y_Nitr = Y_Nitr  # Matriz [NORG, NAMON, NNITRI, NNITRA]
        self.Y_Fosf = Y_Fosf  # Matriz [PORG, PINORG]
        self.Amonia = Amonia  # Matriz [Amonia livre, Amonia ionizada]
        self.PerfilK2 = PerfilK2  # Vetor [K2]
        self.PerfilKd = PerfilKd  # Vetor [Kd]
        self.PerfilQ = PerfilQ  # Vetor [Q]
        self.PerfilV = PerfilV  # Vetor [V]
        self.PerfilH = PerfilH  # Vetor [H]
        self.PerfilCs = PerfilCs  # Vetor [Cs]
        self.matriz_contribuicoes = matriz_contribuicoes
        self.sub_bacias = []  # Matriz [DBO,Cs,NTK,NOx,Pinorg,Qacumulada,Qdistribuida,TC,Jusante,Visitada,ID]
        self.matriz_cargas = []  # Matriz [Carga DBO, Carga NTK, Carga NOx, Carga Pinorg]
        self.PerfilTempo = PerfilTempo

    # METODOS
    
    # Metodo que escreve a matriz Y_DBO
    def Escreve_DBO(self, caminho):
        arq = open(caminho, "a+")
        
        # Escrita do DBO
        arq.write("Concentração de DBO (mg/L): \n")
        for i in range(len(self.Y_DBO[0])):
            arq.write(converte_float(str(self.Y_DBO[0][i])))
            if i != (len(self.Y_DBO[0])-1):
                arq.write(";")
        
        # Escrita do deficit de OD
        arq.write("\nDéficit de OD (mg/L): \n")
        for i in range(len(self.Y_DBO[1])): 
            arq.write(converte_float(str(self.Y_DBO[1][i])))
            if i != (len(self.Y_DBO[1])-1):
                arq.write(";")
        
        # Escrita do OD
        arq.write("\nConcentração de OD (mg/L): \n")
        for i in range(len(self.Y_DBO[2])):
            arq.write(converte_float(str(self.Y_DBO[2][i]))) 
            if i != (len(self.Y_DBO[2])-1):
                arq.write(";") 
        arq.write("\n") 
    
    # Metodo que escreve a matriz Y_Nitr
    def Escreve_Nitr(self, caminho):
        arq = open(caminho, "a+")

        # Escrita do nitrogenio organico
        arq.write("N-Orgânico (mg/L): \n")
        for i in range(len(self.Y_Nitr[0])):
            arq.write(converte_float(str(self.Y_Nitr[0][i])))
            if i != (len(self.Y_Nitr[0])-1):
                arq.write(";")
        
        # Escrita da amonia total
        arq.write("\nN-Amônia Total (mg/L): \n")
        for i in range(len(self.Y_Nitr[1])): 
            arq.write(converte_float(str(self.Y_Nitr[1][i]))) 
            if i != (len(self.Y_Nitr[1])-1):  
                arq.write(";") 

        # Escrita do nitrito
        arq.write("\nN-Nitrito (mg/L): \n")
        for i in range(len(self.Y_Nitr[2])):
            arq.write(converte_float(str(self.Y_Nitr[2][i]))) 
            if i != (len(self.Y_Nitr[2])-1):
                arq.write(";")
        
        # Escrita do nitrato
        arq.write("\nN-Nitrato (mg/L): \n")
        for i in range(len(self.Y_Nitr[3])):
            arq.write(converte_float(str(self.Y_Nitr[3][i])))
            if i != (len(self.Y_Nitr[3])-1): 
                arq.write(";") 
        arq.write("\n") 
    
    # Metodo que escreve a matriz Amonia
    def Escreve_Amonia(self, caminho):
        arq = open(caminho, "a+")

        # Escrita da amonia livre
        arq.write("Amônia Livre (mg/L): \n")
        for i in range(len(self.Amonia[0])):
            arq.write(converte_float(str(self.Amonia[0][i])))
            if i != (len(self.Amonia[0])-1): 
                arq.write(";") 
        arq.write("\n") 

        # Escrita da amonia ionizada
        arq.write("N-Amônia Ionizada (mg/L): \n")
        for i in range(len(self.Amonia[1])): 
            arq.write(converte_float(str(self.Amonia[1][i])))
            if i != (len(self.Amonia[1])-1): 
                arq.write(";") 
        arq.write("\n")

    # Metodo que escreve a matriz Y_Fosf
    def Escreve_Fosf(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita do fosforo organico
        arq.write("Fósforo Orgânico (mg/L): \n")
        for i in range(len(self.Y_Fosf[0])):
            arq.write(converte_float(str(self.Y_Fosf[0][i]))) 
            if i != (len(self.Y_Fosf[0])-1):
                arq.write(";") 

        # Escrita do fosforo inorganico
        arq.write("\nFósforo Inorgânico (mg/L): \n")
        for i in range(len(self.Y_Fosf[1])):
            arq.write(converte_float(str(self.Y_Fosf[1][i]))) 
            if i != (len(self.Y_Fosf[1])-1):
                arq.write(";") 
        arq.write("\n")
    
    # Metodo que escreve o PerfilK2
    def Escreve_K2(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita do K2
        arq.write("Perfil de K2: \n")
        for i in range(len(self.PerfilK2)): 
            arq.write(converte_float(str(self.PerfilK2[i]))) 
            if i != (len(self.PerfilK2)-1):
                arq.write(";")  
        arq.write("\n") 
    
    # Metodo que escreve o PerfilKd
    def Escreve_Kd(self, caminho):
        arq = open(caminho, "a+") 

        # Escita do Kd
        arq.write("Perfil de Kd: \n")
        for i in range(len(self.PerfilKd)):
            arq.write(converte_float(str(self.PerfilKd[i]))) 
            if i != (len(self.PerfilKd)-1): 
                arq.write(";") 
        arq.write("\n") 
    
    # Metodo que escreve o PerfilQ
    def Escreve_Q(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita da vazao
        arq.write("Perfil de Vazão (m3/s): \n")
        for i in range(len(self.PerfilQ)): 
            arq.write(converte_float(str(self.PerfilQ[i])))
            if i != (len(self.PerfilQ)-1):
                arq.write(";") 
        arq.write("\n")
    
    # Metodo que escreve o PerfilV
    def Escreve_V(self, caminho):
        arq = open(caminho, "a+") 
        
        # Escrita da velocidade
        arq.write("Perfil de Velocidade (m/s): \n")
        for i in range(len(self.PerfilV)): 
            arq.write(converte_float(str(self.PerfilV[i])))
            if i != (len(self.PerfilV)-1): 
                arq.write(";")
        arq.write("\n") 
    
    # Metodo que escreve o PerfilH
    def Escreve_H(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita da profundidade
        arq.write("Perfil de Profundidade (m): \n")
        for i in range(len(self.PerfilH)):
            arq.write(converte_float(str(self.PerfilH[i]))) 
            if i != (len(self.PerfilH)-1):
                arq.write(";") 
        arq.write("\n")

    # Metodo que escreve o PerfilCs 
    def Escreve_Cs(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita da concentracao de saturacao
        arq.write("Concentração de Saturação de OD (mg/L): \n")
        for i in range(len(self.PerfilCs)): 
            arq.write(converte_float(str(self.PerfilCs[i]))) 
            if i != (len(self.PerfilCs)-1):
                arq.write(";")  
        arq.write("\n") 
    
    def Escreve_Extensao(self, caminho, tam_rio, tam_cel):
        arq = open(caminho, "a+") 

        # Escrita da extensão
        arq.write("Extensão (km): \n")
        passo = 0 
        for i in range(int(tam_rio)): 
            arq.write(converte_float(str(passo)) + ";")
            passo += tam_cel/1000 
        arq.write("\n") 
    
    def Escreve_Tempo(self, caminho):
        arq = open(caminho, "a+") 

        # Escrita do tempo
        arq.write("Tempo (s): \n")
        for i in range(len(self.PerfilTempo)): 
            arq.write(converte_float(str(self.PerfilTempo[i])))  
            if i != (len(self.PerfilTempo)-1): 
                arq.write(";") 
        arq.write("\n") 
  
    # Metodo que escreve o QUAL_UFMG
    def Escreve_saida_QualUFMG(self, caminho, tam_rio, tam_cel):
        # Escrita das constantes para o QUAL_UFMG
        self.Escreve_Extensao(caminho, tam_rio, tam_cel) 
        self.Escreve_DBO(caminho)  
        self.Escreve_Nitr(caminho) 
        self.Escreve_Amonia(caminho) 
        self.Escreve_Fosf(caminho) 
        self.Escreve_K2(caminho)
        self.Escreve_Kd(caminho)  
        self.Escreve_Q(caminho) 
        self.Escreve_V(caminho)
        self.Escreve_H(caminho) 
        self.Escreve_Cs(caminho) 
        self.Escreve_Tempo(caminho)
        
    # Metodo que escreve o PD
    def Escreve_saida_PD(self, caminho):
        arq = open(caminho, "w")

        # Escrita das cargas
        arq.write("ID;Carga de DBO (Kg/dia);Carga de N-Amônia (Kg/dia);Carga de Nitrito (Kg/dia);Carga de P-inorgânico (Kg/dia);\n")
        
        for i in range(len(self.matriz_cargas)):
            arq.write(converte_float(str(self.sub_bacias[i].ID)) + ";")
            for j in range(len(self.matriz_cargas[i])): 
                self.matriz_cargas[i][j] = str(self.matriz_cargas[i][j]) 
                arq.write(converte_float(self.matriz_cargas[i][j] + ";"))  
            arq.write("\n") 
        arq.write("\n")

        # Escrita das constantes
        arq.write("ID;CME DBO (mg/L);CS de OD (mg/L);CME N-Amônia (mg/L);CME Nitrito (mg/L);CME P-inorgânico (mg/L);Q acumulada (m3/s);Q distribuida (m3/s);TC (horas);\n")
        
        for i in range(len(self.sub_bacias)):
            self.sub_bacias[i].ID = str(self.sub_bacias[i].ID)
            self.sub_bacias[i].CME_DBO = str(self.sub_bacias[i].CME_DBO)
            self.sub_bacias[i].Cs = str(self.sub_bacias[i].Cs)
            self.sub_bacias[i].CME_NTK = str(self.sub_bacias[i].CME_NTK)
            self.sub_bacias[i].CME_NOX = str(self.sub_bacias[i].CME_NOX)
            self.sub_bacias[i].CME_PINORG = str(self.sub_bacias[i].CME_PINORG)
            self.sub_bacias[i].Q_acumulada = str(self.sub_bacias[i].Q_acumulada)
            self.sub_bacias[i].Q_distribuida = str(self.sub_bacias[i].Q_distribuida)
            self.sub_bacias[i].Tc = str(self.sub_bacias[i].Tc)
            
            # Escrita das constantes
            arq.write(converte_float(self.sub_bacias[i].ID) + ";" + 
                      converte_float(self.sub_bacias[i].CME_DBO) + ";" + 
                      converte_float(self.sub_bacias[i].Cs) + ";" + 
                      converte_float(self.sub_bacias[i].CME_NTK) + ";" + 
                      converte_float(self.sub_bacias[i].CME_NOX) + ";" + 
                      converte_float(self.sub_bacias[i].CME_PINORG) + ";" + 
                      converte_float(self.sub_bacias[i].Q_acumulada) + ";" + 
                      converte_float(self.sub_bacias[i].Q_distribuida) + ";" + 
                      converte_float(self.sub_bacias[i].Tc) + ";\n")
