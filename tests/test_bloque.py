# tests/test_bloque.py

import hashlib
import json

from blockchain.bloque import Bloque
from crypto.llaves import generar_llaves, cargar_llaves
from crypto.firmas import firmar_hash, verificar_firma

def generar_hash_falso(nombre_archivo):
    """
    Simula el hash de un archivo.
    """
    return hashlib.sha256(nombre_archivo.encode()).hexdigest()

def test_crear_bloque():
    print("\n🧪 Test: Crear bloque judicial")

    # Simular evidencias
    evidencias = [
        generar_hash_falso("evidencia1.pdf"),
        generar_hash_falso("foto1.jpg"),
        generar_hash_falso("audio1.mp3")
    ]

    # Crear el bloque
    bloque = Bloque(
        id_caso="CASO-123",
        entidad="Fiscalía Anticorrupción",
        evidencias=evidencias,
        firmantes=[],
        validadores=["juez1"],
        hash_anterior="00000abcde12345",
        fiscal_responsable="Fiscal X"
    )

    print("🧱 Hash del bloque:", bloque.hash_bloque)
    print("🌳 Merkle Root:", bloque.merkle_root)

    # Firmar el bloque con la clave privada
    generar_llaves()  # Se sobrescribe para la prueba
    clave_privada, clave_publica = cargar_llaves()

    hash_bytes = bytes.fromhex(bloque.hash_bloque)
    firma = firmar_hash(hash_bytes, clave_privada)

    # Agregar la firma
    bloque.agregar_firma("fiscal_x", firma)

    # Verificar la firma
    es_valida = verificar_firma(hash_bytes, firma, clave_publica)
    print(f"✅ ¿Firma válida en bloque?: {es_valida}")
    assert es_valida

    # Ver JSON del bloque
    bloque_json = bloque.to_json()
    print("\n📦 Bloque en JSON:")
    print(bloque_json)

if __name__ == "__main__":
    test_crear_bloque()


