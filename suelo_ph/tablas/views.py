from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosSuelos, Fincas, Arduinos
from .serializers import FincasSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from login.models import AuthUser
from django.views.decorators.http import require_GET 

def login_view(request):
    return render(request, 'login.html')
def recomendaciones_view(request):
    return render(request, 'recomendaciones.html')  


@login_required
@require_GET 
def historial_datos_api(request):
    try:
        # Obtener parámetros
        finca_id = request.GET.get('id')
        
        if not finca_id:
            return JsonResponse({'error': 'Se requiere el ID de la finca'}, status=400)
        
        # Obtener el usuario real de AuthUser
        try:
            auth_user = AuthUser.objects.get(email=request.user.email)
        except AuthUser.DoesNotExist:
            return JsonResponse({'error': 'Usuario no válido'}, status=403)

        # Verificar que la finca pertenece al usuario correcto
        if not Fincas.objects.filter(id=finca_id, usuario=auth_user).exists():
            return JsonResponse({'error': 'Finca no autorizada'}, status=403)
        
        # Obtener datos filtrados
        datos = DatosSuelos.objects.filter(
            arduino__finca_id=finca_id
        ).order_by('-fecha').values(
            'id', 'fecha', 'humedad', 'temperatura', 'ph', 'arduino__nombre'
        )
        
        # Formatear respuesta
        datos_list = list(datos)
        for dato in datos_list:
            dato['arduino'] = dato.pop('arduino__nombre')
        
        return JsonResponse(datos_list, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def historial_view(request):
    return render(request, 'historial.html')


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