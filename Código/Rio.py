# -*- coding: utf-8 -*-
# Modulo: Rio

class Rio(object):

    def __init__(self, tam_rio, tam_cel, classe, T, Alt, PH, DBOr, ODr, NORGr, NAMONr, NNITRIr, NNITRAr, PORGr, PINORGr, COLr,
                 Qr, Ro2a, Ks, K1, Kb, Koa, Kan, Koi, Kspo, Samon, Kso, Knn, Ro2n, Knitr, Sinorg, a_vel, b_vel, a_prof,
                 b_prof, DBOinc, ODinc, NORGinc, NAMONinc, NNITRIinc, NNITRAinc, PORGinc, PINORGinc, COLinc, Qinc, Sd, Lrd, kmt):

        self.DBO5r = DBOr  # Concentracao de DBO no rio
        self.ODr = ODr  # Concentracao de OD no rio
        self.NORGr = NORGr  # Concentracao de nitrogenio organico no rio
        self.NAMONr = NAMONr  # Concentracao de amonia no rio
        self.NNITRIr = NNITRIr  # Concentracao de nitrito no rio
        self.NNITRAr = NNITRAr  # Concentracao de nitrato no rio
        self.PORGr = PORGr  # Concentracao de fosforo organico no rio
        self.PINORGr = PINORGr  # Concentracao de fosforo inorganico no rio
        self.COLr = 10 * COLr  # passa de mL para L
        self.Qr = Qr  # Vazao do rio
        self.Qinc = Qinc * tam_cel  # Vazao incremental
        self.tam_rio = tam_rio  # Tamanho do rio, em metros
        self.tam_cel = tam_cel  # Tamanho da celula
        self.T = T  # Temperatura
        self.Alt = Alt  # Altitude
        self.Ro2a = Ro2a  # Relacao entre o consumo de oxigenio e a oxidacao da amonia
        self.Ks = Ks  # Coeficiente de sedimentacao
        self.K1 = K1  # Coeficiente de desoxigenacao
        self.Kt = 0  # Coeficiente de conversao da DBO5 a DBOu
        self.Koa = Koa  # Coeficiente de conversao de nitrogenio organico a amonia
        self.Kan = Kan  # Coeficiente de conversao de amonia a nitrito
        self.Koi = Koi  # Coeficiente de conversao de fosforo organico a fosforo inorganico
        self.Kspo = Kspo  # Coeficiente de remocao do fosforo organico por sedimentacao
        self.Kso = Kso  # Coeficiente de sedimentacao do nitrogenio organico
        self.Knn = Knn  # Coeficiente de conversao de nitrito a nitrato
        self.Knitr = Knitr  # Coeficiente de inibicao da nitrificacao por baixo OD
        self.Sinorg = Sinorg  # Coeficiente de liberacao de fosforo inorganico pelo sedimento de fundo
        self.a_vel = a_vel  # Constante de atualizacao da velocidade
        self.b_vel = b_vel  # Constante de atualizacao da velocidade
        self.a_prof = a_prof  # Constante de atualizacao da profundidade
        self.b_prof = b_prof  # Constante de atualizacao da profundidade 
        self.PH = PH  # Ph
        self.Samon = Samon  # Fluxo de liberacao de amonia pelo sedimento de fundo
        self.Ro2n = Ro2n  # Relacao entre o oxigenio consumido por cada unidade de nitrito oxidado a nitrato
        self.classe = classe  # Classe do rio
        self.DBOinc = DBOinc * tam_cel  # DBO incremental
        self.ODinc = ODinc * tam_cel  # OD incremental
        self.NORGinc = NORGinc * tam_cel
        self.NAMONinc = NAMONinc * tam_cel
        self.NNITRinc = NNITRIinc * tam_cel
        self.NNITRAinc = NNITRAinc * tam_cel
        self.PORGinc = PORGinc * tam_cel
        self.PINORGinc = PINORGinc * tam_cel
        self.COLinc = 10 * COLinc * tam_cel # passa de mL para L
        self.Sd = Sd
        self.Lrd = Lrd
        self.Nt = kmt * 1000 / tam_cel
        self.Kb = Kb

    def eq_mistura_DBO(self, DBOur, DBO5e, Qr, Qe):
        return ((Qr * DBOur) + (Qe * DBO5e) + (self.DBOinc * self.Qinc)) / (Qr + Qe + self.Qinc)
    
    def eq_mistura_OD(self, ODr, ODe, Qr, Qe):
        return ((Qr * ODr) + (Qe * ODe) + (self.ODinc * self.Qinc)) / (Qr + Qe + self.Qinc)
    
    def eq_mistura_Norg(self, NORGr, NORGe, Qr, Qe):
        return ((NORGr * Qr) + (NORGe * Qe) +(self.NORGinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Namon(self, NAMONr, NAMONe, Qr, Qe):
        return ((NAMONr * Qr) + (NAMONe * Qe) + (self.NAMONinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Nnitri(self, NNITRIr, NNITRIe, Qr, Qe):
        return ((NNITRIr * Qr) + (NNITRIe * Qe) + (self.NNITRinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Nnitra(self, NNITRAr, NNITRAe, Qr, Qe):
        return ((NNITRAr * Qr) + (NNITRAe * Qe) + (self.NNITRAinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Porg(self, PORGr, PORGe, Qr, Qe):
        return ((PORGr * Qr) + (PORGe * Qe) + (self.PORGinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Pinorg(self, PINORGr, PINORGe, Qr, Qe):
        return ((Qr * PINORGr) + (Qe * PINORGe) + (self.PINORGinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def eq_mistura_Coliformes(self, COLr, COLe, Qr, Qe):
        return ((Qr * COLr) + (Qe * COLe) + (self.COLinc * self.Qinc)) / (Qr + Qe + self.Qinc)

    def Concatena_matrizes(self, matriz_difusa, matriz_contribuicoes):
        matriz_final = []
        i = 0
        j = 0
        T = self.T

        while i < len(matriz_difusa) or j < len(matriz_contribuicoes):
            if i == (len(matriz_difusa)) and j < len(matriz_contribuicoes):
                matriz_final.append(matriz_contribuicoes[j])
                j = j + 1
            elif j == (len(matriz_contribuicoes)) and i < len(matriz_difusa):
                vetor_aux = self.cria_vetor(matriz_difusa[i], T)
                matriz_final.append(vetor_aux)
                vetor_aux = []
                i = i + 1
            else:
                if matriz_difusa[i][6] < matriz_contribuicoes[j][10]:
                    vetor_aux = self.cria_vetor(matriz_difusa[i], T)
                    matriz_final.append(vetor_aux)
                    vetor_aux = []
                    i = i + 1
                elif matriz_difusa[i][6] == matriz_contribuicoes[j][10]:
                    T = matriz_contribuicoes[j][14]
                    new_dbo = self.eq_mistura_DBO(matriz_difusa[i][0], matriz_contribuicoes[j][0], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_od = self.eq_mistura_OD(matriz_difusa[i][1], matriz_contribuicoes[j][1], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_norg = self.eq_mistura_Norg(0, matriz_contribuicoes[j][2], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_namon = self.eq_mistura_Namon(matriz_difusa[i][2], matriz_contribuicoes[j][3], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_nnitri = self.eq_mistura_Nnitri(matriz_difusa[i][3], matriz_contribuicoes[j][4], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_nnitra = self.eq_mistura_Nnitra(0, matriz_contribuicoes[j][5], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_Porg = self.eq_mistura_Porg(0, matriz_contribuicoes[j][6], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_Pinorg = self.eq_mistura_Pinorg(matriz_difusa[i][4], matriz_contribuicoes[j][7], matriz_difusa[i][5], matriz_contribuicoes[j][9])
                    new_Coliformes = self.eq_mistura_Coliformes(matriz_difusa[i][5], matriz_contribuicoes[j][8], matriz_difusa[i][5], matriz_contribuicoes[j][9])

                    vetor_aux.append(new_dbo)
                    vetor_aux.append(new_od)
                    vetor_aux.append(new_norg)
                    vetor_aux.append(new_namon)
                    vetor_aux.append(new_nnitri)
                    vetor_aux.append(new_nnitra)
                    vetor_aux.append(new_Porg)
                    vetor_aux.append(new_Pinorg)
                    vetor_aux.append(new_Coliformes)
                    vetor_aux.append(matriz_contribuicoes[j][9] + matriz_difusa[i][6])
                    vetor_aux.append(matriz_contribuicoes[j][10])
                    vetor_aux.append(matriz_contribuicoes[j][11])
                    vetor_aux.append(matriz_contribuicoes[j][12])
                    vetor_aux.append(matriz_contribuicoes[j][13])
                    vetor_aux.append(T)
                    matriz_final.append(vetor_aux)
                    vetor_aux = []
                    i = i + 1
                    j = j + 1
                else:
                    T = matriz_contribuicoes[j][14]
                    matriz_final.append(matriz_contribuicoes[j])
                    j = j + 1
        return matriz_final

    def cria_vetor(self, vetor_difusa, T):
        vetor_final = [vetor_difusa[0], vetor_difusa[1], 0.0, vetor_difusa[2], vetor_difusa[3], 0.0, 0.0,
                       vetor_difusa[4], vetor_difusa[5], vetor_difusa[6], vetor_difusa[7], 0.0, 0.0, self.K1, T]
        return vetor_final
