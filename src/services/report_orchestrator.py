# -*- coding: utf-8 -*-
"""
Servicio Orquestador de Reportes (Caso de Uso Principal)
--------------------------------------------------------
Orquesta la lectura, limpieza, cálculo analítico y maquetado físico del PDF.
"""

from pathlib import Path
import pandas as pd
import sys

from src.infrastructure import (
    log_info, log_success, log_warning, log_error, log_step,
    validar_existencia, crear_carpeta_si_no_existe, obtener_tamano_legible,
    generar_ruta_pdf_unica, construir_reporte_pdf
)
from src.services.data_cleaner import limpiar_datos_basicos
from src.services.data_analyzer import calcular_metricas_generales, calcular_estadisticas_numericas
from src.services.insights_engine import generar_conclusiones_automaticas


def ejecutar_pipeline_reporte(ruta_entrada: str, carpeta_salida: str) -> None:
    """
    Orquesta el pipeline completo de análisis de datos y generación de reportes PDF:
    1. Valida el archivo de entrada.
    2. Carga los datos (Excel / CSV) de forma segura.
    3. Realiza la limpieza básica de registros y columnas.
    4. Analiza métricas de completitud y estadísticas descriptivas (Decimal).
    5. Genera observaciones de negocio dinámicas (Insights).
    6. Valida la carpeta de salida y resuelve colisiones de nombres de archivos.
    7. Genera y compila físicamente el reporte PDF corporativo.
    """
    ruta_archivo = Path(ruta_entrada)
    path_salida = Path(carpeta_salida)

    log_step(f"Iniciando procesamiento para el archivo: '{ruta_archivo.name}'")

    try:
        # Paso 1: Validar archivo de entrada
        log_step("Paso 1: Validando archivo de entrada...")
        if not validar_existencia(ruta_archivo):
            raise FileNotFoundError(
                "El archivo de entrada no es válido o no existe en la ruta provista.")

        extension = ruta_archivo.suffix.lower()
        if extension not in ['.xlsx', '.xls', '.csv']:
            raise ValueError(
                f"Extensión de archivo no soportada ({extension}). Use: .xlsx, .xls o .csv")

        log_info(f"Validando archivo de entrada: {ruta_archivo.name}...")
        log_success("Archivo de entrada validado correctamente.")

        # Paso 2: Leer el archivo Excel o CSV
        log_step("Paso 2: Leyendo datos del Excel/CSV...")
        log_info("Leyendo datos del archivo...")

        if extension == '.csv':
            try:
                df_crudo = pd.read_csv(ruta_archivo, encoding='utf-8')
            except UnicodeDecodeError:
                df_crudo = pd.read_csv(ruta_archivo, encoding='latin1')
        else:
            df_crudo = pd.read_excel(ruta_archivo)

        if df_crudo.empty:
            raise ValueError(
                "El archivo cargado está vacío (no contiene registros).")

        log_success(
            f"Datos leídos con éxito. Registros iniciales: {df_crudo.shape[0]} | Columnas: {df_crudo.shape[1]}")

        # Paso 3: Limpiar datos
        log_step("Paso 3: Limpiando datos...")
        log_info("Limpiando datos...")
        df_limpio, limpieza_info = limpiar_datos_basicos(df_crudo)
        log_success(
            f"Limpieza completada. Filas vacías eliminadas: {limpieza_info.filas_vacias_eliminadas}")

        # Paso 4: Analizar datos y calcular estadísticas
        log_step("Paso 4: Calculando métricas y análisis cuantitativo...")
        log_info("Calculando métricas generales...")
        metricas = calcular_metricas_generales(
            df_limpio, limpieza_info.filas_vacias_eliminadas)

        log_info("Analizando estadísticas de columnas numéricas...")
        estadisticas = calcular_estadisticas_numericas(
            df_limpio, metricas.columnas_numericas)

        if not metricas.columnas_numericas:
            log_warning("No se detectaron columnas numéricas en el archivo.")

        # Paso 5: Generar conclusiones automáticas (Insights Engine)
        log_info("Generando conclusiones de negocio automatizadas...")
        conclusiones = generar_conclusiones_automaticas(metricas, estadisticas)

        # Paso 6: Administrar el sistema de archivos de salida
        crear_carpeta_si_no_existe(path_salida)
        ruta_pdf = generar_ruta_pdf_unica(path_salida, ruta_archivo.name)
        tamano_legible = obtener_tamano_legible(ruta_archivo)

        # Paso 7: Generar el reporte PDF final
        log_step("Paso 5: Generando reporte PDF corporativo...")
        log_info("Generando reporte PDF...")
        construir_reporte_pdf(
            df=df_limpio,
            metricas=metricas,
            estadisticas=estadisticas,
            conclusiones=conclusiones,
            ruta_pdf=ruta_pdf,
            nombre_archivo_original=ruta_archivo.name,
            extension=extension,
            tamano_legible=tamano_legible
        )

        # Paso 8: Emitir resumen final por consola
        from src.infrastructure import mostrar_resumen_exitoso
        mostrar_resumen_exitoso(
            nombre_archivo=ruta_archivo.name,
            total_registros=metricas.total_registros,
            total_columnas=metricas.total_columnas,
            filas_eliminadas=limpieza_info.filas_vacias_eliminadas,
            ruta_pdf_absoluta=str(ruta_pdf.resolve())
        )

        log_success("Reporte generado correctamente")
        log_success("Proceso finalizado con éxito.")

    except Exception as e:
        log_error(f"Error procesando el archivo: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
