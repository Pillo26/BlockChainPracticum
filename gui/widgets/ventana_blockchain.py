# gui/widgets/ventana_blockchain.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import json
from datetime import datetime

class VentanaBlockchain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⛓️ Cadena de Bloques Minados")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout(self)

        self.texto = QTextEdit()
        self.texto.setReadOnly(True)

        btn_refrescar = QPushButton("🔄 Refrescar")
        btn_refrescar.clicked.connect(self.cargar_bloques)

        btn_limpiar = QPushButton("🧼 Limpiar bloques.json")
        btn_limpiar.clicked.connect(self.limpiar_bloques)

        layout.addWidget(btn_refrescar)
        layout.addWidget(btn_limpiar)
        layout.addWidget(self.texto)

        self.cargar_bloques()

    def cargar_bloques(self):
        try:
            with open("datos/bloques.json", "r") as f:
                bloques = json.load(f)

            if not bloques:
                self.texto.setText("⛓️ No hay bloques minados aún.")
                return

            texto = ""
            for i, b in enumerate(bloques):
                texto += (
                    f"🧱 Bloque {i}\n"
                    f"ID de Caso: {b.get('id_caso')}\n"
                    f"Entidad: {b.get('entidad')}\n"
                    f"Fecha: {datetime.fromtimestamp(b['timestamp'])}\n"
                    f"Hash: {b['hash_bloque'][:40]}...\n"
                    f"Merkle Root: {b['merkle_root'][:40]}...\n"
                    f"Evidencias: {len(b['evidencias'])}\n"
                    f"Firmantes: {[f['usuario'] for f in b['firmantes']]}\n"
                    f"{'-'*60}\n"
                )
            self.texto.setText(texto)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar bloques.json: {e}")

    def limpiar_bloques(self):
        confirmar = QMessageBox.question(self, "Confirmar", "¿Seguro que deseas borrar todos los bloques?")
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                with open("datos/bloques.json", "w") as f:
                    json.dump([], f, indent=4)
                self.texto.setText("✅ Bloques limpiados.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo limpiar bloques.json: {e}")
