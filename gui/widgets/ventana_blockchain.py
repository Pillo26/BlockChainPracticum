# gui/widgets/ventana_blockchain.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox, QInputDialog
import json
from datetime import datetime
from utils.pdf_export import exportar_bloque_pdf, exportar_cadena_pdf
from blockchain.bloque import Bloque


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

        btn_exportar_ultimo = QPushButton("📤 Exportar último bloque a PDF")
        btn_exportar_ultimo.clicked.connect(self.exportar_ultimo_bloque)

        btn_exportar_por_indice = QPushButton("📤 Exportar bloque por número")
        btn_exportar_por_indice.clicked.connect(self.exportar_bloque_por_indice)


        btn_exportar_cadena = QPushButton("📚 Exportar cadena completa a PDF")
        btn_exportar_cadena.clicked.connect(self.exportar_toda_la_cadena)

        layout.addWidget(btn_refrescar)
        layout.addWidget(btn_limpiar)
        layout.addWidget(btn_exportar_ultimo)
        layout.addWidget(btn_exportar_por_indice)
        layout.addWidget(btn_exportar_cadena)
        layout.addWidget(self.texto)

        self.bloques_data = []
        self.cargar_bloques()

    def cargar_bloques(self):
        try:
            with open("datos/bloques.json", "r") as f:
                self.bloques_data = json.load(f)

            if not self.bloques_data:
                self.texto.setText("⛓️ No hay bloques minados aún.")
                return

            texto = ""
            for i, b in enumerate(self.bloques_data):
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

    def exportar_ultimo_bloque(self):
        if not self.bloques_data:
            QMessageBox.warning(self, "Sin bloques", "No hay bloques minados aún.")
            return
        try:
            bloque_dict = self.bloques_data[-1]
            bloque = Bloque.from_dict(bloque_dict)
            ruta = exportar_bloque_pdf(bloque)
            QMessageBox.information(self, "Exportación exitosa", f"✅ PDF exportado a:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el PDF: {e}")

    def exportar_bloque_por_indice(self):
        if not self.bloques_data:
            QMessageBox.warning(self, "Sin bloques", "No hay bloques disponibles para exportar.")
            return

        idx, ok = QInputDialog.getInt(self, "Exportar a PDF", "Selecciona el número de bloque (0 a N):", 0, 0, len(self.bloques_data) - 1)
        if ok:
            try:
                bloque_dict = self.bloques_data[idx]
                bloque = Bloque.from_dict(bloque_dict)
                ruta = exportar_bloque_pdf(bloque)
                QMessageBox.information(self, "Éxito", f"📄 PDF generado en:\n{ruta}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el PDF: {e}")


    def exportar_toda_la_cadena(self):
        if not self.bloques_data:
            QMessageBox.warning(self, "Sin bloques", "No hay bloques para exportar.")
            return
        try:
            bloques_objetos = [Bloque.from_dict(b) for b in self.bloques_data]
            ruta = exportar_cadena_pdf(bloques_objetos)
            QMessageBox.information(self, "Éxito", f"📚 Cadena completa exportada a:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar la cadena: {e}")



    def limpiar_bloques(self):
        confirmar = QMessageBox.question(self, "Confirmar", "¿Seguro que deseas borrar todos los bloques?")
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                with open("datos/bloques.json", "w") as f:
                    json.dump([], f, indent=4)
                self.bloques_data = []
                self.texto.setText("✅ Bloques limpiados.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo limpiar bloques.json: {e}")
