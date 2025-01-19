import itertools

def calcular_custo_rota(rota, matriz_distancias):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz_distancias[rota[i]][rota[i + 1]]
    # Retorna à cidade 0
    custo += matriz_distancias[rota[-1]][rota[0]]
    return custo

def caixeiro_viajante(matriz_distancias):
    num_cidades = len(matriz_distancias)
    # Gera todas as permutações das cidades, excluindo a cidade 0
    cidades = list(range(1, num_cidades))
    melhores_rota = None
    menor_custo = float('inf')
    
    # Gera todas as permutações das cidades
    for permutacao in itertools.permutations(cidades):
        # A cidade 0 é sempre a primeira e a última
        rota = [0] + list(permutacao) + [0]
        custo = calcular_custo_rota(rota, matriz_distancias)
        
        # Verifica se a rota encontrada tem o menor custo
        if custo < menor_custo:
            menor_custo = custo
            melhores_rota = rota
    
    return melhores_rota, menor_custo
