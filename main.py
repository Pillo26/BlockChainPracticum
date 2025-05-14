from PyQt6.QtWidgets import QApplication
import sys
from gui.login import LoginWidget
from gui.ventana_principal import VentanaPrincipal

app = QApplication(sys.argv)

# Referencias globales
ventana_login = None
ventana_principal = None

def mostrar_login():
    global ventana_login, ventana_principal
    if ventana_principal:
        ventana_principal.close()
    ventana_login = LoginWidget(callback_login_exitoso=mostrar_principal)
    ventana_login.show()

def mostrar_principal():
    global ventana_login, ventana_principal
    if ventana_login:
        ventana_login.close()
    ventana_principal = VentanaPrincipal(callback_logout=mostrar_login)
    ventana_principal.show()

mostrar_login()
sys.exit(app.exec())
