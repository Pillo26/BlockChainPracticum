# tests/test_cadena.py

import hashlib
from blockchain.bloque import Bloque
from blockchain.cadena import Blockchain
from crypto.llaves import generar_llaves, cargar_llaves
from crypto.firmas import firmar_hash, verificar_firma

def generar_hash_falso(nombre_archivo):
    """
    Simula el hash SHA-256 de un archivo.
    """
    return hashlib.sha256(nombre_archivo.encode()).hexdigest()

def test_blockchain():
    print("\n🧪 Test: Cadena de bloques judicial")

    # Paso 1: Preparar la cadena
    cadena = Blockchain()

    # Paso 2: Simular evidencias
    evidencias = [
        generar_hash_falso("foto1.png"),
        generar_hash_falso("audio1.wav"),
        generar_hash_falso("reporte.pdf")
    ]

    # Paso 3: Crear el bloque
    hash_anterior = cadena.bloques[-1].hash_bloque if cadena.bloques else "0" * 64

    bloque = Bloque(
        id_caso="CASO-456",
        entidad="Juzgado Penal",
        evidencias=evidencias,
        firmantes=[],
        validadores=["juez2"],
        hash_anterior=hash_anterior,
        fiscal_responsable="Juez Y"
    )

    # Paso 4: Firmar el bloque dos veces (M=2)
    generar_llaves()
    clave_privada, clave_publica = cargar_llaves()

    for i in range(2):  # Firmas suficientes
        firma = firmar_hash(bytes.fromhex(bloque.hash_bloque), clave_privada)
        bloque.agregar_firma(f"firmante_{i+1}", firma)

    # Paso 5: Agregar bloque a la cadena
    agregado = cadena.agregar_bloque(bloque, umbral_firmas=2)
    assert agregado

    # Paso 6: Validar cadena
    assert not cadena.es_valida()

    # Paso 7: Simular alteración
    print("\n🔧 Simulando alteración de evidencia...")
    cadena.bloques[-1].evidencias[0] = "hash_modificado"
    assert not cadena.es_valida()

if __name__ == "__main__":
    test_blockchain()
