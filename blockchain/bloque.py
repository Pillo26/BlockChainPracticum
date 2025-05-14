# blockchain/bloque.py

import hashlib
import json
import time
from blockchain.merkle import calcular_merkle_root

class Bloque:
    def __init__(self, id_caso, entidad, evidencias, firmantes=[], validadores=[], hash_anterior="", fiscal_responsable="", timestamp=None, merkle_root=None, hash_bloque=None):
        """
        Constructor del bloque.
        """
        self.id_caso = id_caso
        self.entidad = entidad  # Fiscalía o Juzgado
        self.evidencias = evidencias  # Lista de hashes de evidencias
        self.timestamp = timestamp if timestamp else time.time()
        self.firmantes = firmantes  # Lista de dicts: {usuario, firma}
        self.validadores = validadores  # Lista de dicts o strings
        self.hash_anterior = hash_anterior
        self.fiscal_responsable = fiscal_responsable

        # Calcula la raíz Merkle a partir de los hashes de evidencias
        self.merkle_root = merkle_root if merkle_root else calcular_merkle_root(self.evidencias)

        # Se calcula al final con todos los datos (sin firma)
        self.hash_bloque = hash_bloque if hash_bloque else self.calcular_hash()

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
    @classmethod
    def from_dict(cls, data):
        """
        Crea un bloque a partir de un diccionario (como los del archivo JSON).
        """
        return cls(
            id_caso=data.get("id_caso"),
            entidad=data.get("entidad"),
            evidencias=data.get("evidencias", []),
            firmantes=data.get("firmantes", []),
            validadores=data.get("validadores", []),
            hash_anterior=data.get("hash_anterior", ""),
            fiscal_responsable=data.get("fiscal_responsable", ""),
            timestamp=data.get("timestamp"),
            merkle_root=data.get("merkle_root"),
            hash_bloque=data.get("hash_bloque")
        )