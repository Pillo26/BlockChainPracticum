from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QTabWidget, QTextEdit
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
from gui.widgets.ventana_blockchain import VentanaBlockchain
from gui.widgets.configuracion_widget import ConfiguracionWidget
from utils.bitacora import registrar_log, leer_logs
from blockchain.merkle import construir_arbol_merkle
from utils.nodos import leer_nodos
from gui.widgets.disputa_widget import DisputaWidget





class VentanaPrincipal(QMainWindow):
    def __init__(self, callback_logout):
        super().__init__()
        self.setWindowTitle("Blockchain Judicial - Evidencias")
        self.setGeometry(100, 100, 900, 600)
        self.callback_logout = callback_logout

        # Leer configuración del usuario
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

        # Sistema de pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.pestana_evidencias = QWidget()
        self.pestana_config = ConfiguracionWidget()
        self.pestana_bitacora = QWidget()
        self.pestana_merkle = QWidget()

        self.tabs.addTab(self.pestana_evidencias, "📁 Evidencias")
        self.tabs.addTab(self.pestana_config, "⚙️ Configuración")
        self.tabs.addTab(self.pestana_bitacora, "📝 Bitácora")
        self.tabs.addTab(self.pestana_merkle, "🌿 Árbol de Merkle")
        self.pestana_disputa = DisputaWidget(self.blockchain, self.usuario_actual, self.rol_actual)
        self.tabs.addTab(self.pestana_disputa, "⚖️ Disputa legal")


        # Layout para pestaña Evidencias
        self.layout = QVBoxLayout(self.pestana_evidencias)

        botones_superiores = QHBoxLayout()
        self.boton_ver_blockchain = QPushButton("🔎 Ver blockchain minada")
        self.boton_ver_blockchain.clicked.connect(self.abrir_ventana_blockchain)
        botones_superiores.addWidget(self.boton_ver_blockchain)

        self.boton_logout = QPushButton("🔒 Cerrar sesión")
        self.boton_logout.clicked.connect(self.cerrar_sesion)
        botones_superiores.addWidget(self.boton_logout)
        self.layout.addLayout(botones_superiores)

        self.label_estado = QLabel(f"Usuario: {self.usuario_actual} | Rol: {self.rol_actual}")
        self.layout.addWidget(self.label_estado)

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



        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Archivo", "Hash", "Entidad", "Fecha", "Firmas", "Estado"])
        self.tabla.itemSelectionChanged.connect(self.actualizar_barra_progreso)
        self.layout.addWidget(self.tabla)

        self.barra_firmas = BarraProgresoFirmas(total_firmas=3)
        self.layout.addWidget(self.barra_firmas)

        self.pestana_evidencias.setLayout(self.layout)

        # Layout para Bitácora
        self.texto_bitacora = QTextEdit()
        self.texto_bitacora.setReadOnly(True)
        layout_bitacora = QVBoxLayout()
        layout_bitacora.addWidget(QLabel("📝 Registro de acciones"))
        layout_bitacora.addWidget(self.texto_bitacora)
        self.pestana_bitacora.setLayout(layout_bitacora)


        self.pestana_nodos = QWidget()
        self.tabs.addTab(self.pestana_nodos, "🔐 Nodos autorizados")
        self.setup_pestana_nodos()

        # Layout para Árbol de Merkle
        self.texto_merkle = QTextEdit()
        self.texto_merkle.setReadOnly(True)
        layout_merkle = QVBoxLayout()
        layout_merkle.addWidget(QLabel("🌿 Estructura del Árbol de Merkle"))
        layout_merkle.addWidget(self.texto_merkle)
        self.pestana_merkle.setLayout(layout_merkle)        

        self.actualizar_tabla()
        self.cargar_bitacora()

    def mostrar_arbol_merkle(self):
        hashes = [ev.hash_archivo for ev in self.evidencias]
        niveles = construir_arbol_merkle(hashes)

        texto = ""
        for nivel, nodos in enumerate(niveles):
            texto += f"Nivel {nivel} (nodos: {len(nodos)}):\n"
            for h in nodos:
                texto += f"  {h}\n"
            texto += "\n"

        self.texto_merkle.setPlainText(texto)



    def abrir_ventana_blockchain(self):
        self.ventana_blockchain = VentanaBlockchain()
        self.ventana_blockchain.show()

    def cerrar_sesion(self):
        self.close()
        self.callback_logout()

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
            registrar_log(self.usuario_actual, self.rol_actual, "Subió evidencia", archivo=nombre)
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
            registrar_log(self.usuario_actual, self.rol_actual, "Firmó evidencia", archivo=evidencia.nombre_archivo)
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
        registrar_log(self.usuario_actual, self.rol_actual, "Validó archivo", archivo=os.path.basename(archivo), extra="válido" if encontrado else "no válido")
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
        self.mostrar_arbol_merkle()

    def actualizar_barra_progreso(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            evidencia = self.evidencias[fila]
            self.barra_firmas.total_firmas = evidencia.total_firmas
            self.barra_firmas.setMaximum(evidencia.total_firmas)
            self.barra_firmas.actualizar_firmas(len(evidencia.firmantes))
        else:
            self.barra_firmas.reiniciar()

    def cargar_bitacora(self):
        logs = leer_logs()
        texto = "\n\n".join(
            f"[{l['timestamp']}] {l['usuario']} ({l['rol']}): {l['accion']}"
            + (f" → {l['archivo']}" if l['archivo'] else "")
            + (f" ({l['extra']})" if l['extra'] else "")
            for l in logs
        )
        self.texto_bitacora.setPlainText(texto)

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

            mensaje = "✅ Se minó un nuevo bloque con las siguientes evidencias:\n\n"
            for ev in nuevo_bloque.evidencias:
                registrar_log(
                    self.usuario_actual,
                    self.rol_actual,
                    "Minó bloque con evidencia",
                    archivo=ev,
                    extra="Evidencia alcanzó el umbral de firmas"
                )
                mensaje += f"• {ev[:10]}...\n"

            QMessageBox.information(self, "Bloque minado", mensaje)

            self.evidencias = []
            guardar_mempool([])
            self.actualizar_tabla()
            self.label_estado.setText("✅ Bloque minado y registrado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error al minar bloque", f"No se pudo minar: {e}")



    def setup_pestana_nodos(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔐 Lista de nodos autorizados:"))

        self.tabla_nodos = QTableWidget()
        self.tabla_nodos.setColumnCount(3)
        self.tabla_nodos.setHorizontalHeaderLabels(["Nombre", "Rol", "Clave pública (corto)"])
        layout.addWidget(self.tabla_nodos)

        self.pestana_nodos.setLayout(layout)
        self.actualizar_tabla_nodos()

    def actualizar_tabla_nodos(self):
        nodos = leer_nodos()
        self.tabla_nodos.setRowCount(len(nodos))
        for i, nodo in enumerate(nodos):
            self.tabla_nodos.setItem(i, 0, QTableWidgetItem(nodo["nombre"]))
            self.tabla_nodos.setItem(i, 1, QTableWidgetItem(nodo["rol"]))
            clave_corta = nodo["clave_publica"].replace("\n", "")[:40] + "..."
            self.tabla_nodos.setItem(i, 2, QTableWidgetItem(clave_corta))
