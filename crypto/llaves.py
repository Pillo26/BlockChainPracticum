# crypto/llaves.py

import os
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Ruta donde se almacenarán las llaves del nodo
RUTA_LLAVES = "datos/llaves_nodo.json"

def generar_llaves():
    """
    Genera un par de llaves ECDSA (privada y pública) y las guarda en formato PEM.
    """
    # Generar clave privada
    clave_privada = ec.generate_private_key(ec.SECP256R1())

    # Derivar clave pública
    clave_publica = clave_privada.public_key()

    # Serializar a formato PEM (texto legible)
    privada_pem = clave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    publica_pem = clave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    # Guardar en archivo JSON
    with open(RUTA_LLAVES, 'w') as archivo:
        json.dump({
            'clave_privada': privada_pem,
            'clave_publica': publica_pem
        }, archivo, indent=4)

    print("🔐 Llaves ECDSA generadas y guardadas exitosamente.")

def cargar_llaves():
    """
    Carga las llaves ECDSA desde archivo JSON.
    Retorna: (clave_privada, clave_publica)
    """
    if not os.path.exists(RUTA_LLAVES):
        raise FileNotFoundError("No se encontraron llaves. Genera primero con generar_llaves().")

    with open(RUTA_LLAVES, 'r') as archivo:
        datos = json.load(archivo)

    clave_privada = serialization.load_pem_private_key(
        datos['clave_privada'].encode(), password=None
    )
    clave_publica = serialization.load_pem_public_key(
        datos['clave_publica'].encode()
    )

    return clave_privada, clave_publica
