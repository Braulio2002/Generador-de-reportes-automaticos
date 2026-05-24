# -*- coding: utf-8 -*-
"""
Módulo de Configuración Global
------------------------------
Define constantes de diseño, rutas predeterminadas de carpetas
y configuraciones visuales del Generador de Reportes Automáticos.
"""

from pathlib import Path
from reportlab.lib import colors

# =========================================================================
# 📂 RUTAS Y CARPETAS PREDETERMINADAS
# =========================================================================
DEFAULT_INPUT_DIR = Path("./datos_entrada")
DEFAULT_OUTPUT_DIR = Path("./datos_salida")

# =========================================================================
# 🎨 PALETA DE COLORES CORPORATIVOS (Premium Slate & Blue)
# =========================================================================
# Pizarra Oscuro (Cabeceras y portada)
PRIMARY_COLOR = colors.HexColor("#1E293B")
# Azul Eléctrico (Acentos y subtítulos)
SECONDARY_COLOR = colors.HexColor("#3B82F6")
# Azul Cielo (Líneas y destacados)
ACCENT_COLOR = colors.HexColor("#0EA5E9")
NEUTRAL_DARK = colors.HexColor("#0F172A")      # Texto principal (Slate 900)
NEUTRAL_LIGHT = colors.HexColor("#F8FAFC")     # Fondo de tablas (Slate 50)
BORDER_COLOR = colors.HexColor("#E2E8F0")      # Bordes suaves (Slate 200)
# Verde Esmeralda (Datos correctos)
SUCCESS_COLOR = colors.HexColor("#10B981")
WARNING_COLOR = colors.HexColor("#F59E0B")     # Amarillo Ámbar (Alertas/Nulos)
TEXT_MUTED = colors.HexColor("#64748B")        # Texto secundario (Slate 500)

# =========================================================================
# 📐 DIMENSIONES Y MAQUETADO DE PDF
# =========================================================================
# Márgenes en puntos (54 pt = 0.75 pulgadas = 1.9 cm)
LEFT_MARGIN = 54
RIGHT_MARGIN = 54
TOP_MARGIN = 54
BOTTOM_MARGIN = 54

# Límite máximo de columnas para la vista previa de datos para evitar desbordes en A4
MAX_PREVIEW_COLS = 7
MAX_PREVIEW_ROWS = 10
