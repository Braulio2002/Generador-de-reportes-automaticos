# -*- coding: utf-8 -*-
"""
Estilos Visuales de ReportLab
------------------------------
Definición centralizada de fuentes, tamaños, interlineados y estilos de párrafo
para el maquetado del documento PDF.
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from src.config import (
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR,
    NEUTRAL_DARK, NEUTRAL_LIGHT, BORDER_COLOR,
    SUCCESS_COLOR, WARNING_COLOR, TEXT_MUTED
)


class EstilosReporte:
    def __init__(self):
        self.styles = getSampleStyleSheet()

        # 1. Estilo de Título Principal en Portada
        self.cover_title = ParagraphStyle(
            'CoverTitle',
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=30,
            textColor=colors.white,
            alignment=0,
            spaceAfter=10
        )

        # 2. Estilo de Subtítulo en Portada
        self.cover_subtitle = ParagraphStyle(
            'CoverSubtitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#93C5FD"),
            alignment=0,
            spaceAfter=25
        )

        # 3. Encabezados de Variable (H1)
        self.h1 = ParagraphStyle(
            'Header1',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=PRIMARY_COLOR,
            spaceBefore=15,
            spaceAfter=10,
            keepWithNext=True
        )

        # 4. Subencabezados (H2)
        self.h2 = ParagraphStyle(
            'Header2',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            textColor=SECONDARY_COLOR,
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True
        )

        # 5. Cuerpo de Texto Estándar
        self.body = ParagraphStyle(
            'Body',
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=NEUTRAL_DARK,
            spaceAfter=8
        )

        # 6. Cuerpo en Negrita
        self.body_bold = ParagraphStyle(
            'BodyBold',
            parent=self.body,
            fontName='Helvetica-Bold'
        )

        # 7. Cabeceras de Tabla
        self.table_header = ParagraphStyle(
            'TableHeader',
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white,
            alignment=1
        )

        # 8. Celdas de Tabla
        self.table_cell = ParagraphStyle(
            'TableCell',
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=NEUTRAL_DARK,
            alignment=0
        )

        self.table_cell_center = ParagraphStyle(
            'TableCellCenter',
            parent=self.table_cell,
            alignment=1
        )

        self.table_cell_right = ParagraphStyle(
            'TableCellRight',
            parent=self.table_cell,
            alignment=2
        )

        # 9. Textos de Tarjeta / Grid Resumen
        self.card_text = ParagraphStyle(
            'CardText',
            parent=self.body,
            fontSize=9,
            leading=13,
            textColor=NEUTRAL_DARK
        )

        # 10. Notas Secundarias / Muted
        self.muted_note = ParagraphStyle(
            'MutedNote',
            parent=self.body,
            textColor=TEXT_MUTED,
            fontSize=8.5,
            leading=12
        )

        self.conclusion_bullet = ParagraphStyle(
            'ConclusionBullet',
            parent=self.body,
            leftIndent=12,
            spaceAfter=6
        )
