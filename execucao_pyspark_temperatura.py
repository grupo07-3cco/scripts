import time
import tracemalloc
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    TimestampType,
    DoubleType
)
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("pipeline-sensores-temperatura")
    .master("local[*]")
    .config("spark.sql.files.maxPartitionBytes", "128mb")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.driver.memory", "2g")
    .config("spark.executor.memory", "4g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("sensor_id", IntegerType(), True),
    StructField("temperatura", DoubleType(), True),
])

def executar_pipeline_spark(arquivo_entrada):

    inicio_pipeline = time.time()

    tracemalloc.start()

    df = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(arquivo_entrada)
    )

    numero_particoes = df.rdd.getNumPartitions()

    df_processado = (
        df
        .withColumn(
            "status",
            F.when(
                F.col("temperatura") < 10,
                "critica"
            )
            .when(
                F.col("temperatura") < 20,
                "baixa"
            )
            .otherwise(
                "normal"
            )
        )
    )

    agregacao_sensor = (
        df_processado
        .groupBy("sensor_id")
        .agg(
            F.count("*").alias("quantidade_leituras"),

            F.avg("temperatura").alias("media_temperatura"),

            F.min("temperatura").alias("min_temperatura"),

            F.max("temperatura").alias("max_temperatura"),
        )
        .withColumn(
            "variacao_temperatura",
            F.col("max_temperatura")
            - F.col("min_temperatura")
        )
    )

    quantidade_registros = df_processado.count()

    quantidade_sensores = agregacao_sensor.count()

    current, peak = tracemalloc.get_traced_memory()

    pico_memoria_driver = peak / 1024 / 1024

    tracemalloc.stop()

    tempo_total = time.time() - inicio_pipeline

    print("\n")
    print("=" * 80)
    print(f"PROCESSANDO: {arquivo_entrada}")
    print("=" * 80)

    print(f"Registros: {quantidade_registros}")
    print(f"Partições: {numero_particoes}")
    print(f"Sensores: {quantidade_sensores}")
    print(
        f"Pico memória driver: "
        f"{pico_memoria_driver:.2f} MB"
    )
    print(
        f"Tempo total: "
        f"{tempo_total:.2f} segundos"
    )

    return {
        "arquivo": arquivo_entrada,
        "registros": quantidade_registros,
        "particoes": numero_particoes,
        "sensores": quantidade_sensores,
        "pico_memoria_driver": pico_memoria_driver,
        "tempo_total": tempo_total
    }

spark_100k = executar_pipeline_spark(
    "leituras_100k.csv"
)

spark_1m = executar_pipeline_spark(
    "leituras_1m.csv"
)

spark_5m = executar_pipeline_spark(
    "leituras_5m.csv"
)

tabela_spark = pd.DataFrame({
    "Tamanho": [
        "100k",
        "1M",
        "5M"
    ],

    "Registros": [
        spark_100k["registros"],
        spark_1m["registros"],
        spark_5m["registros"]
    ],

    "Partições": [
        spark_100k["particoes"],
        spark_1m["particoes"],
        spark_5m["particoes"]
    ],

    "Sensores": [
        spark_100k["sensores"],
        spark_1m["sensores"],
        spark_5m["sensores"]
    ],

    "Memória Driver (MB)": [
        spark_100k["pico_memoria_driver"],
        spark_1m["pico_memoria_driver"],
        spark_5m["pico_memoria_driver"]
    ],

    "Tempo Spark (s)": [
        spark_100k["tempo_total"],
        spark_1m["tempo_total"],
        spark_5m["tempo_total"]
    ]
})

print("\n")
print("=" * 100)
print("TABELA DE RESULTADOS — PYSPARK")
print("=" * 100)

print(
    tabela_spark.to_string(index=False)
)

spark.stop()