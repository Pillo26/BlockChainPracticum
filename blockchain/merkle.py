# blockchain/merkle.py

import hashlib

def sha256(data: str) -> str:
    """
    Devuelve el hash SHA-256 de una cadena como hexadecimal.
    """
    return hashlib.sha256(data.encode()).hexdigest()

def calcular_merkle_root(hashes):
    """
    Calcula la raíz Merkle a partir de una lista de hashes.
    """
    if not hashes:
        return None  # No hay evidencias

    # Copia la lista para no modificarla directamente
    nivel_actual = hashes[:]

    while len(nivel_actual) > 1:
        nuevo_nivel = []

        # Combinar en pares
        for i in range(0, len(nivel_actual), 2):
            izquierda = nivel_actual[i]
            # Si no hay par, duplica el último
            derecha = nivel_actual[i + 1] if i + 1 < len(nivel_actual) else izquierda

            combinado = izquierda + derecha
            nuevo_nivel.append(sha256(combinado))

        nivel_actual = nuevo_nivel

    # Al final queda solo un hash
    return nivel_actual[0]
