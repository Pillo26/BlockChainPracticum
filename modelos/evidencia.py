class Evidencia:
    def __init__(self, nombre_archivo, hash_archivo, entidad_origen, fecha_subida):
        self.nombre_archivo = nombre_archivo
        self.hash_archivo = hash_archivo
        self.entidad_origen = entidad_origen
        self.fecha_subida = fecha_subida
        self.firmantes = []
        self.total_firmas = 3
        self.firmado_por_mi = False

    def estatus_firmas(self):
        return f"{len(self.firmantes)} de {self.total_firmas}"

    def estado_bloque(self):
        return "Listo" if len(self.firmantes) >= self.total_firmas else "Pendiente"
