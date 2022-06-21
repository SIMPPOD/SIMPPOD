# -*- coding: utf-8 -*-
# Modulo: Fosforo

# Importacao de bibliotecas
import numpy as np

# Definicao da classe
class Fosforo (object):  
    
    # METODOS

    # Metodo que constroi a matriz
    @staticmethod
    def constroi_matriz(Koi, Kspo):
        mat_ini = np.array([[(-Koi-Kspo), 0], [Koi, 0]])
        return mat_ini

    # Metodo que constroi o vetor auxiliar
    @staticmethod
    def constroi_vetor_auxiliar(Sinorg, H):
        vet_aux = np.array([[0], [(Sinorg/H)]])
        return vet_aux
