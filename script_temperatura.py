import random

def gerar_coletas(numero_coletas, temp_inicial, variacao_maxima, limite_min, limite_max):
    coletas = []
        
    temp_atual = temp_inicial
    coletas.append(round(temp_atual, 1))
    
    for _ in range(numero_coletas - 1):
        variacao = random.uniform(-variacao_maxima, variacao_maxima)
        temp_atual += variacao
        
        if temp_atual < limite_min:
            temp_atual = limite_min
        elif temp_atual > limite_max:
            temp_atual = limite_max
            
        coletas.append(round(temp_atual, 1))

    return coletas


def simular(temp_inicial_global, coletas):
    print("---------- INICIANDO SIMULAÇÕES DE COLETA ----------\n")
    
    for i in range(coletas):
        variacao_maxima = random.uniform(0.1, 0.6)
        
        limite_min = temp_inicial_global - random.uniform(3.0, 6.0)
        limite_max = temp_inicial_global + random.uniform(3.0, 6.0)
        
        resultado = gerar_coletas(100, temp_inicial_global, variacao_maxima, limite_min, limite_max)
        
        print(f"Simulação #{i+1:03d} | Variação Máx: {variacao_maxima:.2f}°C | Limites: [{limite_min:.1f}°C a {limite_max:.1f}°C]")
        print(f"  -> Histórico: {resultado}\n")

simular(25.0, 100)

