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
    recomendados = []
    for regla in REGLAS_ABONOS:
        if regla["condicion"](ph, humedad, temperatura, temporada):
            # Buscar en Productos
            producto = Productos.objects.filter(nombre__icontains=regla["nombre"]).first()
            if producto:
                recomendados.append(producto.nombre)
                continue
            # Buscar en TipoAbono
            abono = TipoAbono.objects.filter(nombre__icontains=regla["nombre"]).first()
            if abono:
                recomendados.append(abono.nombre)
                continue
            # Si no encontró en la BD → fallback
            recomendados.append(regla["fallback"])
    if not recomendados:
        recomendados.append("NO HAY ABONOS RECOMENDADOS PARA ESOS DATOS")
    return recomendados
