import csv
import random
from datetime import datetime, timedelta


def gerar_coletas(numero_coletas, bpm_inicial, variacao_maxima, intervalo, limite_min, limite_max):
    coletas = []

    data_hora = datetime.now()
    bpm_atual = bpm_inicial

    for i in range(numero_coletas):
        coleta = {
            "numero": i + 1,
            "data_hora": data_hora,
            "bpm": round(bpm_atual, 1)
        }

        coletas.append(coleta)

        variacao = random.uniform(
            -variacao_maxima,
            variacao_maxima
        )

        bpm_atual += variacao

        if bpm_atual < limite_min:
            bpm_atual = limite_min

        elif bpm_atual > limite_max:
            bpm_atual = limite_max

        data_hora += timedelta(seconds=intervalo)

    return coletas


def exportar_csv(coletas, nome_arquivo):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        campos = list(coletas[0].keys())
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(coletas)


def simular(bpm_inicial_global, numero_simulacoes):

    print("---------- INICIANDO SIMULAÇÕES DO SENSOR CARDÍACO ----------\n")

    todas_coletas = []

    for i in range(numero_simulacoes):

        variacao_maxima = random.uniform(1.0, 4.0)

        limite_min = bpm_inicial_global - random.uniform(10, 20)
        limite_max = bpm_inicial_global + random.uniform(10, 20)

        resultado = gerar_coletas(
            100,
            bpm_inicial_global,
            variacao_maxima,
            3,
            limite_min,
            limite_max
        )

        valores = [coleta["bpm"] for coleta in resultado]

        bpm_medio = sum(valores) / len(valores)
        bpm_minimo = min(valores)
        bpm_maximo = max(valores)

        print(
            f"Simulação #{i + 1:03d} | "
            f"Variação Máx: {variacao_maxima:.2f} BPM | "
            f"Limites: [{limite_min:.1f} a {limite_max:.1f} BPM]"
        )

        for coleta in resultado:
            print(
                f"  Coleta {coleta['numero']:03d} | "
                f"{coleta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')} → "
                f"BPM: {coleta['bpm']:.1f}"
            )

        print(
            f"  -> BPM médio: {bpm_medio:.1f}"
        )

        print(
            f"  -> BPM mínimo: {bpm_minimo:.1f}"
        )

        print(
            f"  -> BPM máximo: {bpm_maximo:.1f}\n"
        )

        for coleta in resultado:
            todas_coletas.append({"simulacao": i + 1, **coleta})

    exportar_csv(todas_coletas, "leituras_frequencia_cardiaca.csv")


simular(75, 2000)
