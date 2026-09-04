import csv
import random
from datetime import datetime, timedelta


def gerar_coletas(numero_coletas, temp_inicial, variacao_maxima, intervalo, limite_min, limite_max):
    coletas = []

    data_hora = datetime.now()
    temp_atual = temp_inicial

    for i in range(numero_coletas):
        coleta = {
            "numero": i + 1,
            "data_hora": data_hora,
            "temperatura": round(temp_atual, 1)
        }

        coletas.append(coleta)

        variacao = random.uniform(-variacao_maxima, variacao_maxima)
        temp_atual += variacao

        if temp_atual < limite_min:
            temp_atual = limite_min

        elif temp_atual > limite_max:
            temp_atual = limite_max

        data_hora += timedelta(seconds=intervalo)

    return coletas


def exportar_csv(coletas, nome_arquivo):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        campos = list(coletas[0].keys())
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(coletas)


def simular(temp_inicial_global, numero_simulacoes):
    print("---------- INICIANDO SIMULAÇÕES DE COLETA ----------\n")

    todas_coletas = []

    for i in range(numero_simulacoes):
        variacao_maxima = random.uniform(0.1, 0.6)

        limite_min = temp_inicial_global - random.uniform(3.0, 6.0)
        limite_max = temp_inicial_global + random.uniform(3.0, 6.0)

        resultado = gerar_coletas(100, temp_inicial_global, variacao_maxima, 3, limite_min, limite_max)

        print(f"Simulação #{i+1:03d} | Variação Máx: {variacao_maxima:.2f}°C | Limites: [{limite_min:.1f}°C a {limite_max:.1f}°C]")

        for coleta in resultado:
            print(
                f"  Coleta {coleta['numero']:03d} | "
                f"{coleta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')} → "
                f"Temp: {coleta['temperatura']:.1f}°C"
            )

        print()

        for coleta in resultado:
            todas_coletas.append({"simulacao": i + 1, **coleta})

    exportar_csv(todas_coletas, "leituras_temperatura.csv")

simular(25.0, 100)
