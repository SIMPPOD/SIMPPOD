# -*- coding: utf-8 -*-
# Modulo: Nitrogenio

# Importacao das bibliotecas
import numpy as np

# Definicao da classe
class Nitrogenio (object): 
    
    # METODOS

    # Metodo que constroi a matriz
    @staticmethod
    def constroi_matriz(Koa, Kan, Kso, Knn, fnitr):
        mat_ini = np.array([[-Koa-Kso, 0, 0, 0], [Koa, -(fnitr*Kan), 0, 0], [0, fnitr*Kan, -Knn, 0], [0, 0, fnitr*Knn, 0]])
        return mat_ini

    # Metodo que constroi o vetor auxiliar
    @staticmethod
    def constroi_vetor_auxiliar(Samon, H):
        vet = np.array([[0], [Samon/H], [0], [0]])
        return vet
