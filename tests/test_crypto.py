# tests/test_crypto.py

import hashlib
from crypto.llaves import generar_llaves, cargar_llaves
from crypto.firmas import firmar_hash, verificar_firma

def test_firma_valida():
    print("\n🧪 Test: Firma válida")

    # Paso 1: Generar y cargar llaves
    generar_llaves()
    clave_privada, clave_publica = cargar_llaves()

    # Paso 2: Crear hash simulado de un mensaje (ej. archivo)
    mensaje = b"Hola, soy una evidencia digital"
    hash_bytes = hashlib.sha256(mensaje).digest()

    # Paso 3: Firmar el hash
    firma = firmar_hash(hash_bytes, clave_privada)
    print("🔏 Firma generada.")

    # Paso 4: Verificar la firma
    valido = verificar_firma(hash_bytes, firma, clave_publica)
    print(f"✅ ¿Firma válida? {valido}")

    assert valido is True

def test_firma_invalida():
    print("\n🧪 Test: Firma inválida")

    _, clave_publica = cargar_llaves()

    # Hash original firmado (no tenemos la firma real)
    mensaje = b"Mensaje original"
    hash_original = hashlib.sha256(mensaje).digest()

    # Hash alterado
    mensaje_alterado = b"Mensaje alterado"
    hash_alterado = hashlib.sha256(mensaje_alterado).digest()

    # Firma falsa (solo como ejemplo, no es válida)
    firma_falsa = b"firma_invalida"

    # Verificación debe fallar
    valido = verificar_firma(hash_alterado, firma_falsa, clave_publica)
    print(f"❌ ¿Firma falsa válida? {valido}")

    assert valido is False

if __name__ == "__main__":
    test_firma_valida()
    test_firma_invalida()
