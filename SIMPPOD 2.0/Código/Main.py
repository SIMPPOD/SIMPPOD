from Otimizacao import Otimizacao
from QUAL_UFMG import QUAL_UFMG
from SCS import SCS
from Leitura import *
from Gera_Arquivos import *
from time import time

def monta_perfil_total(perfil_total):
    if len(perfil_total[0]) > 1:
        # Inicializando a variável para armazenar o último valor da primeira sublista
        ultimo_valor_sublista_anterior = perfil_total[0][-1]

        # Aplanando a lista de listas em um único vetor e somando os valores
        vetor = []

        for i, sublist in enumerate(perfil_total):
            if i == 0:
                vetor.extend(sublist)
            else:
                # Somando elementos da sublista com o último valor da lista anterior
                sublist = [elemento + ultimo_valor_sublista_anterior for elemento in sublist]
                
                # Estendendo o vetor com a sublista resultante
                vetor.extend(sublist)
            
            # Atualizando o último valor da lista anterior, exceto para a última sublista
            if i != len(perfil_total) - 1:
                ultimo_valor_sublista_anterior = sublist[-1]
        return vetor
    else: return perfil_total[0]

def executa(vetor_caminhos, diretorio_saidas, modo_execucao, label_caixa_texto, modo_otimizacao, simula_rio, simula_tributarios):
    if simula_rio.get(): vetor_caminhos[0] = vetor_caminhos[0][0]
    id_principal = int(ler_entrada_constantes(vetor_caminhos[0])[47])

    if simula_tributarios.get():
        vetor_caminhos[1] = list(vetor_caminhos[1])
    
    idmax = 0
    for i in range(len(vetor_caminhos[1])):
        id = int(ler_entrada_constantes(vetor_caminhos[1][i])[47])
        if id > idmax: idmax = id
    id = int(ler_entrada_constantes(vetor_caminhos[0])[47])
    if id > idmax: idmax = id
    idmax += 1

    # Vetor dos caminhos de cada curso
    cursos = [[]]*idmax
    for caminho in vetor_caminhos[1]:
        id = int(ler_entrada_constantes(caminho)[47])
        cursos[id] = caminho
    id = int(ler_entrada_constantes(vetor_caminhos[0])[47])
    cursos[id] = vetor_caminhos[0]

    # Vetor dos caminhos de curso com seus braços
    jusante_bracos = [[0, []] for _ in range(len(cursos))]
    for i in range(len(cursos)):
        if len(cursos[i]):
            jusante = ler_entrada_constantes(cursos[i])
            jusante_bracos[int(jusante[47])][0] = cursos[i]
            if jusante[47] != jusante[48]: jusante_bracos[int(jusante[48])][1].append(cursos[i])

    # Vetor que guarda a simulação de um curso
    simulacao_curso = [[]]*len(cursos)
    visitado_curso = [False]*len(cursos)
    celula_entrada_tributarios = [[0, []] for _ in range(len(jusante_bracos))]

    # Simulação por jusante
    
    [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa, 
     historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
     historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
     tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida, perfil_vazao_total, perfil_dbo_total, perfil_od_total] = executa_jusante(jusante_bracos[id_principal], jusante_bracos, visitado_curso, simulacao_curso, celula_entrada_tributarios, diretorio_saidas, modo_execucao, label_caixa_texto, modo_otimizacao, simula_rio, simula_tributarios, [], [], [])
    
    vetor_vazao = monta_perfil_total(perfil_vazao_total)
    vetor_dbo = monta_perfil_total(perfil_dbo_total)
    vetor_od = monta_perfil_total(perfil_od_total)

    return [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
            historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
            historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida, vetor_vazao, vetor_dbo, vetor_od]      

