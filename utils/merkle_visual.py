# utils/merkle_visual.py

from PIL import Image, ImageDraw, ImageFont
import os
from blockchain.merkle import construir_arbol_merkle

def generar_imagen_arbol_merkle(evidencias, ruta="merkle_temp.png"):
    niveles = construir_arbol_merkle(evidencias)

    ancho_img = 1000
    alto_por_nivel = 120
    alto_img = alto_por_nivel * len(niveles)
    radio = 10

    img = Image.new("RGB", (ancho_img, alto_img), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    posiciones = {}

    for nivel_idx, nivel in enumerate(niveles):
        y = alto_por_nivel * nivel_idx + 50
        espacios = ancho_img // (len(nivel) + 1)
        for i, hash_val in enumerate(nivel):
            x = espacios * (i + 1)
            posiciones[(nivel_idx, i)] = (x, y)
            draw.ellipse((x - radio, y - radio, x + radio, y + radio), fill="lightblue", outline="black")
            draw.text((x - 30, y + 15), hash_val[:8], font=font, fill="black")

    # Dibujar líneas
    for nivel_idx in range(len(niveles) - 1):
        for i in range(len(niveles[nivel_idx])):
            padre_idx = i // 2
            x1, y1 = posiciones[(nivel_idx, i)]
            x2, y2 = posiciones[(nivel_idx + 1, padre_idx)]
            draw.line((x1, y1, x2, y2), fill="gray", width=1)

    img.save(ruta)
    return ruta
