# -*- coding: utf-8 -*-
"""
Adaptador de Logs e Interfaz de Consola
----------------------------------------
Controla la salida en terminal formateada, limpia y compatible con codificación CP1252.
"""

import sys


class ConsoleColor:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def log_info(msg: str) -> None:
    print(f"{ConsoleColor.BLUE}[INFO]{ConsoleColor.RESET} {msg}")


def log_success(msg: str) -> None:
    print(
        f"{ConsoleColor.GREEN}[ÉXITO]{ConsoleColor.RESET} {ConsoleColor.BOLD}{msg}{ConsoleColor.RESET}")


def log_warning(msg: str) -> None:
    print(f"{ConsoleColor.YELLOW}[ADVERTENCIA]{ConsoleColor.RESET} {msg}")


def log_error(msg: str) -> None:
    print(
        f"{ConsoleColor.RED}[ERROR]{ConsoleColor.RESET} {ConsoleColor.BOLD}{msg}{ConsoleColor.RESET}")


def log_step(msg: str) -> None:
    print(f"{ConsoleColor.CYAN}> {msg}{ConsoleColor.RESET}")


def mostrar_banner() -> None:
    """Imprime el banner principal ASCII de la aplicación."""
    print(f"{ConsoleColor.BLUE}{ConsoleColor.BOLD}")
    print("+------------------------------------------------------------------+")
    print("|         GENERADOR AUTOMÁTICO DE REPORTES EMPRESARIALES           |")
    print("|         Tecnología de Auditoría de Calidad y Estadísticas        |")
    print("+------------------------------------------------------------------+")
    print(f"{ConsoleColor.RESET}")


def mostrar_resumen_exitoso(
    nombre_archivo: str,
    total_registros: int,
    total_columnas: int,
    filas_eliminadas: int,
    ruta_pdf_absoluta: str
) -> None:
    """Imprime el balance final de procesamiento en la consola."""
    print(f"\n{ConsoleColor.GREEN}{ConsoleColor.BOLD}========================================================================")
    print("*** RESUMEN DE PROCESAMIENTO EXITOSO ***")
    print(
        f"========================================================================{ConsoleColor.RESET}")
    print(f"[Archivo] Archivo Procesado:         {nombre_archivo}")
    print(f"[Registros] Total Registros Analizados:{total_registros:,}")
    print(f"[Columnas] Total Columnas:            {total_columnas}")
    print(f"[Limpieza] Filas Vacías Eliminadas:   {filas_eliminadas}")
    print(
        f"[Reporte] Ruta del PDF Generado:     {ConsoleColor.BOLD}{ruta_pdf_absoluta}{ConsoleColor.RESET}")
    print(f"{ConsoleColor.GREEN}========================================================================{ConsoleColor.RESET}\n")
