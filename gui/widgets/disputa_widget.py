# gui/widgets/disputa_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
)
import os
import hashlib
from utils.bitacora import registrar_log

class DisputaWidget(QWidget):
    def __init__(self, blockchain, usuario, rol):
        super().__init__()
        self.blockchain = blockchain
        self.usuario = usuario
        self.rol = rol

        layout = QVBoxLayout()

        self.label_info = QLabel("🔍 Compara un archivo con la blockchain para detectar alteraciones.")
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)

        self.boton_cargar = QPushButton("📛 Seleccionar archivo en disputa")
        self.boton_cargar.clicked.connect(self.analizar_archivo)

        layout.addWidget(self.label_info)
        layout.addWidget(self.boton_cargar)
        layout.addWidget(self.resultado_texto)
        self.setLayout(layout)

    def analizar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo en disputa")
        if not archivo:
            return

        with open(archivo, "rb") as f:
            contenido = f.read()
            hash_archivo = hashlib.sha256(contenido).hexdigest()

        encontrado = any(hash_archivo in bloque.evidencias for bloque in self.blockchain.bloques)
        resultado = "coincide" if encontrado else "alterado"
        registrar_log(self.usuario, self.rol, "Simuló disputa legal", archivo=os.path.basename(archivo), extra=resultado)

        texto = (
            f"📂 Archivo: {os.path.basename(archivo)}\n"
            f"🔢 Hash SHA-256: {hash_archivo}\n"
            f"📊 Resultado: {'✅ Coincide con una evidencia registrada.' if encontrado else '🚨 Posible alteración detectada. No coincide.'}"
        )
        self.resultado_texto.setPlainText(texto)
