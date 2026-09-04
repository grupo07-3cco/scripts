import csv
import random
from datetime import datetime, timedelta


def gerar_coletas(numero_coletas, valor_inicial, variacao_maxima, intervalo, limite_min, limite_max):
    coletas = []

    data_hora = datetime.now()
    spo2_atual = valor_inicial

    for i in range(numero_coletas):
        coleta = {
            "numero": i + 1,
            "data_hora": data_hora,
            "spo2": round(spo2_atual, 1)
        }

        coletas.append(coleta)

        variacao = random.uniform(-variacao_maxima, variacao_maxima)
        spo2_atual += variacao

        if spo2_atual < limite_min:
            spo2_atual = limite_min
        elif spo2_atual > limite_max:
            spo2_atual = limite_max

        data_hora += timedelta(seconds=intervalo)

    return coletas


def exportar_csv(coletas, nome_arquivo):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        campos = list(coletas[0].keys())
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(coletas)


coletas = gerar_coletas(
    numero_coletas=100,
    valor_inicial=93,
    variacao_maxima=0.5,
    intervalo=3,
    limite_min=91,
    limite_max=95
)

exportar_csv(coletas, "leituras_oxigenio.csv")

for coleta in coletas:
    print(
        f"Coleta {coleta['numero']:03d} | "
        f"{coleta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')} → "
        f"SpO2: {coleta['spo2']:.1f}%"
    )
