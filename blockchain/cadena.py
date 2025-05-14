# blockchain/cadena.py

import json
import os
from blockchain.bloque import Bloque

RUTA_CADENA = "datos/bloques.json"

class Blockchain:
    def __init__(self):
        self.bloques = []
        self.cargar_cadena()

    def cargar_cadena(self):
        """
        Carga la cadena de bloques desde el archivo bloques.json
        """
        if os.path.exists(RUTA_CADENA):
            with open(RUTA_CADENA, 'r') as archivo:
                bloques_json = json.load(archivo)
                self.bloques = [self._bloque_desde_dict(b) for b in bloques_json]
                print(f"📥 Se cargaron {len(self.bloques)} bloques.")
        else:
            self.bloques = []

    def guardar_cadena(self):
        """
        Guarda la cadena de bloques en bloques.json
        """
        with open(RUTA_CADENA, 'w') as archivo:
            json.dump([b.to_dict() for b in self.bloques], archivo, indent=4)
        print("💾 Cadena de bloques guardada.")

    def agregar_bloque(self, bloque, umbral_firmas=2):
        """
        Agrega un bloque a la cadena si cumple con el número mínimo de firmas.
        """
        if len(bloque.firmantes) >= umbral_firmas:
            self.bloques.append(bloque)
            self.guardar_cadena()
            print(f"✅ Bloque agregado. Total bloques: {len(self.bloques)}")
            return True
        else:
            print(f"❌ Bloque rechazado: solo {len(bloque.firmantes)} firmas (requiere {umbral_firmas})")
            return False

    def es_valida(self):
        """
        Verifica la integridad de la cadena completa.
        """
        for i, bloque in enumerate(self.bloques):
            # Recalcular el hash del bloque desde su contenido actual
            hash_calculado = bloque.calcular_hash()
            

            if bloque.hash_bloque != hash_calculado:
                print(f"⚠️ Error: Hash del bloque alterado en posición {i}")
                print(f"    Esperado: {bloque.hash_bloque}")
                print(f"    Calculado: {hash_calculado}")
                return False

            if i > 0:
                hash_anterior_real = self.bloques[i - 1].hash_bloque
                if bloque.hash_anterior != hash_anterior_real:
                    print(f"⚠️ Error: hash_anterior no coincide en bloque {i}")
                return False

        print("🔐 Cadena de bloques válida.")
        return True

    def _bloque_desde_dict(self, datos):
        """
        Convierte un diccionario (desde JSON) a un objeto Bloque.
        """
        bloque = Bloque(
            id_caso=datos['id_caso'],
            entidad=datos['entidad'],
            evidencias=datos['evidencias'],
            firmantes=datos['firmantes'],
            validadores=datos['validadores'],
            hash_anterior=datos['hash_anterior'],
            fiscal_responsable=datos['fiscal_responsable']
        )
        bloque.timestamp = datos['timestamp']
        bloque.hash_bloque = datos['hash_bloque']
        bloque.merkle_root = datos['merkle_root']
        return bloque
