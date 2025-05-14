from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import hashlib
import os
import json
from datetime import datetime
from crypto.llaves import cargar_llaves
from crypto.firmas import firmar_hash
from gui.widgets.barra_progreso import BarraProgresoFirmas
from blockchain.bloque import Bloque
from blockchain.cadena import Blockchain
from blockchain.mempool import cargar_mempool, guardar_mempool
from cryptography.hazmat.primitives import serialization
from modelos.evidencia import Evidencia



# GUI Principal
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blockchain Judicial - Evidencias")
        self.setGeometry(100, 100, 900, 600)

        # Leer configuración de usuario
        try:
            with open("datos/config_usuario.json", "r") as f:
                config = json.load(f)
                self.usuario_actual = config.get("usuario", "anonimo")
                self.rol_actual = config.get("rol", "desconocido")
                self.ruta_llaves = config.get("ruta_llaves", "datos/llaves_nodo.json")
        except Exception as e:
            QMessageBox.critical(self, "Error de configuración", f"No se pudo leer config_usuario.json: {e}")
            self.usuario_actual = "anonimo"
            self.rol_actual = "desconocido"
            self.ruta_llaves = "datos/llaves_nodo.json"

        self.blockchain = Blockchain()
        self.evidencias = cargar_mempool()

        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label_estado = QLabel(f"Usuario: {self.usuario_actual} | Rol: {self.rol_actual}")
        self.layout.addWidget(self.label_estado)

        # Botones
        self.boton_subir = QPushButton("Subir evidencia")
        self.boton_subir.clicked.connect(self.subir_evidencia)
        self.layout.addWidget(self.boton_subir)

        self.boton_firmar = QPushButton("Firmar evidencia seleccionada")
        self.boton_firmar.clicked.connect(self.firmar_evidencia)
        self.layout.addWidget(self.boton_firmar)

        self.boton_ver_firmas = QPushButton("Ver firmas de evidencia seleccionada")
        self.boton_ver_firmas.clicked.connect(self.ver_firmas_evidencia)
        self.layout.addWidget(self.boton_ver_firmas)

        self.boton_validar = QPushButton("Validar archivo local")
        self.boton_validar.clicked.connect(self.validar_integridad_archivo)
        self.layout.addWidget(self.boton_validar)

        # Tabla de evidencias
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Archivo", "Hash", "Entidad", "Fecha", "Firmas", "Estado"
        ])
        self.tabla.itemSelectionChanged.connect(self.actualizar_barra_progreso)
        self.layout.addWidget(self.tabla)

        # Barra de progreso
        self.barra_firmas = BarraProgresoFirmas(total_firmas=3)
        self.layout.addWidget(self.barra_firmas)

        self.actualizar_tabla()

    def subir_evidencia(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar evidencia")
        if archivo:
            nombre = os.path.basename(archivo)
            with open(archivo, 'rb') as f:
                hash_archivo = hashlib.sha256(f.read()).hexdigest()

            evidencia = Evidencia(
                nombre_archivo=nombre,
                hash_archivo=hash_archivo,
                entidad_origen=f"{self.rol_actual.title()} {self.usuario_actual}",
                fecha_subida=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            self.evidencias.append(evidencia)
            self.actualizar_tabla()
            guardar_mempool(self.evidencias)
            self.label_estado.setText(f"📂 Evidencia '{nombre}' cargada exitosamente.")

    def firmar_evidencia(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Advertencia", "Selecciona una evidencia para firmar.")
            return

        evidencia = self.evidencias[fila]
        if any(f["usuario"] == self.usuario_actual for f in evidencia.firmantes):
            QMessageBox.information(self, "Ya firmado", "Ya has firmado esta evidencia.")
            return

        try:
            clave_privada, clave_publica = cargar_llaves()
            firma = firmar_hash(bytes.fromhex(evidencia.hash_archivo), clave_privada)

            clave_publica_pem = clave_publica.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            evidencia.firmantes.append({
                "usuario": self.usuario_actual,
                "rol": self.rol_actual,
                "firma": firma.hex(),
                "fecha": datetime.now().isoformat(),
                "clave": clave_publica_pem
            })

            evidencia.firmado_por_mi = True
            self.actualizar_tabla()
            guardar_mempool(self.evidencias)
            self.label_estado.setText(f"✅ Evidencia '{evidencia.nombre_archivo}' firmada.")

            if all(ev.estado_bloque() == "Listo" for ev in self.evidencias):
                self.minar_bloque()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo firmar: {e}")

    def ver_firmas_evidencia(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Advertencia", "Selecciona una evidencia.")
            return

        evidencia = self.evidencias[fila]
        if not evidencia.firmantes:
            QMessageBox.information(self, "Sin firmas", "Esta evidencia aún no tiene firmas.")
            return

        detalles = ""
        for f in evidencia.firmantes:
            detalles += (
                f"🧾 Usuario: {f['usuario']}\n"
                f"🧑‍⚖️ Rol: {f['rol']}\n"
                f"📅 Fecha: {f['fecha']}\n"
                f"🔐 Clave pública (corto): {f['clave'][:30].replace(chr(10), '')}...\n"
                f"✍️ Firma (hex): {f['firma'][:30]}...\n"
                f"{'-'*40}\n"
            )

        QMessageBox.information(self, "Firmantes", detalles)

    def validar_integridad_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo a validar")
        if not archivo:
            return

        with open(archivo, 'rb') as f:
            hash_local = hashlib.sha256(f.read()).hexdigest()

        encontrado = any(hash_local in bloque.evidencias for bloque in self.blockchain.bloques)

        if encontrado:
            QMessageBox.information(self, "Validación exitosa", "✅ El archivo es auténtico y está en la blockchain.")
        else:
            QMessageBox.warning(self, "Alerta", "⚠️ El archivo NO coincide con ninguna evidencia registrada.")

    def actualizar_tabla(self):
        self.tabla.setRowCount(len(self.evidencias))
        for row, ev in enumerate(self.evidencias):
            self.tabla.setItem(row, 0, QTableWidgetItem(ev.nombre_archivo))
            self.tabla.setItem(row, 1, QTableWidgetItem(ev.hash_archivo[:10] + "..."))
            self.tabla.setItem(row, 2, QTableWidgetItem(ev.entidad_origen))
            self.tabla.setItem(row, 3, QTableWidgetItem(ev.fecha_subida))
            self.tabla.setItem(row, 4, QTableWidgetItem(ev.estatus_firmas()))
            self.tabla.setItem(row, 5, QTableWidgetItem(ev.estado_bloque()))
            for col in range(6):
                self.tabla.item(row, col).setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.actualizar_barra_progreso()

    def actualizar_barra_progreso(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            evidencia = self.evidencias[fila]
            self.barra_firmas.total_firmas = evidencia.total_firmas
            self.barra_firmas.setMaximum(evidencia.total_firmas)
            self.barra_firmas.actualizar_firmas(len(evidencia.firmantes))
        else:
            self.barra_firmas.reiniciar()

    def minar_bloque(self):
        if not self.evidencias:
            QMessageBox.information(self, "Sin evidencias", "No hay evidencias para minar.")
            return

        try:
            nuevo_bloque = Bloque(
                evidencias=[ev.hash_archivo for ev in self.evidencias],
                firmantes=[f for ev in self.evidencias for f in ev.firmantes],
                entidad=self.rol_actual,
                fiscal_responsable=self.usuario_actual,
                id_caso="CASO-DEMO-001"
            )

            self.blockchain.agregar_bloque(nuevo_bloque)
            self.blockchain.guardar_cadena()

            self.evidencias = []
            guardar_mempool([])
            self.actualizar_tabla()
            self.label_estado.setText("✅ Bloque minado y registrado exitosamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error al minar bloque", f"No se pudo minar: {e}")
