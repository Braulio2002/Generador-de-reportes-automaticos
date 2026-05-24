# -*- coding: utf-8 -*-
"""
Constructor Físico de PDF
---------------------------
Toma los datos tabulares, métricas descriptivas y conclusiones automatizadas,
y maqueta físicamente el documento PDF en páginas A4 utilizando ReportLab.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

from src.config import (
    LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, BOTTOM_MARGIN,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR,
    NEUTRAL_DARK, NEUTRAL_LIGHT, BORDER_COLOR,
    SUCCESS_COLOR, WARNING_COLOR, TEXT_MUTED,
    MAX_PREVIEW_COLS, MAX_PREVIEW_ROWS
)
from src.core.models import MetricasReporte, EstadisticaNumerica
from .styles import EstilosReporte
from .canvas_templates import NumberedCanvas, decorar_portada


def calcular_anchos_columnas(df_subset: pd.DataFrame, ancho_disponible: float = 487.27) -> List[float]:
    """Calcula proporcionalmente los anchos de columna para que encajen en el lienzo A4."""
    num_cols = len(df_subset.columns)
    if num_cols == 0:
        return []

    anchos_caracteres = []
    for col in df_subset.columns:
        max_len = len(str(col))
        for val in df_subset[col].head(10):
            val_len = len(str(val)) if pd.notnull(val) else 4
            if val_len > max_len:
                max_len = val_len
        anchos_caracteres.append(max_len)

    total_caracteres = sum(anchos_caracteres)
    if total_caracteres == 0:
        return [ancho_disponible / num_cols] * num_cols

    min_width = 40.0
    anchos = []
    for char_len in anchos_caracteres:
        prop_width = (char_len / total_caracteres) * ancho_disponible
        anchos.append(max(prop_width, min_width))

    suma_anchos = sum(anchos)
    scale = ancho_disponible / suma_anchos
    return [width * scale for width in anchos]


# =========================================================================
# 🛠️ FUNCIONES AUXILIARES PRIVADAS PARA REDUCIR COMPLEJIDAD COGNITIVA
# =========================================================================

def _construir_portada(
    diseno: EstilosReporte,
    nombre_archivo_original: str,
    extension: str,
    tamano_legible: str
) -> List[Any]:
    """Genera secuencialmente los elementos de la Portada del Reporte."""
    elements = []
    elements.append(Spacer(1, 40))
    elements.append(
        Paragraph("REPORTE AUTOMÁTICO DE ANÁLISIS DE DATOS", diseno.cover_title))
    elements.append(Paragraph(
        "AUDITORÍA INTEGRAL DE CALIDAD Y MÉTRICAS CLAVE", diseno.cover_subtitle))

    # Desplazar el flujo hacia abajo pasando el banner decorativo
    elements.append(Spacer(1, 140))
    elements.append(Paragraph("INFORMACIÓN GENERAL DEL ANÁLISIS", diseno.h2))

    local_time_str = datetime.now().strftime("%d/%m/%Y a las %H:%M:%S")

    meta_data = [
        [Paragraph("<b>Archivo de Origen:</b>", diseno.body),
         Paragraph(nombre_archivo_original, diseno.body)],
        [Paragraph("<b>Formato Detectado:</b>", diseno.body),
         Paragraph(f"Archivo plano ({extension.upper()})", diseno.body)],
        [Paragraph("<b>Tamaño del Archivo:</b>", diseno.body),
         Paragraph(tamano_legible, diseno.body)],
        [Paragraph("<b>Fecha y Hora de Emisión:</b>", diseno.body),
         Paragraph(local_time_str, diseno.body)],
        [Paragraph("<b>Estado de los Datos:</b>", diseno.body), Paragraph(
            f"<font color='{SUCCESS_COLOR.hexval()}'><b>PROCESADO Y NORMALIZADO</b></font>", diseno.body_bold)]
    ]

    meta_table = Table(meta_data, colWidths=[150, 337])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NEUTRAL_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(meta_table)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "<b>Nota de Confidencialidad y Uso:</b> Este reporte contiene métricas operativas y datos de calidad calculados de "
        "forma automatizada a partir del archivo suministrado. La información está estructurada para su interpretación directa "
        "por las áreas administrativas, operativas o gerenciales autorizadas.",
        diseno.muted_note
    ))

    elements.append(PageBreak())
    return elements


def _construir_resumen_y_calidad(
    diseno: EstilosReporte,
    metricas: MetricasReporte
) -> List[Any]:
    """Genera la sección 1 (Resumen Ejecutivo) y sección 2 (Calidad de Datos)."""
    elements = []
    elements.append(Paragraph("1. RESUMEN EJECUTIVO", diseno.h1))
    elements.append(Paragraph(
        "Este reporte proporciona un diagnóstico integral del estado físico e integridad de los datos cargados. "
        "A continuación se presenta un balance general de los recursos detectados en el archivo analizado:",
        diseno.body
    ))

    registros_formateados = f"{metricas.total_registros:,}"
    resumen_data = [
        [
            Paragraph(
                f"<b>Total de Registros:</b><br/><font size='14' color='{PRIMARY_COLOR.hexval()}'><b>{registros_formateados}</b></font>", diseno.card_text),
            Paragraph(
                f"<b>Total de Columnas:</b><br/><font size='14' color='{PRIMARY_COLOR.hexval()}'><b>{metricas.total_columnas}</b></font>", diseno.card_text)
        ],
        [
            Paragraph(
                f"<b>Columnas Numéricas:</b><br/><font size='14' color='{SECONDARY_COLOR.hexval()}'><b>{len(metricas.columnas_numericas)}</b></font>", diseno.card_text),
            Paragraph(
                f"<b>Columnas Categóricas:</b><br/><font size='14' color='{SECONDARY_COLOR.hexval()}'><b>{len(metricas.columnas_categoricas)}</b></font>", diseno.card_text)
        ]
    ]

    resumen_table = Table(resumen_data, colWidths=[243, 244])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NEUTRAL_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(resumen_table)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("2. ANÁLISIS DE CALIDAD DE DATOS", diseno.h1))
    elements.append(Paragraph(
        "La limpieza y auditoría de la calidad de datos identifica registros potencialmente corruptos, duplicados o celdas faltantes. "
        "Se aplicó un filtro inicial para normalizar los datos de entrada sin alterar la fuente original.",
        diseno.body
    ))

    calidad_cabecera = [
        Paragraph("Indicador de Calidad", diseno.table_header),
        Paragraph("Valor Detectado", diseno.table_header),
        Paragraph("Porcentaje / Impacto", diseno.table_header),
        Paragraph("Estado / Diagnóstico", diseno.table_header)
    ]

    pct_vacios = (metricas.total_vacios / (metricas.total_registros *
                  metricas.total_columnas)) * 100 if metricas.total_registros > 0 else 0
    pct_duplicados = (metricas.total_duplicados / metricas.total_registros) * \
        100 if metricas.total_registros > 0 else 0

    status_vacios = f"<font color='{SUCCESS_COLOR.hexval()}'><b>ÓPTIMO</b></font>" if pct_vacios < 1 else f"<font color='{WARNING_COLOR.hexval()}'><b>REVISAR</b></font>"
    status_dup = f"<font color='{SUCCESS_COLOR.hexval()}'><b>ÓPTIMO</b></font>" if pct_duplicados < 1 else f"<font color='{WARNING_COLOR.hexval()}'><b>DUPLICADOS DETECTADOS</b></font>"
    status_eliminadas = f"<font color='{PRIMARY_COLOR.hexval()}'><b>DEPURADO</b></font>" if metricas.filas_vacias_eliminadas > 0 else "SIN CAMBIO"

    calidad_rows = [
        calidad_cabecera,
        [
            Paragraph("Filas vacías eliminadas", diseno.table_cell),
            Paragraph(str(metricas.filas_vacias_eliminadas),
                      diseno.table_cell_center),
            Paragraph("-", diseno.table_cell_center),
            Paragraph(status_eliminadas, diseno.table_cell_center)
        ],
        [
            Paragraph("Celdas vacías (Nulos)", diseno.table_cell),
            Paragraph(f"{metricas.total_vacios:,}", diseno.table_cell_center),
            Paragraph(f"{pct_vacios:.2f}% de celdas",
                      diseno.table_cell_center),
            Paragraph(status_vacios, diseno.table_cell_center)
        ],
        [
            Paragraph("Registros duplicados", diseno.table_cell),
            Paragraph(f"{metricas.total_duplicados:,}",
                      diseno.table_cell_center),
            Paragraph(f"{pct_duplicados:.2f}% de filas",
                      diseno.table_cell_center),
            Paragraph(status_dup, diseno.table_cell_center)
        ]
    ]

    calidad_table = Table(calidad_rows, colWidths=[160, 95, 110, 122])
    calidad_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, NEUTRAL_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(calidad_table)

    if metricas.columnas_con_mas_nulos:
        elements.append(Spacer(1, 10))
        nulos_detalles = " | ".join(
            [f"<b>{col}</b>: {num} vacíos" for col, num in metricas.columnas_con_mas_nulos.items()])
        elements.append(Paragraph(
            f"<font color='{WARNING_COLOR.hexval()}'><b>[ALERTA]</b></font> <b>Columnas críticas con vacíos:</b> {nulos_detalles}",
            diseno.table_cell
        ))

    elements.append(PageBreak())
    return elements


def _construir_estadisticas_numericas(
    diseno: EstilosReporte,
    estadisticas: List[EstadisticaNumerica]
) -> List[Any]:
    """Genera la sección 3 (Estadísticas generales cuantitativas)."""
    elements = []
    elements.append(
        Paragraph("3. ESTADÍSTICAS GENERALES NUMÉRICAS", diseno.h1))

    if not estadisticas:
        elements.append(Spacer(1, 10))
        sin_num_data = [[
            Paragraph(
                f"<font size='12' color='{WARNING_COLOR.hexval()}'><b>Métricas Cuantitativas no Disponibles</b></font><br/>"
                "El set de datos analizado no contiene columnas con variables numéricas detectadas (enteros o flotantes). "
                "No ha sido posible computar operaciones aritméticas como sumas, promedios o máximos. "
                "Esto es habitual en archivos orientados estrictamente a registros descriptivos, maestros de clientes o descripciones de texto.",
                diseno.body
            )
        ]]
        sin_num_table = Table(sin_num_data, colWidths=[487])
        sin_num_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), NEUTRAL_LIGHT),
            ('BOX', (0, 0), (-1, -1), 1.5, WARNING_COLOR),
            ('PADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(sin_num_table)
    else:
        elements.append(Paragraph(
            "Se detectaron las siguientes columnas con valores numéricos. Para garantizar la máxima precisión en valores y evitar "
            "los errores habituales de redondeo en coma flotante binaria (floats), todos los cálculos matemáticos de acumulación, "
            "promedio, límites mínimos y límites máximos han sido computados usando aritmética decimal de precisión fija (Decimal):",
            diseno.body
        ))

        est_cabecera = [
            Paragraph("Columna Numérica", diseno.table_header),
            Paragraph("Suma Total", diseno.table_header),
            Paragraph("Promedio", diseno.table_header),
            Paragraph("Valor Mínimo", diseno.table_header),
            Paragraph("Valor Máximo", diseno.table_header)
        ]

        est_rows = [est_cabecera]
        for est in estadisticas:
            est_rows.append([
                Paragraph(f"<b>{est.columna}</b>", diseno.table_cell),
                Paragraph(f"{est.suma:,.2f}", diseno.table_cell_right),
                Paragraph(f"{est.promedio:,.2f}", diseno.table_cell_right),
                Paragraph(f"{est.minimo:,.2f}", diseno.table_cell_right),
                Paragraph(f"{est.maximo:,.2f}", diseno.table_cell_right)
            ])

        est_table = Table(est_rows, colWidths=[127, 90, 90, 90, 90])
        est_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, NEUTRAL_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('PADDING', (0, 1), (-1, -1), 7),
        ]))
        elements.append(est_table)

    elements.append(PageBreak())
    return elements


def _construir_vista_previa(
    diseno: EstilosReporte,
    df: pd.DataFrame
) -> List[Any]:
    """Genera la sección 4 (Tabla de Vista Previa de los datos)."""
    elements = []
    elements.append(Paragraph("4. VISTA PREVIA DE DATOS", diseno.h1))

    total_cols_actual = len(df.columns)
    if total_cols_actual > MAX_PREVIEW_COLS:
        df_preview = df.iloc[:, :MAX_PREVIEW_COLS]
        elements.append(Paragraph(
            f"El archivo contiene un total de <b>{total_cols_actual}</b> columnas. Por razones de legibilidad y para "
            f"evitar desbordes de página en formato A4 vertical, a continuación se presenta una vista previa con las primeras "
            f"<b>10 filas</b> limitadas a las primeras <b>{MAX_PREVIEW_COLS} columnas</b> del archivo:",
            diseno.body
        ))
    else:
        df_preview = df
        elements.append(Paragraph(
            "A continuación se presenta una muestra representativa con las primeras <b>10 filas</b> y la totalidad "
            "de las columnas del archivo cargado:",
            diseno.body
        ))

    preview_cabecera = [Paragraph(col, diseno.table_header)
                        for col in df_preview.columns]
    preview_rows = [preview_cabecera]

    # Función auxiliar local para formatear celdas y controlar la complejidad
    def _formatear_celda(valor: Any) -> Paragraph:
        if pd.isnull(valor):
            return Paragraph(f"<font color='{WARNING_COLOR.hexval()}'><i>Null</i></font>", diseno.table_cell)
        texto = str(valor)
        if len(texto) > 28:
            texto = texto[:25] + "..."
        return Paragraph(texto, diseno.table_cell)

    for _, fila in df_preview.head(MAX_PREVIEW_ROWS).iterrows():
        fila_formateada = [_formatear_celda(val) for val in fila]
        preview_rows.append(fila_formateada)

    anchos_proporcionales = calcular_anchos_columnas(
        df_preview, ancho_disponible=487.27)

    preview_table = Table(preview_rows, colWidths=anchos_proporcionales)
    preview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, NEUTRAL_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(preview_table)
    return elements


def _construir_conclusiones(
    diseno: EstilosReporte,
    conclusiones: List[str]
) -> List[Any]:
    """Genera la sección 5 (Bloque KeepTogether de Conclusiones y Recomendaciones)."""
    elements = []
    elements.append(Spacer(1, 20))

    bloque_conclusiones = []
    bloque_conclusiones.append(
        Paragraph("5. CONCLUSIONES Y RECOMENDACIONES", diseno.h1))
    bloque_conclusiones.append(Paragraph(
        "A partir de las métricas de calidad y la analítica descriptiva realizada de forma automatizada por el motor, "
        "se desprenden las siguientes observaciones relevantes:",
        diseno.body
    ))

    for conclusion in conclusiones:
        bloque_conclusiones.append(Paragraph(
            f"• {conclusion}",
            diseno.conclusion_bullet
        ))

    elements.append(KeepTogether(bloque_conclusiones))
    return elements


# =========================================================================
# 🚀 ORQUESTADOR PÚBLICO DE MAQUETADO DE PDF
# =========================================================================

def construir_reporte_pdf(
    df: pd.DataFrame,
    metricas: MetricasReporte,
    estadisticas: List[EstadisticaNumerica],
    conclusiones: List[str],
    ruta_pdf: Path,
    nombre_archivo_original: str,
    extension: str,
    tamano_legible: str
) -> None:
    """Maqueta y compila el documento PDF final con ReportLab."""

    # El ancho útil es A4 ancho (595.27 pt) - márgenes izquierdo/derecho (108 pt) = 487.27 pt
    doc = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )

    # Cargar hoja de estilos visuales
    diseno = EstilosReporte()
    story = []

    # Construir secuencialmente cada una de las secciones en sub-bloques modulares
    story.extend(_construir_portada(
        diseno, nombre_archivo_original, extension, tamano_legible))
    story.extend(_construir_resumen_y_calidad(diseno, metricas))
    story.extend(_construir_estadisticas_numericas(diseno, estadisticas))
    story.extend(_construir_vista_previa(diseno, df))
    story.extend(_construir_conclusiones(diseno, conclusiones))

    # Compilar el documento PDF en el sistema de archivos
    doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=decorar_portada)
