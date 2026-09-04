import random
from datetime import datetime, timedelta


def gerar_coletas(numero_coletas, valor_inicial, variacao_maxima, intervalo):
    coletas = []

    data_hora = datetime.now()
    umid_atual = valor_inicial

    for i in range(numero_coletas):
        coleta = {
            "numero": i + 1,
            "data_hora": data_hora,
            "umidade": round(umid_atual, 1)
        }

        coletas.append(coleta)

        variacao = random.uniform(-variacao_maxima, variacao_maxima)
        umid_atual += variacao

        data_hora += timedelta(seconds=intervalo)

    return coletas


coletas = gerar_coletas(
    numero_coletas=100,
    valor_inicial=75,
    variacao_maxima=0.5,
    intervalo=3
)

for coleta in coletas:
    print(
        f"Coleta {coleta['numero']:03d} | "
        f"{coleta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')} → "
        f"{coleta['umidade']:.1f}%"
    )