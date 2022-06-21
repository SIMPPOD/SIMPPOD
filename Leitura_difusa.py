# -*- coding: utf-8 -*-
# Metodo: Leitura_difusa

# Definicao da classe
class Leitura_difusa(object):

    # METODOS

    @staticmethod        
    def ler(Caminho):
        leitor = open(Caminho) 
        leitor.readline() 
        matriz = []
        
        for x in leitor: 
            cn = x.split(' ')
            for i in range(len(cn)): 
                cn[i] = float(cn[i]) 
            matriz.append(cn)
        
        return matriz

    @staticmethod
    def ler_hidro(Caminho):
        leitor = open(Caminho)  
        leitor.readline()
        matriz = []
        
        tam_celula = float(leitor.readline().split(' ')[0])
        fator = float(leitor.readline().split(' ')[0])

        for x in leitor:   
            cn = x.split(' ') 
            for i in range(len(cn)): 
                cn[i] = float(cn[i]) 
            matriz.append(cn)
        
        return [matriz,tam_celula,fator]
    
    # Metodo que le o arquivo de CME
    @staticmethod
    def ler_cme(Caminho):
        leitor = open(Caminho) 
        leitor.readline()  
        matriz = []
        
        for x in leitor:  
            uso = x.split(' ')  
            for i in range(len(uso)):  
                if i != 1:
                    uso[i] = float(uso[i])  
            matriz.append(uso)

        return matriz