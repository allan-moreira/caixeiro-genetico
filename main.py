import random
import numpy as np
import copy

# Número de cidades
NUM_CIDADES = 6
POPULACAO_INICIAL = 5
GERACOES = 50
TAXA_MUTACAO = 1
TAXA_CROSSOVER = 0.8
ELITISMO = 1

melhor = [0, 3, 5, 1, 4, 2, 0]

# Geração de matriz de distâncias entre cidades (aleatória)
def gerar_matriz_distancias(n):
    """matriz = np.random.randint(10, 100, size=(n, n))
    np.fill_diagonal(matriz, 0)  # Distância de uma cidade para si mesma é 0
    return (matriz + matriz.T) // 2  # Tornar simétrica"""
    
    return np.array([[ 0, 25,  1,  1, 32, 45],
                     [25,  0, 65, 45,  1,  1],
                     [ 1, 65,  0, 39,  1, 53],
                     [ 1, 45, 39,  0, 71,  1],
                     [32,  1,  1, 71,  0, 50],
                     [45,  1, 53,  1, 50,  0]])
            

# Inicialização dos cromossomos (indivíduos)
def inicializar_populacao(tamanho_pop, num_cidades):
    return [[0] + random.sample(range(1, num_cidades), num_cidades - 1) + [0] for _ in range(tamanho_pop)]

# Avaliação da aptidão de um cromossomo
def calcular_fitness(cromossomo, matriz_distancias):
    custo = 0
    for i in range(len(cromossomo) - 1):
        custo += matriz_distancias[cromossomo[i], cromossomo[i + 1]]
    print(custo)
    return custo

# Seleção por torneio
def selecao_torneio(populacao, fitness, k=3):
    torneio = random.sample(list(zip(populacao, fitness)), k)
    return min(torneio, key=lambda x: x[1])[0]

# Crossover (ordem, Order Crossover - OX)
def crossover(pai1, pai2):
    if random.random() > TAXA_CROSSOVER:
        return pai1.copy()

    tamanho = len(pai1)
    ponto1, ponto2 = sorted(random.sample(range(1, tamanho), 2))

    filho = [0] + [-1] * (tamanho - 2) + [0]
    filho[ponto1:ponto2] = pai1[ponto1:ponto2]
    preenche = [gene for gene in pai2 if gene not in filho]
    pos = 0
    for i in range(tamanho):
        if filho[i] == -1:
            filho[i] = preenche[pos]
            pos += 1

    return filho

# Mutação (troca de posições aleatórias)
def mutacao(cromossomo, n = 1):
    if random.random() < TAXA_MUTACAO:
        for i in range(n):
            idx1, idx2 = random.sample(range(1, len(cromossomo) - 1), 2)
            cromossomo[idx1], cromossomo[idx2] = cromossomo[idx2], cromossomo[idx1]
    return cromossomo

# Algoritmo Evolutivo
def algoritmo_evolutivo(matriz_distancias):
    # Inicialização
    populacao = inicializar_populacao(POPULACAO_INICIAL, NUM_CIDADES)
    
    for geracao in range(GERACOES):
        # Avaliar a aptidão
        fitness = [calcular_fitness(ind, matriz_distancias) for ind in populacao]
        nova_populacao = []
        print(populacao)

        # Elitismo: manter os melhores
        elites = sorted(zip(populacao, fitness), key=lambda x: x[1])[:ELITISMO]
        print("elites: {}".format(elites))
        nova_populacao.extend([elite[0][:] for elite in elites])
        
        # Multipla mutação do pior
        pior = sorted(zip(populacao, fitness), key=lambda x: x[1])[-1]
        print(pior)
        nova_populacao.append(mutacao(pior[0], 2)[:])
        
        print("nova população")
        print(nova_populacao)

        # Seleção, cruzamento e mutação
        while len(nova_populacao) < POPULACAO_INICIAL:
            ind = selecao_torneio(populacao, fitness)
            ind = mutacao(ind)
            nova_populacao.append(ind)
        
        print("nova população")
        print(nova_populacao)
        populacao = nova_populacao
        sorted(populacao)

        # Melhor solução da geração
        melhor_fitness = min(fitness)
        melhor_cromossomo = populacao[fitness.index(melhor_fitness)]
        print(f"Geração {geracao + 1}: Melhor solução = {melhor_cromossomo}, Fitness = {melhor_fitness}")

    # Melhor solução final
    fitness_final = [calcular_fitness(ind, matriz_distancias) for ind in populacao]
    melhor_cromossomo = populacao[fitness_final.index(max(fitness_final))]
    return melhor_cromossomo, min(fitness_final)

# Execução
if _name_ == "_main_":
    matriz_distancias = gerar_matriz_distancias(NUM_CIDADES)
    print("Matriz de Distâncias:")
    print(matriz_distancias)

    melhor_rota, melhor_custo = algoritmo_evolutivo(matriz_distancias)
    print("\nMelhor Rota Encontrada:", melhor_rota)
    print("Custo da Melhor Rota:", melhor_custo)