# -*- coding: utf-8 -*-
"""
Servicio de Análisis Cuantitativo y Métricas
--------------------------------------------
Realiza cálculos estadísticos y métricas de calidad sobre el set de datos.
"""

import decimal
from decimal import Decimal
from typing import List, Dict
import pandas as pd
import numpy as np

from src.core.models import MetricasReporte, EstadisticaNumerica

# Configurar precisión decimal
decimal.getcontext().prec = 28


def calcular_metricas_generales(df: pd.DataFrame, filas_vacias_eliminadas: int) -> MetricasReporte:
    """
    Calcula las métricas principales de completitud y estructura del set de datos:
    - Total de registros y columnas.
    - Cantidad total de celdas vacías (nulos).
    - Cantidad de filas duplicadas.
    - Detección de columnas numéricas y categóricas.
    - Identificación de las 3 columnas con más nulos.
    """
    total_registros = len(df)
    total_columnas = len(df.columns)

    # Calcular celdas vacías (NaN)
    total_vacios = int(df.isnull().sum().sum())

    # Calcular filas duplicadas
    total_duplicados = int(df.duplicated().sum())

    # Clasificación de columnas
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    columnas_categoricas = df.select_dtypes(
        exclude=[np.number]).columns.tolist()

    # Columnas críticas con mayor cantidad de nulos
    vacios_por_columna = df.isnull().sum()
    columnas_con_mas_nulos = (
        vacios_por_columna[vacios_por_columna > 0]
        .sort_values(ascending=False)
        .head(3)
        .to_dict()
    )

    return MetricasReporte(
        total_registros=total_registros,
        total_columnas=total_columnas,
        total_vacios=total_vacios,
        total_duplicados=total_duplicados,
        columnas_numericas=columnas_numericas,
        columnas_categoricas=columnas_categoricas,
        filas_vacias_eliminadas=filas_vacias_eliminadas,
        columnas_con_mas_nulos=columnas_con_mas_nulos
    )


def calcular_estadisticas_numericas(df: pd.DataFrame, columnas_numericas: List[str]) -> List[EstadisticaNumerica]:
    """
    Calcula resúmenes descriptivos (Suma, Promedio, Mínimo, Máximo) de alta precisión (Decimal)
    para las columnas numéricas indicadas.
    """
    estadisticas = []

    for col in columnas_numericas:
        serie = df[col].dropna()
        if serie.empty:
            continue

        # Calcular agregaciones
        suma_val = float(serie.sum())
        promedio_val = float(serie.mean())
        min_val = float(serie.min())
        max_val = float(serie.max())

        # Convertir a Decimal para garantizar 100% de precisión matemática contable
        dec_suma = Decimal(str(suma_val))
        dec_promedio = Decimal(str(promedio_val))
        dec_min = Decimal(str(min_val))
        dec_max = Decimal(str(max_val))

        estadisticas.append(
            EstadisticaNumerica(
                columna=col,
                suma=dec_suma,
                promedio=dec_promedio,
                minimo=dec_min,
                maximo=dec_max
            )
        )

    return estadisticas
