import math
import random
import time

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

def iniciar_simulacao():

    print("==============================================")
    print("     SIMULADOR DE SENSOR INMP441")
    print("==============================================")
    print(f"Taxa de amostragem: {TAXA_AMOSTRAGEM} Hz")
    print(f"Amostras por leitura: {AMOSTRAS_POR_LEITURA}")
    print("==============================================\n")

    while True:

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

        print(
            f"RMS: {rms:8.2f} | "
            f"dB relativo: {db:6.2f} | "
            f"Ambiente: {classificacao}"
        )

        time.sleep(0.5)

iniciar_simulacao()