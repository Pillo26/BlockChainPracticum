import json
import os
from modelos.evidencia import Evidencia


RUTA_MEMPOOL = "datos/mempool.json"

def guardar_mempool(lista_evidencias):
    """
    Guarda las evidencias aún no minadas en un archivo JSON.
    Cada evidencia incluye su hash, metadatos y lista de firmantes.
    """
    serializable = []
    for ev in lista_evidencias:
        serializable.append({
            "nombre_archivo": ev.nombre_archivo,
            "hash_archivo": ev.hash_archivo,
            "entidad_origen": ev.entidad_origen,
            "fecha_subida": ev.fecha_subida,
            "firmantes": ev.firmantes
        })

    with open(RUTA_MEMPOOL, "w") as f:
        json.dump(serializable, f, indent=4)

def cargar_mempool():
    """
    Carga evidencias pendientes desde mempool.json.
    Si el archivo no existe o está vacío/malformado, devuelve una lista vacía.
    """
    if not os.path.exists(RUTA_MEMPOOL):
        return []

    try:
        with open(RUTA_MEMPOOL, "r") as f:
            contenido = f.read().strip()
            if not contenido:
                return []

            data = json.loads(contenido)

        evidencias = []
        for item in data:
            ev = Evidencia(
                nombre_archivo=item["nombre_archivo"],
                hash_archivo=item["hash_archivo"],
                entidad_origen=item["entidad_origen"],
                fecha_subida=item["fecha_subida"]
            )
            ev.firmantes = item.get("firmantes", [])
            evidencias.append(ev)

        return evidencias

    except Exception as e:
        print(f"⚠️ Error al cargar mempool: {e}")
        return []
