from Otimizacao import Otimizacao
from QUAL_UFMG import QUAL_UFMG
from SCS import SCS
from Leitura import *
from Gera_Arquivos import *
from time import time

def executa(vetor_caminhos, diretorio_saidas, modo_execucao, label_caixa_texto, modo_otimizacao, simula_rio, simula_tributarios):
    if simula_rio.get(): vetor_caminhos[0] = vetor_caminhos[0][0]
    if simula_tributarios.get():
        vetor_caminhos[1] = list(vetor_caminhos[1])

    if modo_execucao.get() == "110":
        cenario_base_pontual = []
        # Simula Qualidade de Água Pontual  --> gera CBP
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Poluição Pontual\n"

        tempo_inicial = time()
        qual_ufmg = QUAL_UFMG()

        if simula_rio.get() and not simula_tributarios.get():
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], False)
            cenario_base_pontual_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
            cenario_base_pontual.append(cenario_base_pontual_rio)
            gera_saida_base_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"
        
        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], False)
                cenario_base_pontual_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_pontual.append(cenario_base_pontual_tributario)
                gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"
        
        else:
            cenario_base_pontual_tributarios = []
            celula_entrada_tributarios = []
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], False)
                cenario_base_pontual_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                celula_entrada_tributarios.append(rio.Nt)
                gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
            
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], False)
            cenario_base_pontual_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, cenario_base_pontual_tributarios, celula_entrada_tributarios)
            cenario_base_pontual.append(cenario_base_pontual_rio)
            gera_saida_base_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"
                     
        # Criacao dos parametros do retorno
        melhor_solucao_pontual = None
        cenario_base_difusa = None
        melhor_solucao_difusa = None
        historico_fo_pontual = None
        historico_fo = None
        historico_tempo_iteracoes_pontual = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos_pontual = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida_pontual = None
        iteracao_versao_rapida = None

        # Guardando perfil da vazao
        if simula_rio.get() or (not simula_rio.get() and len(vetor_caminhos[1]) == 1):
            perfilQ_pontual = cenario_base_pontual[0].PerfilQ
        else: perfilQ_pontual = None
        perfilQ = None

        print("Simulação de Qualidade de Água para poluição pontual concluída.\nGráficos e arquivos gerados.")

    elif modo_execucao.get() == "101":
        cenario_base_difusa = []
        # Simula Qualidade de Água Difusa  --> gera CBD
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Simulação Qualidade de Água: Poluição Difusa\n"

        tempo_inicial = time()
        qual_ufmg = QUAL_UFMG()

        if simula_rio.get() and not simula_tributarios.get():
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], True)
            cenario_base_difusa_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
            cenario_base_difusa.append(cenario_base_difusa_rio)
            gera_saida_base_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_difusa_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"
            
        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], True)
                cenario_base_difusa_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_difusa.append(cenario_base_difusa_tributario)
                gera_saida_base_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_difusa_tributario, tam_rio, tam_cel, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"

        else:
            cenario_base_difusa_tributarios = []
            celula_entrada_tributarios = []
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], True)
                cenario_base_difusa_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_difusa_tributarios.append(cenario_base_difusa_tributario)
                celula_entrada_tributarios.append(rio.Nt)
                gera_saida_base_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_difusa_tributario, tam_rio, tam_cel, i)
            
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], True)
            cenario_base_difusa_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, cenario_base_difusa_tributarios, celula_entrada_tributarios)
            cenario_base_difusa.append(cenario_base_difusa_rio)
            gera_saida_base_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_difusa_rio, tam_rio, tam_cel, -1)           
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"

        # Criacao dos parametros do retorno      
        cenario_base_pontual = None
        melhor_solucao_pontual = None
        melhor_solucao_difusa = None
        historico_fo_pontual = None
        historico_fo = None
        historico_tempo_iteracoes_pontual = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos_pontual = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida_pontual = None
        iteracao_versao_rapida = None

        # Guardando perfil da vazao
        if simula_rio.get() or (not simula_rio.get() and len(vetor_caminhos[1]) == 1):
            perfilQ = cenario_base_difusa[0].PerfilQ
        else: perfilQ = None
        perfilQ_pontual = None

        print("Simulação de Qualidade de Água para poluição difusa concluída.\nGráficos e arquivos gerados.")

    elif modo_execucao.get() == "111":
        cenario_base_pontual = []
        cenario_base_difusa = []
        # Simula Qualidade de Água Difusa  --> gera CBP e CBD
        label_caixa_texto["text"] = label_caixa_texto["text"] + " Poluição Pontual + Poluição Difusa\n"

        tempo_inicial = time()
        qual_ufmg = QUAL_UFMG()

        if simula_rio.get() and not simula_tributarios.get():
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], False)
            cenario_base_pontual_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
            cenario_base_pontual.append(cenario_base_pontual_rio)
            gera_saida_base_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"

            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], True)
            cenario_base_difusa_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
            cenario_base_difusa.append(cenario_base_difusa_rio)
            gera_saida_base_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_difusa_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"
            
        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], False)
                cenario_base_pontual_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_pontual.append(cenario_base_pontual_tributario)
                gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"

            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], True)
                cenario_base_difusa_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_difusa.append(cenario_base_difusa_tributario)
                gera_saida_base_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_difusa_tributario, tam_rio, tam_cel, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"

        else:
            cenario_base_pontual_tributarios = []
            celula_entrada_tributarios = []
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], False)
                cenario_base_pontual_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                celula_entrada_tributarios.append(rio.Nt)
                gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
            
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], False)
            cenario_base_pontual_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, cenario_base_pontual_tributarios, celula_entrada_tributarios)
            cenario_base_pontual.append(cenario_base_pontual_rio)
            gera_saida_base_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, tam_rio, tam_cel, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Pontual: " + str(tempo_final - tempo_inicial) + "\n"
                     
            cenario_base_difusa_tributarios = []
            celula_entrada_tributarios = []
            for i in range(len(vetor_caminhos[1])):
                [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[1][i], True)
                cenario_base_difusa_tributario = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, None, None)
                cenario_base_difusa_tributarios.append(cenario_base_difusa_tributario)
                celula_entrada_tributarios.append(rio.Nt)
                gera_saida_base_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_difusa_tributario, tam_rio, tam_cel, i)
            
            [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(vetor_caminhos[0], True)
            cenario_base_difusa_rio = qual_ufmg.executa(rio, matriz_contribuicoes, matriz_reducoes, True, [], scs, None, matriz_tipo_contribuicoes, cenario_base_difusa_tributarios, celula_entrada_tributarios)
            cenario_base_difusa.append(cenario_base_difusa_rio)
            gera_saida_base_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_difusa_rio, tam_rio, tam_cel, -1)           
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Poluição Difusa: " + str(tempo_final - tempo_inicial) + "\n"
        
        # Criacao dos parametros do retorno
        melhor_solucao_pontual = None
        melhor_solucao_difusa = None
        historico_fo_pontual = None
        historico_fo = None
        historico_tempo_iteracoes_pontual = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos_pontual = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida_pontual = None
        iteracao_versao_rapida = None

        # Guardando perfil da vazao
        if simula_rio.get() or (not simula_rio.get() and len(vetor_caminhos[1]) == 1):
            perfilQ_pontual = cenario_base_pontual[0].PerfilQ
            perfilQ = cenario_base_difusa[0].PerfilQ
        else:
            perfilQ = None
            perfilQ_pontual = None

        print("Simulação de Qualidade de Água para poluição pontual e difusa concluída.\nGráficos e arquivos gerados.")

    elif modo_execucao.get() == 2:
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Modelo de Cargas Difusas.\nArquivos gerados.\n(OBS: nesse modo de execução não há geração de saídas gráficas)."

        tempo_inicial = time()

        if simula_rio.get() and not simula_tributarios.get():
            scs_rio = SCS(vetor_caminhos[0])
            [_, _, _] = scs_rio.executa([])
            gera_saida_estimar_cargas(vetor_caminhos[0], diretorio_saidas, scs_rio, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Estimação do Modelo de Cargas Difusas: " + str(tempo_final - tempo_inicial) + "\n"

        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                scs_tributario = SCS(vetor_caminhos[1][i])
                [_, _, _] = scs_tributario.executa([])
                gera_saida_estimar_cargas(vetor_caminhos[1][i], diretorio_saidas, scs_tributario, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Estimação do Modelo de Cargas Difusas: " + str(tempo_final - tempo_inicial) + "\n"

        else:
            scs_rio = SCS(vetor_caminhos[0])
            [_, _, _] = scs_rio.executa([])
            gera_saida_estimar_cargas(vetor_caminhos[0], diretorio_saidas, scs_rio, -1)

            for i in range(len(vetor_caminhos[1])):
                scs_tributario = SCS(vetor_caminhos[1][i])
                [_, _, _] = scs_tributario.executa([])
                gera_saida_estimar_cargas(vetor_caminhos[1][i], diretorio_saidas, scs_tributario, i)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Estimação do Modelo de Cargas Difusas: " + str(tempo_final - tempo_inicial) + "\n"

        # Criacao dos parametros do retorno
        cenario_base_pontual = None
        melhor_solucao_pontual = None
        cenario_base_difusa = None
        melhor_solucao_difusa = None
        historico_fo_pontual = None
        historico_fo = None
        historico_tempo_iteracoes_pontual = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos_pontual = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida_pontual = None
        iteracao_versao_rapida = None
        tam_rio = None
        tam_cel = None
        ph = None
        perfilQ_pontual = None
        perfilQ = None

        print("Estimação de cargas difusas concluída.\nArquivos gerados.")
    
    elif modo_execucao.get() == "21":
        cenario_base_pontual = []
        melhor_solucao_pontual = []
        historico_fo_pontual = []
        historico_tempo_iteracoes_pontual = []
        historico_filhos_invalidos_pontual = []
        iteracao_versao_rapida_pontual = []
        perfilQ_pontual = []
        
        # Otimizacao modo pontual  --> gera CBP e COP
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Otimização de Cargas Pontuais \n"
        
        tempo_inicial = time()
        otimizacao = Otimizacao()

        if simula_rio.get() and not simula_tributarios.get():                                                                                                                                                                                  
            [cenario_base_pontual_rio, melhores_solucoes_pontual_rio, tempo_pontual_rio, tempo_pontual_rapida_rio, tam_rio, tam_cel, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, historico_fo_pontual_rio, historico_tempo_iteracoes_pontual_rio, historico_filhos_invalidos_pontual_rio, iteracao_versao_rapida_pontual_rio, ph, melhor_solucao_pontual_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], False, modo_otimizacao.get(), None, None)
            melhor_solucao_pontual_rio = melhores_solucoes_pontual_rio[-1]

            cenario_base_pontual.append(cenario_base_pontual_rio)
            melhor_solucao_pontual.append(melhor_solucao_pontual_rio)
            historico_fo_pontual.append(historico_fo_pontual_rio)
            historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_rio)
            historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_rio)
            iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_rio)
            perfilQ_pontual.append(melhor_solucao_pontual_rio.cenario.PerfilQ)

            gera_saida_otimizado_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, melhor_solucao_pontual_rio, melhor_solucao_pontual_rapida_rio, tam_rio, tam_cel, tempo_pontual_rio, tempo_pontual_rapida_rio, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Otimização Pontual: " + str(tempo_final - tempo_inicial) + "\n"

        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                [cenario_base_pontual_tributario, melhores_solucoes_pontual_tributario, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, historico_fo_pontual_tributario, historico_tempo_iteracoes_pontual_tributario, historico_filhos_invalidos_pontual_tributario, iteracao_versao_rapida_pontual_tributario, ph, melhor_solucao_pontual_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], False, modo_otimizacao.get(), None, None)
                melhor_solucao_pontual_tributario = melhores_solucoes_pontual_tributario[-1]

                cenario_base_pontual.append(cenario_base_pontual_tributario)
                melhor_solucao_pontual.append(melhor_solucao_pontual_tributario)
                historico_fo_pontual.append(historico_fo_pontual_tributario)
                historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_tributario)
                historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_tributario)
                iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_tributario)
                perfilQ_pontual.append(melhor_solucao_pontual_tributario.cenario.PerfilQ)

                gera_saida_otimizado_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, melhor_solucao_pontual_tributario, melhor_solucao_pontual_rapida_tributario, tam_rio, tam_cel, tempo_pontual_tributario, tempo_pontual_rapida_tributario, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, i)
                tempo_final = time()
                label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Otimização Pontual: " + str(tempo_final - tempo_inicial) + "\n"
        
        else:
            cenario_base_pontual_tributarios = []
            melhor_solucao_pontual_tributarios = []
            historico_fo_pontual_tributarios = []
            historico_tempo_iteracoes_pontual_tributarios = []
            historico_filhos_invalidos_pontual_tributarios = []
            iteracao_versao_rapida_pontual_tributarios = []
            perfilQ_pontual_tributarios = []
            celula_entrada_tributarios = []

            for i in range(len(vetor_caminhos[1])):
                [cenario_base_pontual_tributario, melhores_solucoes_pontual_tributario, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, historico_fo_pontual_tributario, historico_tempo_iteracoes_pontual_tributario, historico_filhos_invalidos_pontual_tributario, iteracao_versao_rapida_pontual_tributario, ph, melhor_solucao_pontual_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], False, modo_otimizacao.get(), None, None)
                
                if melhores_solucoes_pontual_tributario:
                    melhor_solucao_pontual_tributario = melhores_solucoes_pontual_tributario[-1]
                    cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                    melhor_solucao_pontual_tributarios.append(melhor_solucao_pontual_tributario.cenario)
                    historico_fo_pontual_tributarios.append(historico_fo_pontual_tributario)
                    historico_tempo_iteracoes_pontual_tributarios.append(historico_tempo_iteracoes_pontual_tributario)
                    historico_filhos_invalidos_pontual_tributarios.append(historico_filhos_invalidos_pontual_tributario)
                    iteracao_versao_rapida_pontual_tributarios.append(iteracao_versao_rapida_pontual_tributario)
                    perfilQ_pontual_tributarios.append(melhor_solucao_pontual_tributario.cenario.PerfilQ)
                    celula_entrada_tributarios.append(rio.Nt)

                    gera_saida_otimizado_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, melhor_solucao_pontual_tributario, melhor_solucao_pontual_rapida_tributario, tam_rio, tam_cel, tempo_pontual_tributario, tempo_pontual_rapida_tributario, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, i)
            
                else:
                    melhor_solucao_pontual_tributario = cenario_base_pontual_tributario
                    cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                    melhor_solucao_pontual_tributarios.append(melhor_solucao_pontual_tributario)
                    celula_entrada_tributarios.append(rio.Nt)

                    gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
            
            [cenario_base_pontual_rio, melhores_solucoes_pontual_rio, tempo_pontual_rio, tempo_pontual_rapida_rio, tam_rio, tam_cel, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, historico_fo_pontual_rio, historico_tempo_iteracoes_pontual_rio, historico_filhos_invalidos_pontual_rio, iteracao_versao_rapida_pontual_rio, ph, melhor_solucao_pontual_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], False, modo_otimizacao.get(), melhor_solucao_pontual_tributarios, celula_entrada_tributarios)
            melhor_solucao_pontual_rio = melhores_solucoes_pontual_rio[-1]

            cenario_base_pontual.append(cenario_base_pontual_rio)
            melhor_solucao_pontual.append(melhor_solucao_pontual_rio)
            historico_fo_pontual.append(historico_fo_pontual_rio)
            historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_rio)
            historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_rio)
            iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_rio)
            perfilQ_pontual.append(melhor_solucao_pontual_rio.cenario.PerfilQ)

            gera_saida_otimizado_pontual(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, melhor_solucao_pontual_rio, melhor_solucao_pontual_rapida_rio, tam_rio, tam_cel, tempo_pontual_rio, tempo_pontual_rapida_rio, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Otimização Pontual: " + str(tempo_final - tempo_inicial) + "\n"

        cenario_base_difusa = None
        melhor_solucao_difusa = None
        historico_fo = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida = None
        perfilQ = None
   
    elif modo_execucao.get() == "22":
        cenario_base_pontual = []
        melhor_solucao_pontual = []
        historico_fo_pontual = []
        historico_tempo_iteracoes_pontual = []
        historico_filhos_invalidos_pontual = []
        iteracao_versao_rapida_pontual = []
        perfilQ_pontual = []
        cenario_base_difusa = []
        melhor_solucao_difusa = []
        historico_fo = []
        historico_tempo_iteracoes = []
        historico_filhos_invalidos = []
        iteracao_versao_rapida = []
        perfilQ = []
        
        # Otimizacao modo pontual  --> gera CBP e COP
        label_caixa_texto["text"] = label_caixa_texto["text"] + "Otimização de Cargas Pontuais \n"
        
        tempo_inicial = time()
        otimizacao = Otimizacao()

        if simula_rio.get() and not simula_tributarios.get():
            # Cenário Pontual                                                                                                                                                                               
            [cenario_base_pontual_rio, melhores_solucoes_pontual_rio, tempo_pontual_rio, tempo_pontual_rapida_rio, tam_rio, tam_cel, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, historico_fo_pontual_rio, historico_tempo_iteracoes_pontual_rio, historico_filhos_invalidos_pontual_rio, iteracao_versao_rapida_pontual_rio, ph, melhor_solucao_pontual_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], False, modo_otimizacao.get(), None, None)
            melhor_solucao_pontual_rio = melhores_solucoes_pontual_rio[-1]

            cenario_base_pontual.append(cenario_base_pontual_rio)
            melhor_solucao_pontual.append(melhor_solucao_pontual_rio)
            historico_fo_pontual.append(historico_fo_pontual_rio)
            historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_rio)
            historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_rio)
            iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_rio)
            perfilQ_pontual.append(melhor_solucao_pontual_rio.cenario.PerfilQ)
            
            # Cenário Difuso
            [cenario_base_difusa_rio, melhores_solucoes_difusa_rio, tempo_difusa_rio, tempo_difusa_rapida_rio, tam_rio, tam_cel, vetor_invalidos_difusa_rio, vetor_invalidos_difusa_rapida_rio, historico_fo_difusa_rio, historico_tempo_iteracoes_difusa_rio, historico_filhos_invalidos_difusa_rio, iteracao_versao_rapida_difusa_rio, ph, melhor_solucao_difusa_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], True, modo_otimizacao.get(), None, None)
            melhor_solucao_difusa_rio = melhores_solucoes_difusa_rio[-1]

            cenario_base_difusa.append(cenario_base_difusa_rio)
            melhor_solucao_difusa.append(melhor_solucao_difusa_rio)
            historico_fo.append(historico_fo_difusa_rio)
            historico_tempo_iteracoes.append(historico_tempo_iteracoes_difusa_rio)
            historico_filhos_invalidos.append(historico_filhos_invalidos_difusa_rio)
            iteracao_versao_rapida.append(iteracao_versao_rapida_difusa_rio)
            perfilQ.append(melhor_solucao_difusa_rio.cenario.PerfilQ)

            gera_saida_otimizada_pontual_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, cenario_base_difusa_rio, melhor_solucao_pontual_rio, melhor_solucao_pontual_rapida_rio, melhor_solucao_difusa_rio, melhor_solucao_difusa_rapida_rio, tam_rio, tam_cel, tempo_pontual_rio, tempo_pontual_rapida_rio, tempo_difusa_rio, tempo_difusa_rapida_rio, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, vetor_invalidos_difusa_rio, vetor_invalidos_difusa_rapida_rio, -1)

            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal dada com sucesso!\nTempo de execução da Otimização Pontual e Difusa: " + str(tempo_final - tempo_inicial) + "\n"

        elif not simula_rio.get() and simula_tributarios.get():
            for i in range(len(vetor_caminhos[1])):
                # Cenário Pontual
                [cenario_base_pontual_tributario, melhores_solucoes_pontual_tributario, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, historico_fo_pontual_tributario, historico_tempo_iteracoes_pontual_tributario, historico_filhos_invalidos_pontual_tributario, iteracao_versao_rapida_pontual_tributario, ph, melhor_solucao_pontual_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], False, modo_otimizacao.get(), None, None)
                melhor_solucao_pontual_tributario = melhores_solucoes_pontual_tributario[-1]

                cenario_base_pontual.append(cenario_base_pontual_tributario)
                melhor_solucao_pontual.append(melhor_solucao_pontual_tributario)
                historico_fo_pontual.append(historico_fo_pontual_tributario)
                historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_tributario)
                historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_tributario)
                iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_tributario)
                perfilQ_pontual.append(melhor_solucao_pontual_tributario.cenario.PerfilQ)

                # Cenário Difuso
                [cenario_base_difusa_tributario, melhores_solucoes_difusa_tributario, tempo_difusa_tributario, tempo_difusa_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_difusa_tributario, vetor_invalidos_difusa_rapida_tributario, historico_fo_difusa_tributario, historico_tempo_iteracoes_difusa_tributario, historico_filhos_invalidos_difusa_tributario, iteracao_versao_rapida_difusa_tributario, ph, melhor_solucao_difusa_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], True, modo_otimizacao.get(), None, None)
                melhor_solucao_difusa_tributario = melhores_solucoes_difusa_tributario[-1]

                cenario_base_difusa.append(cenario_base_difusa_tributario)
                melhor_solucao_difusa.append(melhor_solucao_difusa_tributario)
                historico_fo.append(historico_fo_difusa_tributario)
                historico_tempo_iteracoes.append(historico_tempo_iteracoes_difusa_tributario)
                historico_filhos_invalidos.append(historico_filhos_invalidos_difusa_tributario)
                iteracao_versao_rapida.append(iteracao_versao_rapida_difusa_tributario)
                perfilQ.append(melhor_solucao_difusa_tributario.cenario.PerfilQ)
                
                gera_saida_otimizada_pontual_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, cenario_base_difusa_tributario, melhor_solucao_pontual_tributario, melhor_solucao_pontual_rapida_tributario, melhor_solucao_difusa_tributario, melhor_solucao_difusa_rapida_tributario, tam_rio, tam_cel, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tempo_difusa_tributario, tempo_difusa_rapida_tributario, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, vetor_invalidos_difusa_tributario, vetor_invalidos_difusa_rapida_tributario, i)

            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do(s) Tributário(s) dada com sucesso!\nTempo de execução da Otimização Pontual e Difusa: " + str(tempo_final - tempo_inicial) + "\n"
        
        else:
            cenario_base_pontual_tributarios = []
            melhor_solucao_pontual_tributarios = []
            historico_fo_pontual_tributarios = []
            historico_tempo_iteracoes_pontual_tributarios = []
            historico_filhos_invalidos_pontual_tributarios = []
            iteracao_versao_rapida_pontual_tributarios = []
            perfilQ_pontual_tributarios = []
            celula_entrada_tributarios = []
            cenario_base_difusa_tributarios = []
            melhor_solucao_difusa_tributarios = []
            historico_fo_difusa_tributarios = []
            historico_tempo_iteracoes_difusa_tributarios = []
            historico_filhos_invalidos_difusa_tributarios = []
            iteracao_versao_rapida_difusa_tributarios = []
            perfilQ_difusa_tributarios = []
            celula_entrada_tributarios = []

            for i in range(len(vetor_caminhos[1])):
                [cenario_base_pontual_tributario, melhores_solucoes_pontual_tributario, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, historico_fo_pontual_tributario, historico_tempo_iteracoes_pontual_tributario, historico_filhos_invalidos_pontual_tributario, iteracao_versao_rapida_pontual_tributario, ph, melhor_solucao_pontual_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], False, modo_otimizacao.get(), None, None)
                [cenario_base_difusa_tributario, melhores_solucoes_difusa_tributario, tempo_difusa_tributario, tempo_difusa_rapida_tributario, tam_rio, tam_cel, vetor_invalidos_difusa_tributario, vetor_invalidos_difusa_rapida_tributario, historico_fo_difusa_tributario, historico_tempo_iteracoes_difusa_tributario, historico_filhos_invalidos_difusa_tributario, iteracao_versao_rapida_difusa_tributario, ph, melhor_solucao_difusa_rapida_tributario, rio] = otimizacao.executa(vetor_caminhos[1][i], True, modo_otimizacao.get(), None, None)
                
                if melhores_solucoes_pontual_tributario:
                    melhor_solucao_pontual_tributario = melhores_solucoes_pontual_tributario[-1]
                    cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                    melhor_solucao_pontual_tributarios.append(melhor_solucao_pontual_tributario.cenario)
                    historico_fo_pontual_tributarios.append(historico_fo_pontual_tributario)
                    historico_tempo_iteracoes_pontual_tributarios.append(historico_tempo_iteracoes_pontual_tributario)
                    historico_filhos_invalidos_pontual_tributarios.append(historico_filhos_invalidos_pontual_tributario)
                    iteracao_versao_rapida_pontual_tributarios.append(iteracao_versao_rapida_pontual_tributario)
                    perfilQ_pontual_tributarios.append(melhor_solucao_pontual_tributario.cenario.PerfilQ)

                    melhor_solucao_difusa_tributario = melhores_solucoes_difusa_tributario[-1]
                    cenario_base_difusa_tributarios.append(cenario_base_difusa_tributario)
                    melhor_solucao_difusa_tributarios.append(melhor_solucao_difusa_tributario.cenario)
                    historico_fo_difusa_tributarios.append(historico_fo_difusa_tributario)
                    historico_tempo_iteracoes_difusa_tributarios.append(historico_tempo_iteracoes_difusa_tributario)
                    historico_filhos_invalidos_difusa_tributarios.append(historico_filhos_invalidos_difusa_tributario)
                    iteracao_versao_rapida_difusa_tributarios.append(iteracao_versao_rapida_difusa_tributario)
                    perfilQ_difusa_tributarios.append(melhor_solucao_difusa_tributario.cenario.PerfilQ)

                    celula_entrada_tributarios.append(rio.Nt)
                    gera_saida_otimizada_pontual_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, cenario_base_difusa_tributario, melhor_solucao_pontual_tributario, melhor_solucao_pontual_rapida_tributario, melhor_solucao_difusa_tributario, melhor_solucao_difusa_rapida_tributario, tam_rio, tam_cel, tempo_pontual_tributario, tempo_pontual_rapida_tributario, tempo_difusa_tributario, tempo_difusa_rapida_tributario, vetor_invalidos_pontual_tributario, vetor_invalidos_pontual_rapida_tributario, vetor_invalidos_difusa_tributario, vetor_invalidos_difusa_rapida_tributario, i)

                else:
                    melhor_solucao_pontual_tributario = cenario_base_pontual_tributario
                    cenario_base_pontual_tributarios.append(cenario_base_pontual_tributario)
                    melhor_solucao_pontual_tributarios.append(melhor_solucao_pontual_tributario)

                    melhor_solucao_difusa_tributario = cenario_base_difusa_tributario
                    cenario_base_difusa_tributarios.append(cenario_base_difusa_tributario)
                    melhor_solucao_difusa_tributarios.append(melhor_solucao_difusa_tributario)

                    celula_entrada_tributarios.append(rio.Nt)
                    gera_saida_base_pontual(vetor_caminhos[1][i], diretorio_saidas, cenario_base_pontual_tributario, tam_rio, tam_cel, i)
                    gera_saida_base_difusa(vetor_caminhos[1][i], diretorio_saidas, cenario_base_difusa_tributario, tam_rio, tam_cel, i)
            
            [cenario_base_pontual_rio, melhores_solucoes_pontual_rio, tempo_pontual_rio, tempo_pontual_rapida_rio, tam_rio, tam_cel, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, historico_fo_pontual_rio, historico_tempo_iteracoes_pontual_rio, historico_filhos_invalidos_pontual_rio, iteracao_versao_rapida_pontual_rio, ph, melhor_solucao_pontual_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], False, modo_otimizacao.get(), melhor_solucao_pontual_tributarios, celula_entrada_tributarios)
            melhor_solucao_pontual_rio = melhores_solucoes_pontual_rio[-1]

            cenario_base_pontual.append(cenario_base_pontual_rio)
            melhor_solucao_pontual.append(melhor_solucao_pontual_rio)
            historico_fo_pontual.append(historico_fo_pontual_rio)
            historico_tempo_iteracoes_pontual.append(historico_tempo_iteracoes_pontual_rio)
            historico_filhos_invalidos_pontual.append(historico_filhos_invalidos_pontual_rio)
            iteracao_versao_rapida_pontual.append(iteracao_versao_rapida_pontual_rio)
            perfilQ_pontual.append(melhor_solucao_pontual_rio.cenario.PerfilQ)

            [cenario_base_difusa_rio, melhores_solucoes_difusa_rio, tempo_difusa_rio, tempo_difusa_rapida_rio, tam_rio, tam_cel, vetor_invalidos_difusa_rio, vetor_invalidos_difusa_rapida_rio, historico_fo_difusa_rio, historico_tempo_iteracoes_difusa_rio, historico_filhos_invalidos_difusa_rio, iteracao_versao_rapida_difusa_rio, ph, melhor_solucao_difusa_rapida_rio, rio] = otimizacao.executa(vetor_caminhos[0], True, modo_otimizacao.get(), melhor_solucao_difusa_tributarios, celula_entrada_tributarios)
            melhor_solucao_difusa_rio = melhores_solucoes_difusa_rio[-1]

            cenario_base_difusa.append(cenario_base_difusa_rio)
            melhor_solucao_difusa.append(melhor_solucao_difusa_rio)
            historico_fo.append(historico_fo_difusa_rio)
            historico_tempo_iteracoes.append(historico_tempo_iteracoes_difusa_rio)
            historico_filhos_invalidos.append(historico_filhos_invalidos_difusa_rio)
            iteracao_versao_rapida.append(iteracao_versao_rapida_difusa_rio)
            perfilQ.append(melhor_solucao_difusa_rio.cenario.PerfilQ)

            gera_saida_otimizada_pontual_difusa(vetor_caminhos[0], diretorio_saidas, cenario_base_pontual_rio, cenario_base_difusa_rio, melhor_solucao_pontual_rio, melhor_solucao_pontual_rapida_rio, melhor_solucao_difusa_rio, melhor_solucao_difusa_rapida_rio, tam_rio, tam_cel, tempo_pontual_rio, tempo_pontual_rapida_rio, tempo_difusa_rio, tempo_difusa_rapida_rio, vetor_invalidos_pontual_rio, vetor_invalidos_pontual_rapida_rio, vetor_invalidos_difusa_rio, vetor_invalidos_difusa_rapida_rio, -1)
            tempo_final = time()
            label_caixa_texto["text"] = label_caixa_texto["text"] + "\nSaida do Rio Principal e do(s) Tributário(s) dada com sucesso!\nTempo de execução da Otimização Pontual e Difusa: " + str(tempo_final - tempo_inicial) + "\n"

    return [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
            historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
            historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ]      