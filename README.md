# 📊 Generador Automático de Reportes Empresariales

Un motor modular de analítica y auditoría de datos en Python que automatiza por completo la limpieza, normalización, análisis de calidad de datos, estadísticas descriptivas de alta precisión contable (`Decimal`) y la compilación física de reportes PDF corporativos con diseño premium y conclusiones automatizadas basadas en los datos.

Este proyecto está desarrollado bajo principios **SOLID** y una arquitectura altamente desacoplada (**Clean Architecture**), lo que garantiza un entorno de trabajo escalable, mantenible y testeable.

---

## ✨ Características Principales

*   **🧹 Ingesta & Limpieza Inteligente de Datos**: Carga datos desde archivos `.xlsx`, `.xls` y `.csv`. Elimina filas completamente vacías, remueve espacios redundantes en strings de celdas y normaliza las cabeceras a formatos legibles.
*   **🧮 Aritmética de Alta Precisión (`Decimal`)**: Toda la agregación y cálculo descriptivo (Suma, Promedio, Mínimos, Máximos) se procesa utilizando la librería `Decimal` con precisión fija de 28 decimales. Esto evita los errores de redondeo tradicionales de coma flotante de hardware binario (`float`), garantizando reportes comerciales y financieros 100% confiables.
*   **🧠 Motor de Observaciones Automáticas (Insights Engine)**: Algoritmos dinámicos que analizan la calidad de los registros y redactan diagnósticos textuales y recomendaciones directas para la toma de decisiones gerenciales.
*   **🎨 Reporte PDF con Estética Premium (ReportLab)**:
    *   **Diseño Pizarra & Azul (Slate & Blue)** corporativo con colores curados y tipografías legibles.
    *   **Paginación Dinámica ("Página X de Y")** e inclusión de encabezados/pies de página mediante la clase `NumberedCanvas` de doble pasada.
    *   **Vista Previa Adaptativa**: Renderizado proporcional de las primeras 10 filas de datos adaptando dinámicamente el ancho de las columnas A4 para evitar solapamientos.
    *   **KeepTogether**: Secciones cohesivas (como conclusiones o tarjetas) protegidas para que no se fracturen visualmente de forma indecorosa en saltos de página.
*   **🔒 Prevención de Sobreescritura**: Implementa una asignación física incremental y segura para los informes resultantes (`reporte_ventas_1.pdf`, `reporte_ventas_2.pdf`).

---

## 📁 Estructura del Proyecto (Clean Architecture)

El proyecto sigue una organización desacoplada orientada a separar la lógica de negocio pura de los detalles técnicos de infraestructura:

```
Generador-de-reportes-automaticos/
├── main.py                         # Entrada CLI y bootstrap de la aplicación
├── config.py                       # Constantes visuales (colores, márgenes, límites) y carpetas por defecto
├── crear_datos_prueba.py           # Utilidad para generar datasets de prueba (.xlsx y .csv)
├── .gitignore                      # Exclusiones de Git (caches, entornos y PDFs resultantes)
├── README.md                       # Documentación principal del sistema
├── core/                           # CAPA DE DOMINIO: Modelos de datos e interfaces puras
│   ├── __init__.py
│   └── models.py                   # DTOs inmutables tipados (LimpiezaInfo, EstadisticaNumerica, MetricasReporte)
├── services/                       # CAPA DE APLICACIÓN: Casos de uso y reglas de procesamiento
│   ├── __init__.py
│   ├── data_cleaner.py             # Procesamiento y depuración con Pandas
│   ├── data_analyzer.py            # Métricas generales y resúmenes con aritmética Decimal
│   ├── insights_engine.py          # Motor de observaciones analíticas
│   └── report_orchestrator.py      # Orquestador y pipeline analítico principal
└── infrastructure/                 # CAPA DE INFRAESTRUCTURA: Adaptadores tecnológicos externos
    ├── __init__.py
    ├── file_system.py              # Gestión física y nombres incrementales del disco
    ├── logger.py                   # Logs de consola seguros en ASCII para evitar problemas unicode
    └── pdf/                        # Adaptador ReportLab para maquetado visual
        ├── __init__.py
        ├── styles.py               # Hojas de estilo visuales y paletas de colores
        ├── canvas_templates.py     # Paginación dinámica (NumberedCanvas) y carátula
        └── pdf_builder.py          # Constructor del lienzo A4 (portada, tablas y espaciados)
```

---

## 🚀 Instalación y Requisitos

