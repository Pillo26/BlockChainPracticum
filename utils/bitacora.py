# utils/bitacora.py

import json
from datetime import datetime
import os

BITACORA_PATH = "datos/bitacora.jsonl"

def registrar_log(usuario, rol, accion, archivo=None, extra=None):
    entrada = {
        "usuario": usuario,
        "rol": rol,
        "accion": accion,
        "archivo": archivo,
        "extra": extra,
        "timestamp": datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(BITACORA_PATH), exist_ok=True)

    with open(BITACORA_PATH, "a") as f:
        f.write(json.dumps(entrada) + "\n")

def leer_logs():
    """
    Devuelve una lista de registros desde la bitácora en formato legible.
    """
    if not os.path.exists(BITACORA_PATH):
        return []

    registros = []
    with open(BITACORA_PATH, "r") as f:
        for linea in f:
            try:
                entrada = json.loads(linea)
                registros.append(entrada)
            except json.JSONDecodeError:
                continue
    return registros
