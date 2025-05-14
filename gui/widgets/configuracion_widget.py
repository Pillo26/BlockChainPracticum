# gui/widgets/configuracion_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox
)
import os
import json
import sys

class ConfiguracionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        btn_limpiar_bloques = QPushButton("🧹 Limpiar bloques.json")
        btn_limpiar_bloques.clicked.connect(self.limpiar_bloques)
        layout.addWidget(btn_limpiar_bloques)

        btn_limpiar_usuarios = QPushButton("🧼 Limpiar usuarios.json")
        btn_limpiar_usuarios.clicked.connect(self.limpiar_usuarios)
        layout.addWidget(btn_limpiar_usuarios)

        btn_cerrar_sesion = QPushButton("🔒 Cerrar sesión")
        btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(btn_cerrar_sesion)

        self.setLayout(layout)

    def limpiar_bloques(self):
        try:
            with open("datos/bloques.json", "w") as f:
                json.dump([], f, indent=4)
            QMessageBox.information(self, "Éxito", "✅ bloques.json ha sido limpiado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo limpiar bloques.json:\n{e}")

    def limpiar_usuarios(self):
        respuesta = QMessageBox.question(
            self,
            "Confirmar limpieza",
            "⚠️ ¿Estás seguro de que quieres eliminar todos los usuarios registrados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                with open("datos/usuarios.json", "w") as f:
                    json.dump({}, f, indent=4)
                QMessageBox.information(self, "Éxito", "✅ usuarios.json ha sido limpiado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo limpiar usuarios.json:\n{e}")

    def cerrar_sesion(self):
        try:
            # Limpia config_usuario.json
            with open("datos/config_usuario.json", "w") as f:
                json.dump({}, f)
            QMessageBox.information(self, "Cierre de sesión", "Has cerrado sesión.")
            os.execl(sys.executable, sys.executable, *sys.argv)  # reinicia la app
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cerrar sesión:\n{e}")
