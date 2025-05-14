# crypto/firmas.py

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

def firmar_hash(hash_bytes, clave_privada):
    """
    Firma un hash utilizando ECDSA.
    hash_bytes: hash (bytes) a firmar.
    clave_privada: objeto de clave privada ECDSA.
    Retorna: firma en bytes.
    """
    firma = clave_privada.sign(
        hash_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    return firma

def verificar_firma(hash_bytes, firma, clave_publica):
    """
    Verifica una firma digital usando ECDSA.
    Retorna: True si es válida, False si no lo es.
    """
    try:
        clave_publica.verify(
            firma,
            hash_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
