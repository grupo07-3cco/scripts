import random


def gerar_coletas(numero_coletas, bpm_inicial, variacao_maxima, limite_min, limite_max):
    coletas = []

    bpm_atual = bpm_inicial
    coletas.append(round(bpm_atual, 1))

    for _ in range(numero_coletas - 1):

        variacao = random.uniform(
            -variacao_maxima,
            variacao_maxima
        )

        bpm_atual += variacao

        if bpm_atual < limite_min:
            bpm_atual = limite_min

        elif bpm_atual > limite_max:
            bpm_atual = limite_max

        coletas.append(round(bpm_atual, 1))

    return coletas


def simular(bpm_inicial_global, numero_simulacoes):

    print("---------- INICIANDO SIMULAÇÕES DO SENSOR CARDÍACO ----------\n")

    for i in range(numero_simulacoes):

        variacao_maxima = random.uniform(1.0, 4.0)

        limite_min = bpm_inicial_global - random.uniform(10, 20)
        limite_max = bpm_inicial_global + random.uniform(10, 20)

        resultado = gerar_coletas(
            100,
            bpm_inicial_global,
            variacao_maxima,
            limite_min,
            limite_max
        )

        bpm_medio = sum(resultado) / len(resultado)
        bpm_minimo = min(resultado)
        bpm_maximo = max(resultado)

        print(
            f"Simulação #{i + 1:03d} | "
            f"Variação Máx: {variacao_maxima:.2f} BPM | "
            f"Limites: [{limite_min:.1f} a {limite_max:.1f} BPM]"
        )

        print(
            f"  -> BPM médio: {bpm_medio:.1f}"
        )

        print(
            f"  -> BPM mínimo: {bpm_minimo:.1f}"
        )

        print(
            f"  -> BPM máximo: {bpm_maximo:.1f}"
        )

        print(
            f"  -> Histórico: {resultado}\n"
        )


simular(75, 2000)
