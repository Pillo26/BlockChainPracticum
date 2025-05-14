# gui/widgets/barra_progreso.py

from PyQt6.QtWidgets import QProgressBar

class BarraProgresoFirmas(QProgressBar):
    def __init__(self, total_firmas, parent=None):
        super().__init__(parent)
        self.total_firmas = total_firmas
        self.setMinimum(0)
        self.setMaximum(total_firmas)
        self.setValue(0)
        self.setFormat("Firmas: %v de %m")
        self.setTextVisible(True)

    def actualizar_firmas(self, firmas_actuales):
        self.setValue(firmas_actuales)

    def reiniciar(self):
        self.setValue(0)
