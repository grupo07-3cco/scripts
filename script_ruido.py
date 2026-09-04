import csv
import math
import random
from datetime import datetime, timedelta

TAXA_AMOSTRAGEM = 16000       # 16 kHz
AMOSTRAS_POR_LEITURA = 1024   # tamanho do bloco de áudio

def simular_inmp441(nivel_ruido):
    """
    Simula uma leitura do INMP441.

    O sensor real enviaria amostras digitais através do I2S.
    Aqui geramos essas amostras artificialmente.

    nivel_ruido:
        intensidade do sinal simulado.
    """

    amostras = []

    for _ in range(AMOSTRAS_POR_LEITURA):

        # Ruído ambiente simulado
        amostra = random.gauss(0, nivel_ruido)

        # Simula uma amostra digital de áudio
        amostra = int(amostra)

        # Limite de uma amostra de áudio de 16 bits
        amostra = max(-32768, min(32767, amostra))

        amostras.append(amostra)

    return amostras

def calcular_rms(amostras):

    soma = 0

    for amostra in amostras:
        soma += amostra ** 2

    rms = math.sqrt(soma / len(amostras))

    return rms

def calcular_db(rms):

    # Referência utilizada apenas para a simulação
    referencia = 500

    if rms <= 0:
        return 0

    db = 20 * math.log10(rms / referencia)

    return db

def classificar_ruido(db):

    if db < 10:
        return "Muito baixo"

    elif db < 30:
        return "Baixo"

    elif db < 50:
        return "Moderado"

    elif db < 70:
        return "Alto"

    else:
        return "Muito alto"

def gerar_coletas(numero_coletas, intervalo):
    coletas = []

    data_hora = datetime.now()

    for i in range(numero_coletas):

        nivel_ruido = random.choice([
            100,    # silêncio
            300,    # ambiente tranquilo
            700,    # conversa
            1500,   # ambiente movimentado
            3000,   # ambiente barulhento
            5000    # ruído intenso
        ])

        amostras = simular_inmp441(nivel_ruido)

        rms = calcular_rms(amostras)

        db = calcular_db(rms)

        classificacao = classificar_ruido(db)

        coleta = {
            "numero": i + 1,
            "data_hora": data_hora,
            "db": round(db, 2),
            "classificacao": classificacao
        }

        coletas.append(coleta)

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
    intervalo=0.5
)

exportar_csv(coletas, "leituras_ruido.csv")

for coleta in coletas:
    print(
        f"Coleta {coleta['numero']:03d} | "
        f"{coleta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')} → "
        f"dB: {coleta['db']:.2f} ({coleta['classificacao']})"
    )
