# -*- coding: utf-8 -*-
"""
Plantillas de Canvas del PDF
----------------------------
Controla el ciclo de vida en dos pasadas de ReportLab para la paginación dinámica,
así como el pintado estético de la Portada y los Encabezados repetitivos.
"""

from datetime import datetime
from reportlab.pdfgen import canvas

from src.config import (
    PRIMARY_COLOR, SECONDARY_COLOR, NEUTRAL_LIGHT,
    BORDER_COLOR, TEXT_MUTED
)


class NumberedCanvas(canvas.Canvas):
    """
    Canvas de doble pasada para calcular el total de páginas
    y añadir un encabezado/pie de página corporativo dinámico.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        # Almacenar estado de la página para la segunda pasada
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count: int):
        self.saveState()

        # Omitir elementos repetitivos en la Portada (Página 1)
        if self._pageNumber == 1:
            self.restoreState()
            return

        # ---- ENCABEZADO REPETITIVO ----
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(PRIMARY_COLOR)
        self.drawString(54, 795, "REPORTE AUTOMÁTICO DE ANÁLISIS DE DATOS")

        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(541, 795, "CONFIDENCIAL - USO INTERNO")

        # Línea divisoria de encabezado
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 788, 541, 788)

        # ---- PIE DE PÁGINA REPETITIVO ----
        self.line(54, 52, 541, 52)

        local_time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.drawString(54, 38, f"Generado el: {local_time_str}")

        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 38, page_text)

        self.restoreState()


def decorar_portada(canvas_inst: canvas.Canvas, _doc_inst=None) -> None:
    """Callback para dibujar el fondo estético de la portada en la primera página."""
    canvas_inst.saveState()

    # Franja superior en pizarra oscuro (42% superior de la portada)
    canvas_inst.setFillColor(PRIMARY_COLOR)
    canvas_inst.rect(0, 488, 595.27, 353.89, stroke=0, fill=1)

    # Línea decorativa secundaria en azul
    canvas_inst.setFillColor(SECONDARY_COLOR)
    canvas_inst.rect(0, 480, 595.27, 8, stroke=0, fill=1)

    # Pie estético en gris suave
    canvas_inst.setFillColor(NEUTRAL_LIGHT)
    canvas_inst.rect(0, 0, 595.27, 60, stroke=0, fill=1)

    # Metadatos del sistema en el pie de portada
    canvas_inst.setFont("Helvetica-Bold", 8)
    canvas_inst.setFillColor(PRIMARY_COLOR)
    canvas_inst.drawString(54, 28, "GENERADOR DE REPORTES AUTOMÁTICOS")

    canvas_inst.setFont("Helvetica", 8)
    canvas_inst.setFillColor(TEXT_MUTED)
    canvas_inst.drawRightString(
        541, 28, "TECNOLOGÍA DE AUDITORÍA Y ANÁLISIS DE DATOS")

    canvas_inst.restoreState()
