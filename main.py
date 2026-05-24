# -*- coding: utf-8 -*-
"""
Generador de Reportes Automáticos (Entrada Principal)
------------------------------------------------------
Punto de acceso de la interfaz de comandos de la aplicación.
Organiza la invocación del orquestador y la administración del CLI.
"""

import sys
import argparse
from pathlib import Path

# Importar módulos usando el espacio de nombres de la carpeta src
from src.config import DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR
from src.infrastructure import mostrar_banner, log_info, log_warning, log_error
from src.services import ejecutar_pipeline_reporte


def main() -> None:
    # 1. Configurar CLI Parser
    parser = argparse.ArgumentParser(
        description="Script automático en arquitectura modular para el análisis de datos y generación de reportes PDF."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        help="Ruta del archivo Excel (.xlsx, .xls) o CSV de entrada."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help="Carpeta donde se guardará el reporte PDF (por defecto: './datos_salida')."
    )

    args = parser.parse_args()

    # 2. Mostrar banner estético
    mostrar_banner()

    archivo_entrada = args.input
    carpeta_salida = args.output_dir

    # 3. Escaneo inteligente de archivos por defecto
    if not archivo_entrada:
        if DEFAULT_INPUT_DIR.exists():
            archivos_disponibles = [
                p for p in DEFAULT_INPUT_DIR.iterdir()
                if p.is_file() and p.suffix.lower() in ['.xlsx', '.xls', '.csv']
            ]
            if archivos_disponibles:
                # Ordenar por fecha de modificación (tomar el más reciente)
                archivos_disponibles.sort(
                    key=lambda p: p.stat().st_mtime, reverse=True)
                archivo_entrada = str(archivos_disponibles[0])
                log_info(
                    f"No se ingresó ruta de entrada. Seleccionando archivo más reciente: {archivo_entrada}")
            else:
                log_warning(
                    f"No se encontraron archivos en la carpeta por defecto: '{DEFAULT_INPUT_DIR}'")

        if not archivo_entrada:
            log_error("Debe especificar la ruta de un archivo de datos.")
            print("\nUso correcto:")
            print("  python main.py -i ruta/al/archivo.xlsx")
            print("  python main.py --input datos.csv --output-dir reportes_pdf\n")
            sys.exit(1)

    # 4. Invocación del pipeline
    ejecutar_pipeline_reporte(archivo_entrada, carpeta_salida)


if __name__ == "__main__":
    main()
