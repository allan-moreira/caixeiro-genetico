import random
import numpy as np

# Inicialização de Constantes
NUM_CIDADES = 6
POPULACAO_INICIAL = 5
GERACOES = 50
TAXA_MUTACAO = 0.8

# Geração de matriz de distâncias entre cidades (aleatória)
def gerar_matriz_distancias(n):
    matriz = np.random.randint(10, 100, size=(n, n))
    np.fill_diagonal(matriz, 0)  # Distância de uma cidade para si mesma é 0
    return (matriz + matriz.T) // 2  # Tornar simétrica

# Inicialização dos cromossomos (indivíduos)
def inicializar_populacao(tamanho_pop, num_cidades):
    return [[0] + random.sample(range(1, num_cidades), num_cidades - 1) + [0] for _ in range(tamanho_pop)] # Cria vetor que começa e termina em 0 e possui o numero de cada cidade sem repetição

# Avaliação da aptidão de um cromossomo
def calcular_fitness(cromossomo, matriz_distancias):
    custo = 0
    for i in range(len(cromossomo) - 1):
        custo += matriz_distancias[cromossomo[i], cromossomo[i + 1]] # Função a ser minimizada
    return custo

# Seleção por deterministica
def selecao_deterministica(populacao):
    return random.sample(populacao, 2) # Escolhe dois indivíduos aleatórios

def elitismo(populacao, fitness):
    return min(zip(populacao, fitness), key=lambda x: x[1])[0] # Escolhe o melhor indivíduo da geração (menor distancia)

# Crossover
def crossover(pai1, pai2):
    tamanho = len(pai1)
    divisao = int(0.7 * tamanho) # Cria uma divisão de aproximadamente 70% do tamanho do cromossomo

    filho = tamanho * [0] 
    filho[:divisao] = pai1[:divisao] # Cria um filho que recebe a primeira metade do pai 1

    preenche = [gene for gene in pai2 if gene not in filho] # cria vetor das cidades que o filho ainda não tem em relaçao ao pai 2

    for i in range(divisao, tamanho - 1): # Substitui os 0's pelas cidades do pai 2
        filho[i] = preenche.pop(0)

    print(f"            Crossover entre {pai1} e {pai2} tendo como filho {filho}")

    return filho

# Mutação (troca de posições aleatórias)
def mutacao(individuo):
    mutado = individuo[:] # Cria uma cópia profunda

    if random.random() <= TAXA_MUTACAO: 
        idx1, idx2 = random.sample(range(1, len(individuo) - 1), 2)
        mutado[idx1], mutado[idx2] = mutado[idx2], mutado[idx1] # Troca duas posições aleatórias do cromossomo de lugar

        print(f"                Mutação do individuo {individuo} para {mutado}")

    return mutado

def imprime_geracao(resultado):
    for individuo in resultado:
        print(f"        Individuo: {individuo[0]} -> Distancia percorrida: {individuo[1]}")

# Algoritmo Evolutivo
def algoritmo_evolutivo(matriz_distancias):
    # Inicialização
    populacao = inicializar_populacao(POPULACAO_INICIAL, NUM_CIDADES)
    
    for geracao in range(GERACOES):
        # Avaliar a aptidão
        fitness = [calcular_fitness(individuo, matriz_distancias) for individuo in populacao]

        # Melhor solução da geração
        resultados = sorted(list(zip(populacao, fitness)), key = lambda x: x[1])
        melhor_fitness = resultados[0][1]
        melhor_cromossomo = resultados[0][0]

        # Exibição da geração
        print(f"\nGeração {geracao}: Melhor solução = {melhor_cromossomo}, Fitness = {melhor_fitness}")
        imprime_geracao(resultados)

        nova_populacao = []

        print(f"\n        Gerando nova população:")

        # Elitismo: mantém o melhor indivíduo para a próxima geração
        elite = elitismo(populacao, fitness)
        nova_populacao.extend([elite[:]])

        # Seleção, cruzamento e mutação
        while len(nova_populacao) < POPULACAO_INICIAL:
            pai1, pai2 = selecao_deterministica(populacao) # Seleciona
            individuo = crossover(pai1, pai2) # Cruza

            if random.random() <= TAXA_MUTACAO:
                individuo = mutacao(individuo) # Muta

            nova_populacao.append(individuo)
        
        populacao = nova_populacao

    # Melhor solução final
    fitness_final = [calcular_fitness(ind, matriz_distancias) for ind in populacao] 
    resultados = sorted(list(zip(populacao, fitness_final)), key = lambda x: x[1])
    melhor_fitness = resultados[0][1]
    melhor_cromossomo = resultados[0][0]

    # Exibição da última geração
    print(f"\nGeração {GERACOES}: Melhor solução = {melhor_cromossomo}, Fitness = {melhor_fitness}")
    imprime_geracao(resultados)

    return melhor_cromossomo, melhor_fitness

# Execução
if __name__ == "__main__":
    matriz_distancias = gerar_matriz_distancias(NUM_CIDADES)
    print("Matriz de Distâncias:\n", matriz_distancias)

    melhor_rota, melhor_custo = algoritmo_evolutivo(matriz_distancias)
    print("\nMelhor Rota Encontrada:", melhor_rota)
    print("Custo da Melhor Rota:", melhor_custo)