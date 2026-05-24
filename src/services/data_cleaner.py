# -*- coding: utf-8 -*-
"""
Servicio de Limpieza de Datos
-----------------------------
Implementa los casos de uso para la depuración y normalización de DataFrames.
"""

from typing import Tuple
import pandas as pd
import numpy as np
from src.core.models import LimpiezaInfo


def limpiar_datos_basicos(df: pd.DataFrame) -> Tuple[pd.DataFrame, LimpiezaInfo]:
    """
    Realiza la limpieza y normalización del set de datos:
    - Remueve filas que estén completamente vacías.
    - Recorta los espacios en blanco innecesarios en todas las celdas de texto.
    - Sanea y normaliza las cabeceras/columnas eliminando caracteres inválidos.
    """
    total_filas_original = len(df)

    # 1. Eliminar filas que estén completamente vacías (todas sus celdas son NaN)
    df_limpio = df.dropna(how='all')
    filas_vacias_eliminadas = total_filas_original - len(df_limpio)

    # 2. Limpiar espacios innecesarios en celdas de tipo texto (stripping)
    # Usamos df.map (soportado en pandas moderno)
    df_limpio = df_limpio.map(lambda x: x.strip() if isinstance(x, str) else x)

    # 3. Normalizar nombres de columnas: strip, remover saltos de línea y formatear
    columnas_originales = df_limpio.columns.tolist()
    columnas_limpias = []
    for col in columnas_originales:
        col_str = str(col).strip().replace('\n', ' ').replace('\r', '')
        if not col_str:
            col_str = f"Columna_Sin_Nombre_{len(columnas_limpias) + 1}"
        columnas_limpias.append(col_str)

    df_limpio.columns = columnas_limpias

    info_limpieza = LimpiezaInfo(
        filas_originales=total_filas_original,
        filas_vacias_eliminadas=filas_vacias_eliminadas,
        filas_limpias=len(df_limpio),
        columnas_normalizadas=len(columnas_limpias)
    )

    return df_limpio, info_limpieza
