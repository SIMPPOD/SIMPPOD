# -*- coding: utf-8 -*-
# Modulo: DBO

# Importacao de bibliotecas
import numpy as np

# Definicao da classe
class DBO (object):
    
    # METODOS

    # Metodo que constroi a matriz
    @staticmethod
    def constroi_matriz(Kd, Ks, K2, Kt):
        mat_ini = np.array([[-Kd - Ks, 0, 0], [Kd, K2, 0], [-Kd*Kt, 0, -K2]])
        return mat_ini

    # Metodo que constroi o vetor auxiliar --> acrescentar Sd
    @staticmethod
    def constroi_vetor_auxiliar(K2, Cs, Ro2a, Ro2n, Kan, fnitr, Namon, Nnitri, Knn):
        a = Sd/H + (K2 * Cs)  # Reintroducao de OD por K2
        b = (Ro2a * fnitr * Namon * Kan) + (Ro2n * fnitr * Nnitri * Knn)  # Consumo de OD por nitrogenio
        c = a - b
        d = -a + b
        vet = np.array([[0], [d], [c]])
        return vet       