### Requisitos Previos
*   Python 3.10 o superior instalado.

### Clonar el Repositorio
```bash
git clone https://github.com/Braulio2002/Generador-de-reportes-automaticos.git
cd Generador-de-reportes-automaticos
```

### Instalar Dependencias
Instala los paquetes analíticos y de generación visual necesarios:
```bash
pip install pandas openpyxl reportlab xlrd
```

---

## 💻 Instrucciones de Uso

### 1. Iniciar los datos de prueba
Para generar los datasets de prueba simulados con nulos, duplicados y variables numéricas/categóricas, ejecuta:
```bash
python crear_datos_prueba.py
```
Esto creará de manera automatizada:
*   `./datos_entrada/ventas_test.xlsx`
*   `./datos_entrada/clientes_test.csv`

### 2. Ejecutar el orquestador principal
Puedes invocar a `main.py` especificando el archivo de entrada mediante la interfaz CLI:

*   **Analizar Excel de Ventas**:
    ```bash
    python main.py -i datos_entrada/ventas_test.xlsx
    ```
*   **Analizar CSV de Clientes**:
    ```bash
    python main.py -i datos_entrada/clientes_test.csv
    ```
*   **Cambiar la carpeta de salida del PDF**:
    ```bash
    python main.py -i datos_entrada/ventas_test.xlsx -o reportes_comerciales
    ```

> 💡 **Nota Inteligente**: Si ejecutas `python main.py` sin argumentos, el sistema escaneará automáticamente la carpeta `./datos_entrada`, identificará el archivo de datos más recientemente modificado y procesará su información de forma directa.

---

## 📈 Salida de Consola Esperada

Al iniciar la ejecución, verás una interfaz visual formateada libre de caracteres unicode conflictivos, lo que garantiza compatibilidad total en terminales de codificación restringida en Windows (CP1252/PowerShell):

```text
+------------------------------------------------------------------+
|         GENERADOR AUTOMATICO DE REPORTES EMPRESARIALES           |
|         Tecnología de Auditoría de Calidad y Estadísticas        |
+------------------------------------------------------------------+

> Iniciando procesamiento para el archivo: 'ventas_test.xlsx'
> Paso 1: Validando archivo de entrada...
[INFO] Validando archivo de entrada: ventas_test.xlsx...
[ÉXITO] Archivo de entrada validado correctamente.
> Paso 2: Leyendo datos del Excel/CSV...
[INFO] Leyendo datos del archivo...
[ÉXITO] Datos leídos con éxito. Registros iniciales: 15 | Columnas: 7
> Paso 3: Limpiando datos...
[INFO] Limpiando datos...
[ÉXITO] Limpieza completada. Filas vacías eliminadas: 0
> Paso 4: Calculando métricas y análisis cuantitativo...
[INFO] Calculando métricas generales...
[INFO] Analizando estadísticas de columnas numéricas...
[INFO] Generando conclusiones de negocio automatizadas...
> Paso 5: Generando reporte PDF corporativo...
[INFO] Generando reporte PDF...

========================================================================
*** RESUMEN DE PROCESAMIENTO EXITOSO ***
========================================================================
[Archivo] Archivo Procesado:         ventas_test.xlsx
[Registros] Total Registros Analizados:15
[Columnas] Total Columnas:            7
[Limpieza] Filas Vacías Eliminadas:   0
[Reporte] Ruta del PDF Generado:     D:\reportes\reporte_ventas_test.pdf
========================================================================

[ÉXITO] Reporte generado correctamente
[ÉXITO] Proceso finalizado con éxito.
```

---

## 📜 Estructura del Reporte PDF

El reporte resultante se divide en las siguientes secciones maquetadas a la perfección:
1.  **Portada Corporativa**: Banner decorativo Slate, título principal destacado, metadatos estructurados de auditoría y notas de confidencialidad.
2.  **Resumen Ejecutivo**: Balance cuantitativo general en formato de tarjetas e informe del diagnóstico físico de calidad de los datos (celdas vacías, registros duplicados).
3.  **Estadísticas Generales**: Desglose exacto (Suma, Media, Min, Max) en aritmética Decimal de las variables métricas.
4.  **Vista Previa de los Datos**: Muestra controlada de las primeras 10 filas de información adaptada al ancho útil de la página A4.
5.  **Conclusiones y Recomendaciones**: Observaciones textuales automatizadas y sugerencias operativas para corregir inconsistencias en la captura.
