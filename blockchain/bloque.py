# blockchain/bloque.py

import hashlib
import json
import time
from blockchain.merkle import calcular_merkle_root

class Bloque:
    def __init__(self, id_caso, entidad, evidencias, firmantes=[], validadores=[], hash_anterior="", fiscal_responsable=""):
        """
        Constructor del bloque.
        """
        self.id_caso = id_caso
        self.entidad = entidad  # Fiscalía o Juzgado
        self.evidencias = evidencias  # Lista de hashes de evidencias
        self.timestamp = time.time()
        self.firmantes = firmantes  # Lista de dicts: {usuario, firma}
        self.validadores = validadores  # Lista de dicts o strings
        self.hash_anterior = hash_anterior
        self.fiscal_responsable = fiscal_responsable

        # Calcula la raíz Merkle a partir de los hashes de evidencias
        self.merkle_root = calcular_merkle_root(self.evidencias)

        # Se calcula al final con todos los datos (sin firma)
        self.hash_bloque = self.calcular_hash()

    def calcular_hash(self):
        """
        Genera el hash SHA-256 del bloque (excluyendo firmas).
        """
        bloque_str = json.dumps({
            'id_caso': self.id_caso,
            'entidad': self.entidad,
            'evidencias': self.evidencias,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'firmantes': [f['usuario'] for f in self.firmantes],
            'validadores': self.validadores,
            'hash_anterior': self.hash_anterior,
            'fiscal_responsable': self.fiscal_responsable
        }, sort_keys=True)

        return hashlib.sha256(bloque_str.encode()).hexdigest()

    def agregar_firma(self, usuario, firma):
        """
        Agrega una firma al bloque.
        """
        self.firmantes.append({
            'usuario': usuario,
            'firma': firma.hex()
        })

    def to_dict(self):
        """
        Convierte el bloque a un diccionario serializable.
        """
        return {
            'id_caso': self.id_caso,
            'entidad': self.entidad,
            'evidencias': self.evidencias,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'firmantes': self.firmantes,
            'validadores': self.validadores,
            'hash_anterior': self.hash_anterior,
            'fiscal_responsable': self.fiscal_responsable,
            'hash_bloque': self.hash_bloque
        }

    def to_json(self):
        """
        Devuelve el bloque en formato JSON.
        """
        return json.dumps(self.to_dict(), indent=4)
