from .models import TipoAbono, Productos

def recomendar_abono(ph, humedad, temperatura, temporada):
    if temporada == 'Mitaca':
        if ph > 1 and humedad > 1 and temperatura > 1:
            # Buscar primero en Productos por nombre relacionado a urea
            producto = Productos.objects.filter(nombre__icontains="urea").first()
            if producto:
                return producto.nombre
            # Si no hay producto, buscar en TipoAbono
            abono = TipoAbono.objects.filter(nombre__icontains="urea").first()
            if abono:
                return abono.nombre
            else:
                return "Abono Cosecha Ácido"
        else:
            producto = Productos.objects.filter(nombre__icontains="Cosecha Balanceado").first()
            if producto:
                return producto.nombre
            abono = TipoAbono.objects.filter(nombre__icontains="Cosecha Balanceado").first()
            if abono:
                return abono.nombre
            else:
                return "NO HAY ABONOS RECOMENDADOS PARA ESOS DATOS"
