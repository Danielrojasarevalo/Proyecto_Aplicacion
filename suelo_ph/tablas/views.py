from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosSuelos, Fincas, Arduinos
from .serializers import FincasSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from login.models import AuthUser

def login_view(request):
    return render(request, 'login.html')

def historial_view(request):
    return render(request, 'historial.html') 

def recomendaciones_view(request):
    return render(request, 'recomendaciones.html')

@login_required
def datos_view(request):
    finca_id = request.GET.get('id')
    if not finca_id:
        return JsonResponse({'error': 'No se especificó finca'}, status=400)

    try:
        auth_user = AuthUser.objects.get(email=request.user.email)
    except AuthUser.DoesNotExist:
        return JsonResponse({'error': 'Usuario no válido'}, status=403)

    finca = get_object_or_404(Fincas, id=finca_id, usuario=auth_user)
    
    # Obtener los arduinos de la finca para pasarlos al template
    arduinos = Arduinos.objects.filter(finca=finca)
    
    context = {
        'finca_id': finca_id,
        'arduinos': arduinos,
    }
    return render(request, 'datos.html', context)

@login_required
def datos_json(request):
    finca_id = request.GET.get('id')
    arduino_id = request.GET.get('arduino_id')  # Nuevo parámetro opcional
    
    if not finca_id:
        return JsonResponse({'error': 'No se especificó finca'}, status=400)

    try:
        auth_user = AuthUser.objects.get(email=request.user.email)
    except AuthUser.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    finca = get_object_or_404(Fincas, id=finca_id, usuario=auth_user)
    
    # Filtra por finca a través del arduino
    queryset = DatosSuelos.objects.filter(arduino__finca=finca)
    
    # Filtro adicional por arduino si se especifica
    if arduino_id:
        queryset = queryset.filter(arduino_id=arduino_id)
    
    # Obtiene los datos con información del arduino
    datos = queryset.values(
        'fecha', 
        'humedad', 
        'temperatura', 
        'ph',
        'arduino__nombre'  # Incluye el nombre del arduino
    ).order_by('-fecha')  # Ordena por fecha descendente

    lista_datos = []
    for d in datos:
        lista_datos.append({
            'fecha': d['fecha'].strftime('%Y-%m-%d %H:%M:%S'),  # Formato más completo
            'humedad': d['humedad'],
            'temperatura': d['temperatura'],
            'ph': d['ph'],
            'arduino': d['arduino__nombre'],  # Nombre del dispositivo
        })

    return JsonResponse(lista_datos, safe=False)