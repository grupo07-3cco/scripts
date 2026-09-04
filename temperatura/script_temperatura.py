import random
import pandas as pd


def gerar_coletas(
    numero_coletas,
    temp_inicial,
    variacao_maxima,
    limite_min,
    limite_max
):
    coletas = []

    temp_atual = temp_inicial
    coletas.append(round(temp_atual, 1))

    for _ in range(numero_coletas - 1):

        variacao = random.uniform(
            -variacao_maxima,
            variacao_maxima
        )

        temp_atual += variacao

        if temp_atual < limite_min:
            temp_atual = limite_min

        elif temp_atual > limite_max:
            temp_atual = limite_max

        coletas.append(round(temp_atual, 1))

    return coletas


def gerar_dataset(numero_registros, arquivo):

    registros = []

    sensores = 100

    temperaturas = {}

    for sensor_id in range(1, sensores + 1):

        temperatura_inicial = random.uniform(20, 30)

        variacao_maxima = random.uniform(0.1, 0.6)

        limite_min = temperatura_inicial - random.uniform(3, 6)
        limite_max = temperatura_inicial + random.uniform(3, 6)

        temperaturas[sensor_id] = {
            "atual": temperatura_inicial,
            "variacao": variacao_maxima,
            "min": limite_min,
            "max": limite_max
        }

    for i in range(numero_registros):

        sensor_id = random.randint(1, sensores)
        sensor = temperaturas[sensor_id]

        temperatura = gerar_coletas(
            1,
            sensor["atual"],
            sensor["variacao"],
            sensor["min"],
            sensor["max"]
        )[0]

        sensor["atual"] = temperatura

        registros.append({
            "timestamp": pd.Timestamp.now(),
            "sensor_id": sensor_id,
            "temperatura": temperatura,
        })

    df = pd.DataFrame(registros)

    df.to_csv(
        arquivo,
        index=False
    )

    print(
        f"{arquivo} gerado com "
        f"{numero_registros:,} registros."
    )


gerar_dataset(
    100_000,
    "leituras_100k.csv"
)

gerar_dataset(
    1_000_000,
    "leituras_1m.csv"
)

gerar_dataset(
    5_000_000,
    "leituras_5m.csv"
)
