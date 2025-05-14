# gui/login.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QTabWidget, QMessageBox, QComboBox
)
import json
import os
from crypto.llaves import generar_llaves
from utils.nodos import registrar_nodo

USUARIOS_PATH = "datos/usuarios.json"

class LoginWidget(QWidget):
    def __init__(self, callback_login_exitoso):
        super().__init__()
        self.setWindowTitle("Acceso al sistema")
        self.callback_login_exitoso = callback_login_exitoso  # función para redirigir al dashboard

        self.tabs = QTabWidget()
        self.tab_login = QWidget()
        self.tab_crear = QWidget()

        self.tabs.addTab(self.tab_login, "Iniciar sesión")
        self.tabs.addTab(self.tab_crear, "Crear cuenta")

        self.init_login_tab()
        self.init_crear_tab()

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

    def init_login_tab(self):
        layout = QVBoxLayout()

        self.login_usuario = QLineEdit()
        self.login_usuario.setPlaceholderText("Usuario")

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Contraseña")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_ingresar = QPushButton("Iniciar sesión")
        btn_ingresar.clicked.connect(self.verificar_credenciales)

        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.login_usuario)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.login_password)
        layout.addWidget(btn_ingresar)

        self.tab_login.setLayout(layout)

    def init_crear_tab(self):
        layout = QVBoxLayout()

        self.crear_usuario = QLineEdit()
        self.crear_usuario.setPlaceholderText("Nuevo usuario")

        self.crear_password = QLineEdit()
        self.crear_password.setPlaceholderText("Contraseña")
        self.crear_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.crear_rol = QComboBox()
        self.crear_rol.addItems(["perito", "fiscal", "abogado defensor"])

        btn_crear = QPushButton("Crear cuenta")
        btn_crear.clicked.connect(self.crear_cuenta)

        layout.addWidget(QLabel("Nuevo usuario:"))
        layout.addWidget(self.crear_usuario)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.crear_password)
        layout.addWidget(QLabel("Rol:"))
        layout.addWidget(self.crear_rol)
        layout.addWidget(btn_crear)

        self.tab_crear.setLayout(layout)

    def verificar_credenciales(self):
        usuario = self.login_usuario.text()
        contraseña = self.login_password.text()

        if not os.path.exists(USUARIOS_PATH):
            QMessageBox.warning(self, "Error", "No hay usuarios registrados.")
            return

        with open(USUARIOS_PATH, "r") as f:
            usuarios = json.load(f)

        if usuario in usuarios and usuarios[usuario]["password"] == contraseña:
            config = {
                "usuario": usuario,
                "rol": usuarios[usuario]["rol"],
                "ruta_llaves": f"datos/llaves_{usuario}.json"
            }
            with open("datos/config_usuario.json", "w") as f:
                json.dump(config, f, indent=4)
            self.callback_login_exitoso()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def crear_cuenta(self):
        usuario = self.crear_usuario.text()
        password = self.crear_password.text()
        rol = self.crear_rol.currentText()

        if not usuario or not password:
            QMessageBox.warning(self, "Campos incompletos", "Todos los campos son obligatorios.")
            return

        usuarios = {}
        if os.path.exists(USUARIOS_PATH):
            with open(USUARIOS_PATH, "r") as f:
                usuarios = json.load(f)

        if usuario in usuarios:
            QMessageBox.warning(self, "Ya existe", "Ese usuario ya está registrado.")
            return

        usuarios[usuario] = {
            "password": password,
            "rol": rol
        }

        with open(USUARIOS_PATH, "w") as f:
            json.dump(usuarios, f, indent=4)

        ruta_llaves = f"datos/llaves_{usuario}.json"
        generar_llaves(nombre_archivo=ruta_llaves)

        # Registrar nodo con clave pública
        try:
            with open(ruta_llaves, "r") as f:
                llaves = json.load(f)
                clave_publica = llaves["clave_publica"]
                registrar_nodo(usuario, rol, clave_publica)
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"No se pudo registrar el nodo en nodos_autorizados.json: {e}")

        QMessageBox.information(self, "Éxito", "Cuenta creada, llaves generadas y nodo registrado.")
