# -*- coding: utf-8 -*-
"""
Adaptador de Acceso al Sistema de Archivos
------------------------------------------
Gestiona rutas, confirma la existencia de ficheros y previene la sobreescritura.
"""

from pathlib import Path


def validar_existencia(ruta_archivo: Path) -> bool:
    """Verifica si la ruta provista apunta a un archivo físico real existente."""
    return ruta_archivo.exists() and ruta_archivo.is_file()


def crear_carpeta_si_no_existe(carpeta: Path) -> None:
    """Crea el directorio destino y sus ancestros de forma recursiva si no existe."""
    if not carpeta.exists():
        carpeta.mkdir(parents=True, exist_ok=True)


def obtener_tamano_legible(ruta_archivo: Path) -> str:
    """Retorna el tamaño en bytes convertido en KB o MB legible."""
    try:
        bytes_size = ruta_archivo.stat().st_size
        if bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.2f} KB"
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    except Exception:
        return "Desconocido"


def generar_ruta_pdf_unica(carpeta_salida: Path, nombre_original: str) -> Path:
    """
    Genera un nombre de archivo único de reporte en la carpeta destino,
    evitando sobreescrituras mediante sufijos correlativos.

    Ejemplo:
      nombre_original: "ventas.xlsx" -> "reporte_ventas.pdf"
      Si existe: "reporte_ventas_1.pdf", "reporte_ventas_2.pdf", etc.
    """
    nombre_limpio = Path(nombre_original).stem.replace(" ", "_")
    nombre_pdf = f"reporte_{nombre_limpio}.pdf"
    ruta_pdf = carpeta_salida / nombre_pdf

    if not ruta_pdf.exists():
        return ruta_pdf

    contador = 1
    while True:
        nombre_con_sufijo = f"reporte_{nombre_limpio}_{contador}.pdf"
        ruta_pdf = carpeta_salida / nombre_con_sufijo
        if not ruta_pdf.exists():
            return ruta_pdf
        contador += 1
