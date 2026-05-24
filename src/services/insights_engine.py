# -*- coding: utf-8 -*-
"""
Servicio del Motor de Conclusiones (Insights Engine)
----------------------------------------------------
Redacta observaciones y recomendaciones técnicas automáticas de negocio
según el comportamiento y la calidad física de los datos cargados.
"""

from typing import List
from src.core.models import MetricasReporte, EstadisticaNumerica
from src.config import WARNING_COLOR


def generar_conclusiones_automaticas(metricas: MetricasReporte, estadisticas: List[EstadisticaNumerica]) -> List[str]:
    """
    Genera un listado de conclusiones y observaciones automáticas en base a las
    métricas de calidad y estadísticas de precisión del dataset.
    """
    conclusiones = []
    total_filas = metricas.total_registros

    # 1. Volumen de datos
    if total_filas > 1000:
        conclusiones.append(
            f"<b>Volumen de datos alto:</b> Se analizó un set de datos mediano/grande con {total_filas} registros, "
            "lo que proporciona una base estadísticamente sólida para la toma de decisiones."
        )
    else:
        conclusiones.append(
            f"<b>Volumen de datos acotado:</b> El set contiene {total_filas} registros. Es adecuado para reportes puntuales, "
            "pero se recomienda acumular mayor historial para análisis predictivos."
        )

    # 2. Registros duplicados
    duplicados = metricas.total_duplicados
    if duplicados > 0:
        pct_dup = (duplicados / total_filas) * 100 if total_filas > 0 else 0
        conclusiones.append(
            f"<b>Registros Duplicados:</b> Se identificaron {duplicados} filas idénticas ({pct_dup:.1f}% del total). "
            f"<font color='{WARNING_COLOR.hexval()}'><b>Se recomienda validar los procesos de captura</b></font> o los IDs de registros "
            "para evitar distorsiones en las sumatorias."
        )
    else:
        conclusiones.append(
            "<b>Integridad de Registros Únicos:</b> No se detectaron registros duplicados en el set de datos. "
            "La unicidad física de los registros se encuentra en un estado óptimo (100%)."
        )

    # 3. Campos vacíos (nulos)
    nulos = metricas.total_vacios
    if nulos > 0:
        total_celdas = total_filas * metricas.total_columnas
        pct_nulos = (nulos / total_celdas) * 100 if total_celdas > 0 else 0
        nulos_info = ""
        if metricas.columnas_con_mas_nulos:
            cols = ", ".join([f"'{c}' ({n} vacíos)" for c,
                             n in metricas.columnas_con_mas_nulos.items()])
            nulos_info = f" Principalmente en: {cols}."

        conclusiones.append(
            f"<b>Campos Vacíos:</b> Existe un {pct_nulos:.1f}% de valores nulos en el lienzo ({nulos} celdas vacías).{nulos_info} "
            "Se sugiere establecer campos obligatorios en el origen para optimizar futuras cargas."
        )
    else:
        conclusiones.append(
            "<b>Completitud del Set de Datos:</b> Excelente calidad de llenado. No se encontraron valores vacíos "
            "o nulos en ninguna de las variables registradas."
        )

    # 4. Concentraciones cuantitativas
    if estadisticas:
        # Encontrar el de mayor suma y promedio
        col_mayor_suma = max(estadisticas, key=lambda x: x.suma)
        col_mayor_prom = max(estadisticas, key=lambda x: x.promedio)

        suma_formateada = f"{col_mayor_suma.suma:,.2f}"
        prom_formateado = f"{col_mayor_prom.promedio:,.2f}"

        conclusiones.append(
            f"<b>Concentración Numérica:</b> La columna con la mayor acumulación total es '{col_mayor_suma.columna}' "
            f"con un acumulado de <b>{suma_formateada}</b>. Por su parte, la columna con el valor medio más elevado "
            f"es '{col_mayor_prom.columna}' promediando <b>{prom_formateado}</b> por registro."
        )
    else:
        conclusiones.append(
            "<b>Ausencia de Columnas Métricas:</b> El archivo analizado cuenta puramente con datos cualitativos "
            "o descriptivos. Se recomienda enriquecer el set con variables cuantitativas si se requiere análisis financiero."
        )

    return conclusiones
