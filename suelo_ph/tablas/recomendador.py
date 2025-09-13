from .models import TipoAbono, Productos

# Definimos las reglas de recomendación
REGLAS_ABONOS = [
    {
        "condicion": lambda ph, h, t, temporada: temporada == "Mitaca" and ph > 1 and h > 1 and t > 1,
        "nombre": "ABOTEK",
        "fallback": "Abono Cosecha Ácido"
    },
        {
        "condicion": lambda ph, h, t, temporada: temporada == "Mitaca" and ph > 1 and h > 1 and t > 1,
        "nombre": "NUTRIMON",
        "fallback": "Abono Cosecha Ácido"
    },
    {
        "condicion": lambda ph, h, t, temporada: temporada == "Mitaca",
        "nombre": "Cosecha Balanceado",
        "fallback": "NO HAY ABONOS RECOMENDADOS PARA ESOS DATOS"
    }
    
]

def recomendar_abono(ph, humedad, temperatura, temporada):
    for regla in REGLAS_ABONOS:
        if regla["condicion"](ph, humedad, temperatura, temporada):
            # Buscar en Productos
            producto = Productos.objects.filter(nombre__icontains=regla["nombre"]).first()
            if producto:
                return producto.nombre
            # Buscar en TipoAbono
            abono = TipoAbono.objects.filter(nombre__icontains=regla["nombre"]).first()
            if abono:
                return abono.nombre
            # Si no encontró en la BD → fallback
            return regla["fallback"]
    
    # Si no se cumple ninguna regla
    return "NO HAY ABONOS RECOMENDADOS PARA ESOS DATOS"
