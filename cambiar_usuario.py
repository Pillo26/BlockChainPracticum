import json

usuarios = {
    "1": {
        "usuario": "juan_perito",
        "rol": "perito",
        "ruta_llaves": "datos/llaves_perito.json"
    },
    "2": {
        "usuario": "maria_fiscal",
        "rol": "fiscal",
        "ruta_llaves": "datos/llaves_fiscal.json"
    },
    "3": {
        "usuario": "pedro_abogado",
        "rol": "abogado_defensor",
        "ruta_llaves": "datos/llaves_abogado.json"
    }
}

print("Selecciona un usuario:")
print("1. Perito Informático")
print("2. Fiscal del Ministerio Público")
print("3. Abogado Defensor")

eleccion = input("Número de opción: ").strip()

if eleccion in usuarios:
    with open("datos/config_usuario.json", "w") as f:
        json.dump(usuarios[eleccion], f, indent=4)
    print(f"✅ Configuración actualizada para: {usuarios[eleccion]['usuario']} ({usuarios[eleccion]['rol']})")
else:
    print("❌ Opción no válida.")
