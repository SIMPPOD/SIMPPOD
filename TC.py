# -*- coding: utf-8 -*-
# Modulo: TC

# Definicao da classe
class TC (object):
    # METODOS

    @staticmethod
    def calcula_Tc(L, s, A, C):
        if A < 50:
            s = s*1000  # passa de m/m para m/km
            if C == 1:
                Tc = 0.00167 * ((L / (s ** 0.5)) ** 0.7)
            else:
                Tc = 0.00024 * ((L / (s ** 0.5)) ** 0.7)
        elif 140 < A < 930:
            s = s*1000
            Tc = 21.88 * (A ** 0.41) * s ** (-0.17)
            Tc = Tc/60
        else:
            L = L/1000  # passa pra km
            Tc = 20.17 * ((L / (s ** 0.5)) ** 0.5)
            Tc = Tc/60        
        return Tc
