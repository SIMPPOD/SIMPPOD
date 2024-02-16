import random
from Cromossomo import Cromossomo
from deap import base, creator, tools

class NSGA2:

    class Evolution:

        def __init__(self, problem, num_of_individuals, num_of_tour_particips,
                    tournament_prob, crossover_param, mutation_param):
            self.utils = NSGA2.NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param,
                                    mutation_param)
            self.population = None
            self.on_generation_finished = []        

    class Individual(object):

        def __init__(self):
            self.rank = None
            self.crowding_distance = None
            self.domination_count = None
            self.dominated_solutions = None
            self.features = None
            self.objectives = None

        @staticmethod
        def dominates(individual, other_individual):
            # a minha FO é menor que a FO do outro? Se eu for maior ou igual, eu não domino
            #and_condition = True
            #or_condition = False
            #for first, second in zip([individual.func_objetivo], [other_individual.func_objetivo]):
            #    and_condition = and_condition and first <= second
            #    or_condition = or_condition or first < second
            #return (and_condition and or_condition)
            if all(x <= y for x, y in zip(individual.func_objetivo, other_individual.func_objetivo)) and any(x < y for x, y in zip(individual.func_objetivo, other_individual.func_objetivo)):
                return True
            return False        

    class Population:

        def __init__(self, lista_individuos):
            self.lista_individuos = lista_individuos
            self.fronts = []

        def __len__(self):
            return len(self.lista_individuos)

        def __iter__(self):
            return self.lista_individuos.__iter__()

        def extend(self, new_individuals):
            self.lista_individuos.extend(new_individuals)

        def append(self, new_individual):
            self.lista_individuos.append(new_individual)


    class Problem:

        def __init__(self, objectives, num_of_variables, variables_range, expand, same_range):
            self.num_of_objectives = len(objectives)
            self.num_of_variables = num_of_variables
            self.objectives = objectives
            self.expand = expand
            self.variables_range = []
            if same_range:
                for _ in range(num_of_variables):
                    self.variables_range.append(variables_range[0])
            else:
                self.variables_range = variables_range

    class NSGA2Utils:

        def __init__(self, problem, num_of_individuals,
                    num_of_tour_particips, tournament_prob, crossover_param, mutation_param):

            self.problem = problem
            self.num_of_individuals = num_of_individuals
            self.num_of_tour_particips = num_of_tour_particips
            self.tournament_prob = tournament_prob
            self.crossover_param = crossover_param
            self.mutation_param = mutation_param

        @staticmethod
        def fast_nondominated_sort(population):
            population.fronts = [[]]
            for individual in population.lista_individuos: # Escolhe um individuo
                individual.domination_count = 0
                individual.dominated_solutions = []
                for other_individual in population.lista_individuos: # Para cada outro individuo na populacao
                    if NSGA2.Individual.dominates(individual, other_individual): # se eu domino sobre esse outro individuo da população
                        individual.dominated_solutions.append(other_individual) # me inclui na lista de dominantes
                    elif NSGA2.Individual.dominates(other_individual, individual): # se o outro individuo dominar sobre mim
                        individual.domination_count += 1 # conta quantos outros individuos dominam sobre mim
                if individual.domination_count == 0: # se não existir nenhum outro que domine sobre mim
                    individual.rank = 0 # o meu rank é 0
                    population.fronts[0].append(individual) # sou adicionado na fronteira zero
            
            i = 0 # comecando a formação de fronteiras a partir da fronteira 0
            while len(population.fronts[i]) > 0: # enquanto existir individuos em uma fronteira
                temp = []
                for individual in population.fronts[i]: # Escolhe um individuo de uma fronteira
                    for other_individual in individual.dominated_solutions: # Para cada um dos individuos que eu domino
                        other_individual.domination_count -= 1 # diminiu 1 da quantidade de individuos no qual esse outro domina (me retirando da contagem)
                        if other_individual.domination_count == 0: # se não existir nenhum outro que domine sobre ele (se apenas eu domino sobre ele)
                            other_individual.rank = i + 1 # seu rank é a próxima fronteira
                            temp.append(other_individual) # temp após rodar uma fronteira terá os indivíduos da população que são dominados por i individuos
                i = i + 1 # avança para a próxima fronteira
                population.fronts.append(temp) # monta a população da fronteira

        def calculate_crowding_distance(self, front):
            if len(front) > 0: # se existir indivíduos nessa fronteira
                solutions_num = len(front) # conta quantos individuos tem
                for individual in front: # para cada um deles
                    individual.crowding_distance = 0 # a distancia crowding é 0

                for m in range(len(front[0].func_objetivo)): # para cada função objetivo do individuo
                    front.sort(key=lambda individual: individual.func_objetivo[m]) # ordena a fronteira de acordo com o valor de FO
                    front[0].crowding_distance = 10 ** 9 # a distancia crowding do individuo com menor FO é 10^9
                    front[solutions_num - 1].crowding_distance = 10 ** 9 # a distancia crowding do individuo com maior FO é 10^9
                    m_values = [individual.func_objetivo[m] for individual in front] # seleciona a FO de todos os individuos da fronteira
                    scale = max(m_values) - min(m_values) # cria uma escala igual a amplitude das FOs
                    if scale == 0: scale = 1 # se a maior FO for igual a menor FO, a amplitude é 1
                    for i in range(1, solutions_num - 1): # para cada individuo na fronteira, menos o primeiro e o último
                        front[i].crowding_distance += (front[i + 1].func_objetivo[m] - front[i - 1].func_objetivo[m]) / scale # a distancia crowding é acrescida de (FO do próximo - a FO do anterior)/amplitude

        def crowding_operator(self, individual, other_individual):
            # se o rank do primeiro é menor que o rank do segundo
            if (individual.rank < other_individual.rank) or \
                    ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)): # os ranks são iguais e a distancia crowding do primeiro é maior que a do segundo
                return 1
            else:
                return -1

        def create_children(self, population, matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs, Rio, vetor_invalidos, qual_ufmg, matriz_reducao_pontual, caminho_curso, simulacao_curso, celula_entrada_tributarios, matriz_tipo_contribuicoes):
            children = []
            while len(children) < len(population): # enquanto não se tem uma população de filhos de mesmo tamanho da população dos pais
                parent1 = self.__tournament(population) # escolhe um pai
                parent2 = self.__tournament(population) # escolhe outro pai
                while parent1 == parent2:
                    parent2 = self.__tournament(population) # escolhe outro pai
                child1, child2 = self.__crossover(parent1, parent2) # faz o crossover entre os pais, gerando dois filhos
                self.__mutate(child1) # aplica a mutação no filho 1
                self.__mutate(child2) # aplica a mutação no filho 2
                child1.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)
                child2.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)

                while not child1.isValido(Rio, numFuncao) or not child2.isValido(Rio, numFuncao):
                    if not child1.isValido(Rio, numFuncao): vetor_invalidos[1]+=1
                    if not child2.isValido(Rio, numFuncao): vetor_invalidos[1]+=1

                    child1, child2 = self.__crossover(parent1, parent2) # faz o crossover entre os pais, gerando dois filhos
                    self.__mutate(child1) # aplica a mutação no filho 1
                    self.__mutate(child2) # aplica a mutação no filho 2
                    child1.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)
                    child2.exec_QualUFMG(qual_ufmg, Rio, matriz_contribuicoes, matriz_reducao_pontual, scs, numFuncao, matriz_tipo_contribuicoes, caminho_curso, simulacao_curso, celula_entrada_tributarios)

                child1.avalia_func_objetivo(matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs) # calcula a FO do filho 1
                children.append(child1)
                child2.avalia_func_objetivo(matriz_contribuicoes, numFuncao, vetor_pesos_pontual, vetor_pesos_difusa, scs) # calcula a FO do filho 2
                children.append(child2)

            return children

        def __crossover(self, individual1, individual2):
            num_of_features = len(individual1.alelos) # conta quantos alelos o filho tem
            child1 = Cromossomo(False,num_of_features)
            child2 = Cromossomo(False,num_of_features)
            for i in range(num_of_features): # para cada alelo do filho
                beta = self.__get_beta() # calcula o beta
                
                aux = []
                aux2 = []
                
                x1 = (individual1.alelos[i][0] + individual2.alelos[i][0]) / 2 # x1 é a média entre os alelos do pai
                x2 = abs((individual1.alelos[i][0] - individual2.alelos[i][0]) / 2) # x2 é a metade da amplitude dos alelos do pai
                
                x3 = (individual1.alelos[i][1] + individual2.alelos[i][1]) / 2 # x1 é a média entre os alelos do pai
                x4 = abs((individual1.alelos[i][1] - individual2.alelos[i][1]) / 2) # x2 é a metade da amplitude dos alelos do pai
                
                aux = [x1 + beta * x2, x3 + beta * x4]
                aux2 = [x1 - beta * x2, x3 - beta * x4]
                
                child1.alelos.append(aux) 
                child2.alelos.append(aux2)

            return child1, child2

        def __get_beta(self):
            u = random.random()
            if u <= 0.5:
                return (2 * u) ** (1 / (self.crossover_param + 1))
            return (2 * (1 - u)) ** (-1 / (self.crossover_param + 1))

        def __mutate(self, child):
            num_of_features = len(child.alelos) # conta quantos alelos tem o filho
            for gene in range(num_of_features): # para cada alelo no filho
                u, delta = self.__get_delta() # calcula o delta

                if u < 0.5:
                    child.alelos[gene][0] += delta * (child.alelos[gene][0] - self.problem.variables_range[0][0][gene]) # o alelo do filho é acrescido de delta*(alelo-min_range)
                    child.alelos[gene][1] += delta * (child.alelos[gene][1] - self.problem.variables_range[1][0]) # o alelo do filho é acrescido de delta*(alelo-min_range)
                else:
                    child.alelos[gene][0] += delta * (self.problem.variables_range[0][1] - child.alelos[gene][0]) # o alelo do filho é acrescido de delta*(max_range-alelo)
                    child.alelos[gene][1] += delta * (self.problem.variables_range[1][1] - child.alelos[gene][1]) # o alelo do filho é acrescido de delta*(max_range-alelo)
                
                if child.alelos[gene][0] < self.problem.variables_range[0][0][gene]: # se o alelo for menor que min_range
                    child.alelos[gene][0] = self.problem.variables_range[0][0][gene] # ele será o min_range
                elif child.alelos[gene][0] > self.problem.variables_range[0][1]: # se o alelo for maior que max_range
                    child.alelos[gene][0] = self.problem.variables_range[0][1] # ele será o max_range

                if child.alelos[gene][1] < self.problem.variables_range[1][0]: # se o alelo for menor que min_range
                    child.alelos[gene][1] = self.problem.variables_range[1][0] # ele será o min_range
                elif child.alelos[gene][1] > self.problem.variables_range[1][1]: # se o alelo for maior que max_range
                    child.alelos[gene][1] = self.problem.variables_range[1][1] # ele será o max_range

        def __get_delta(self):
            u = random.random()
            if u < 0.5:
                return u, (2 * u) ** (1 / (self.mutation_param + 1)) - 1
            return u, 1 - (2 * (1 - u)) ** (1 / (self.mutation_param + 1))

        def __tournament(self, population):
            pop_indexes = [i for i in range(len(population))]
            tournament_indexes = random.sample(pop_indexes, self.num_of_tour_particips) # seleciona 2 pais aleatorios da população
            best = population[tournament_indexes[0]]
            for index in tournament_indexes: # para cada pai
                if (self.crowding_operator(population[index], best) == 1 and # se o rank do pai selecionado é menor que o do melhor, ou se os ranks são iguais e a distancia crowding do pai selecionado é maior que a do melhor 
                    self.__choose_with_prob(self.tournament_prob)): # se acontecer o torneio
                    best = population[index] # escolhe o melhor pai
            return best

        def __choose_with_prob(self, prob):
            if random.random() <= prob:
                return True
            return False