def executa_jusante(jusante, jusante_bracos, visitado_curso, simulacao_curso, celula_entrada_tributarios, diretorio_saidas, modo_execucao, label_caixa_texto, modo_otimizacao, simula_rio, simula_tributarios, perfil_vazao_total, perfil_dbo_total, perfil_od_total):
    # Simulando curso por recursão
    id_corpo = int(ler_entrada_constantes(jusante[0])[47])  # Pega o id do corpo sendo analisado
    if jusante[1]:  # Se o corpo tiver braços
        aux1 = [jusante[0]]
        aux2 = []
        for i in range(len(jusante[1])):  # Para cada um dos braços do corpo
            braco = ler_entrada_constantes(jusante[1][i])  # Pega o braço sendo analisado
            id_braco = int(braco[47])  # Pega o id desse braço
            braco[46] *= 1000 / braco[1]
            celula_entrada_tributarios[id_corpo][0] = id_corpo
            celula_entrada_tributarios[id_corpo][1].append(braco[46])
            if not visitado_curso[id_braco]:  # Se o braço não tiver sido visitado ainda
                visitado_curso[id_braco] = True  # Visita o braço
                executa_jusante(jusante_bracos[id_braco], jusante_bracos, visitado_curso, simulacao_curso, celula_entrada_tributarios, diretorio_saidas, modo_execucao, label_caixa_texto, modo_otimizacao, simula_rio, simula_tributarios, perfil_vazao_total, perfil_dbo_total, perfil_od_total)
            aux2.append(braco) 
        aux1.append(aux2)

        [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
         historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
         historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
         tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida] = simula_curso(aux1, simulacao_curso, celula_entrada_tributarios[id_corpo][1], diretorio_saidas, modo_execucao, modo_otimizacao)

        gerar_grafico = int(ler_entrada_constantes(jusante[0])[49])
        if gerar_grafico:
            perfil_dbo_total.append(cenario_base_pontual.Y_DBO)
            perfil_od_total.append(cenario_base_pontual.Y_OD)
            perfil_vazao_total.append(cenario_base_pontual.PerfilQ)

        if modo_execucao.get() == "110": simulacao_curso[id_corpo] = cenario_base_pontual
        elif modo_execucao.get() == "21":
            if melhor_solucao_pontual: simulacao_curso[id_corpo] = melhor_solucao_pontual.cenario
            else: simulacao_curso[id_corpo] = cenario_base_pontual

        return [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
                historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
                historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
                tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida, perfil_vazao_total, perfil_dbo_total, perfil_od_total]

    else:  # Se o corpo não tiver braços

        [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
         historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
         historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
         tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida] = simula_curso(jusante, simulacao_curso, celula_entrada_tributarios[id_corpo][1], diretorio_saidas, modo_execucao, modo_otimizacao)
        
        gerar_grafico = int(ler_entrada_constantes(jusante[0])[49])
        if gerar_grafico:
            perfil_dbo_total.append(cenario_base_pontual.Y_DBO)
            perfil_od_total.append(cenario_base_pontual.Y_OD)
            perfil_vazao_total.append(cenario_base_pontual.PerfilQ)            

        if modo_execucao.get() == "110": simulacao_curso[id_corpo] = cenario_base_pontual
        elif modo_execucao.get() == "21":
            if melhor_solucao_pontual: simulacao_curso[id_corpo] = melhor_solucao_pontual.cenario
            else: simulacao_curso[id_corpo] = cenario_base_pontual

        return [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
                historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
                historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
                tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida, perfil_vazao_total, perfil_dbo_total, perfil_od_total]
        
def simula_curso(caminho_curso, simulacao_curso, celula_entrada_tributarios, diretorio_saidas, modo_execucao, modo_otimizacao):
    print("SIMULANDO ", caminho_curso[0])
    if modo_execucao.get() == "110":
        # Simula Qualidade de Água Pontual  --> gera CBP
        qual_ufmg = QUAL_UFMG()
        [rio, matriz_contribuicoes, matriz_reducoes, scs, tam_rio, tam_cel, ph, matriz_tipo_contribuicoes] = qual_ufmg.constroi_param_ini(caminho_curso[0], False)

        cenario_base_pontual = qual_ufmg.executa(caminho_curso, simulacao_curso, rio, matriz_contribuicoes, matriz_reducoes, False, [], scs, None, matriz_tipo_contribuicoes, celula_entrada_tributarios)
        gera_saida_base_pontual(caminho_curso[0], diretorio_saidas, cenario_base_pontual, tam_rio, tam_cel)
        
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
        perfilQ_pontual = cenario_base_pontual.PerfilQ
        perfilQ = None
        melhor_solucao_pontual_rapida = None

    elif modo_execucao.get() == "21":
        # Otimizacao modo pontual  --> gera CBP e COP
        otimizacao = Otimizacao()
        [cenario_base_pontual, melhores_solucoes_pontual, tempo_pontual, tempo_pontual_rapida, tam_rio, tam_cel, vetor_invalidos_pontual, vetor_invalidos_pontual_rapida, historico_fo_pontual, historico_tempo_iteracoes_pontual, historico_filhos_invalidos_pontual, iteracao_versao_rapida_pontual, ph, melhor_solucao_pontual_rapida, rio] = otimizacao.executa(caminho_curso, False, modo_otimizacao.get(), simulacao_curso, celula_entrada_tributarios)
        
        if melhores_solucoes_pontual:
            melhor_solucao_pontual = melhores_solucoes_pontual[-1]
            perfilQ_pontual = melhor_solucao_pontual.cenario.PerfilQ                                                                    
            gera_saida_otimizado_pontual(caminho_curso[0], diretorio_saidas, cenario_base_pontual, melhor_solucao_pontual, melhor_solucao_pontual_rapida, tam_rio, tam_cel, tempo_pontual, tempo_pontual_rapida, vetor_invalidos_pontual, vetor_invalidos_pontual_rapida)
        else:
            melhor_solucao_pontual = None
            perfilQ_pontual = cenario_base_pontual.PerfilQ
            gera_saida_base_pontual(caminho_curso[0], diretorio_saidas, cenario_base_pontual, tam_rio, tam_cel)

        cenario_base_difusa = None
        melhor_solucao_difusa = None
        historico_fo = None
        historico_tempo_iteracoes = None
        historico_filhos_invalidos = None
        iteracao_versao_rapida = None   
        perfilQ = None
        
    return [cenario_base_pontual, melhor_solucao_pontual, cenario_base_difusa, melhor_solucao_difusa,
            historico_fo_pontual, historico_fo, historico_tempo_iteracoes_pontual, historico_tempo_iteracoes,
            historico_filhos_invalidos_pontual, historico_filhos_invalidos, iteracao_versao_rapida_pontual, iteracao_versao_rapida,
            tam_rio, tam_cel, ph, perfilQ_pontual, perfilQ, melhor_solucao_pontual_rapida]  