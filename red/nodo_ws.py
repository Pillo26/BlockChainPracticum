# red/nodo_ws.py

import asyncio
import json
import websockets
from blockchain.cadena import Blockchain
from blockchain.bloque import Bloque

PUERTO = 8001
cadena = Blockchain()

nodos_conectados = set()

async def recibir_bloque(websocket, _):
    """
    Manejador principal que recibe bloques y los valida.
    """
    nodos_conectados.add(websocket)
    try:
        async for mensaje in websocket:
            datos = json.loads(mensaje)
            if datos.get("tipo") == "bloque":
                bloque_dict = datos["contenido"]
                print(f"\n📥 Bloque recibido desde otro nodo.")

                # Convertir el dict a objeto Bloque
                bloque = Bloque(
                    id_caso=bloque_dict['id_caso'],
                    entidad=bloque_dict['entidad'],
                    evidencias=bloque_dict['evidencias'],
                    firmantes=bloque_dict['firmantes'],
                    validadores=bloque_dict['validadores'],
                    hash_anterior=bloque_dict['hash_anterior'],
                    fiscal_responsable=bloque_dict['fiscal_responsable']
                )
                bloque.timestamp = bloque_dict['timestamp']
                bloque.hash_bloque = bloque_dict['hash_bloque']
                bloque.merkle_root = bloque_dict['merkle_root']

                # Validar y agregar
                if cadena.agregar_bloque(bloque, umbral_firmas=2):
                    print("✅ Bloque válido y agregado.")
                else:
                    print("❌ Bloque inválido o sin suficientes firmas.")
    except Exception as e:
        print(f"⚠️ Error en conexión: {e}")
    finally:
        nodos_conectados.discard(websocket)

def iniciar_servidor():
    print(f"🌐 Nodo escuchando en puerto {PUERTO}")
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(recibir_bloque, "localhost", PUERTO)
    )
    asyncio.get_event_loop().run_forever()
