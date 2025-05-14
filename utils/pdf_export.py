from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime
import os

from utils.merkle_visual import generar_imagen_arbol_merkle


def exportar_bloque_pdf(bloque, carpeta_salida="bloques_exportados"):
    os.makedirs(carpeta_salida, exist_ok=True)
    nombre_archivo = f"bloque_{bloque.id_caso}_{bloque.hash_bloque[:8]}.pdf"
    ruta_pdf = os.path.join(carpeta_salida, nombre_archivo)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=LETTER,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    elementos = _bloque_a_elementos(bloque)
    doc.build(elementos)

    return ruta_pdf


def exportar_cadena_pdf(lista_bloques, carpeta_salida="bloques_exportados"):
    os.makedirs(carpeta_salida, exist_ok=True)
    nombre_pdf = f"cadena_bloques_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    ruta_pdf = os.path.join(carpeta_salida, nombre_pdf)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=LETTER,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    elementos = []
    for idx, bloque in enumerate(lista_bloques):
        elementos += _bloque_a_elementos(bloque, index=idx)
        elementos.append(PageBreak())  # Siempre separar bloques

    # Eliminar último salto de página si está vacío
    if elementos and isinstance(elementos[-1], PageBreak):
        elementos.pop()

    doc.build(elementos)
    return ruta_pdf


def _bloque_a_elementos(bloque, index=None):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justificado', alignment=4))  # Justificado
    elementos = []

    # Título y encabezado
    titulo = f"📄 Reporte Legal de Bloque Minado"
    if index is not None:
        titulo += f" (#{index})"
    encabezado = (
        f"<b>ID del Caso:</b> {bloque.id_caso}<br/>"
        f"<b>Entidad:</b> {bloque.entidad}<br/>"
        f"<b>Fecha:</b> {datetime.fromtimestamp(bloque.timestamp).strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        f"<b>Fiscal Responsable:</b> {bloque.fiscal_responsable}<br/>"
        f"<b>Hash del Bloque:</b> {bloque.hash_bloque}<br/>"
        f"<b>Hash Anterior:</b> {bloque.hash_anterior}<br/>"
        f"<b>Merkle Root:</b> {bloque.merkle_root}"
    )
    elementos.append(Paragraph(titulo, styles['Title']))
    elementos.append(Spacer(1, 0.1 * inch))
    elementos.append(Paragraph(encabezado, styles['Normal']))
    elementos.append(Spacer(1, 0.2 * inch))

    # Tabla de Evidencias
    if bloque.evidencias:
        evidencias = [[str(i+1), h] for i, h in enumerate(bloque.evidencias)]
        tabla_ev = Table([["#", "Hash de Evidencia"]] + evidencias, colWidths=[30, 450])
        tabla_ev.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elementos.append(Paragraph("📁 <b>Evidencias:</b>", styles['Heading3']))
        elementos.append(tabla_ev)
        elementos.append(Spacer(1, 0.2 * inch))

        # Imagen del árbol Merkle
        try:
            ruta_imagen = generar_imagen_arbol_merkle(bloque.evidencias)
            if os.path.exists(ruta_imagen):
                elementos.append(Paragraph("🌳 <b>Visualización del Árbol de Merkle:</b>", styles['Heading3']))
                elementos.append(Spacer(1, 0.1 * inch))
                elementos.append(Image(ruta_imagen, width=5.8 * inch, height=3.0 * inch))
                elementos.append(Spacer(1, 0.2 * inch))
        except Exception as e:
            elementos.append(Paragraph(f"⚠️ No se pudo generar la imagen del árbol Merkle: {str(e)}", styles['Normal']))
            elementos.append(Spacer(1, 0.1 * inch))

    else:
        elementos.append(Paragraph("⚠️ Este bloque no contiene evidencias.", styles['Normal']))
        elementos.append(Spacer(1, 0.1 * inch))

    # Tabla de Firmantes
    if bloque.firmantes:
        firmantes = [["Usuario", "Rol", "Fecha", "Firma (corto)"]]
        for f in bloque.firmantes:
            firma_corta = f["firma"][:20] + "..."
            firmantes.append([f["usuario"], f["rol"], f["fecha"], firma_corta])
        tabla_firmas = Table(firmantes, colWidths=[50, 100, 160, 300])
        tabla_firmas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
        ]))
        elementos.append(Paragraph("✍️ <b>Firmantes del bloque:</b>", styles['Heading3']))
        elementos.append(tabla_firmas)
    else:
        elementos.append(Paragraph("❌ Este bloque no ha sido firmado aún.", styles['Normal']))

    # Pie de página con número de bloque y fecha
   

    return elementos
