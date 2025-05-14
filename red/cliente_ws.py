# red/cliente_ws.py

import asyncio
import websockets
import json

async def enviar_bloque(bloque_json, ip="localhost", puerto=8001):
    uri = f"ws://{ip}:{puerto}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "tipo": "bloque",
            "contenido": bloque_json
        }))
        print("📤 Bloque enviado al nodo.")

# Solo para pruebas manuales:
# from blockchain.bloque import Bloque
# bloque = Bloque(...)
# asyncio.run(enviar_bloque(bloque.to_dict()))
