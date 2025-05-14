# utils/nodos.py

import json
import os

RUTA_NODOS = "datos/nodos_autorizados.json"

def registrar_nodo(nombre, rol, clave_publica):
    if not os.path.exists(RUTA_NODOS):
        nodos = []
    else:
        with open(RUTA_NODOS, "r") as f:
            nodos = json.load(f)

    # Evitar duplicados por nombre
    if any(nodo["nombre"] == nombre for nodo in nodos):
        return

    nodos.append({
        "nombre": nombre,
        "rol": rol,
        "clave_publica": clave_publica
    })

    with open(RUTA_NODOS, "w") as f:
        json.dump(nodos, f, indent=4)

def leer_nodos():
    if not os.path.exists(RUTA_NODOS):
        return []
    try:
        with open(RUTA_NODOS, "r") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except Exception as e:
        print(f"[⚠️] Error leyendo nodos autorizados: {e}")
        return []


def obtener_nodos_autorizados():
    if os.path.exists(RUTA_NODOS):
        with open(RUTA_NODOS, "r") as f:
            return json.load(f)
    return {}
