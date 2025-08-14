from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosSuelos, Fincas, Arduinos,TipoAbono, Productos
from .serializers import FincasSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from login.models import AuthUser
from django.views.decorators.http import require_GET 
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from datetime import datetime
from .recomendador import recomendar_abono


def login_view(request):
    return render(request, 'login.html')
def recomendaciones_view(request):
    return render(request, 'recomendaciones.html')  






@login_required
@require_POST
@csrf_exempt
def resultados_json(request):
    try:
        data = json.loads(request.body)
        fecha_desde = data.get('fecha_desde')
        fecha_hasta = data.get('fecha_hasta')
        tipo_abono_nombre = data.get('tipo_abono_nombre')
        finca_id = data.get('finca_id')
        
        if not all([fecha_desde, fecha_hasta, tipo_abono_nombre, finca_id]):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan parámetros requeridos'
            }, status=400)
        
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            
            if fecha_desde > fecha_hasta:
                return JsonResponse({
                    'status': 'error',
                    'message': 'La fecha de inicio no puede ser mayor a la fecha final'
                }, status=400)
                
            auth_user = AuthUser.objects.get(email=request.user.email)
            finca = get_object_or_404(Fincas, id=finca_id, usuario=auth_user)
            
            datos = DatosSuelos.objects.filter(
                fecha__gte=fecha_desde,
                fecha__lte=fecha_hasta,
                arduino__finca=finca
            ).order_by('fecha')
            
            if not datos.exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'No se encontraron datos para los criterios seleccionados'
                })
            
            datos_list = [{
                'fecha': dato.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'ph': dato.ph,
                'humedad': dato.humedad,
                'temperatura': dato.temperatura,
                'arduino': dato.arduino.nombre if dato.arduino else None
            } for dato in datos]
            
            # Calcular promedios de sensores (ignorar None, y si no hay datos válidos, no da error)
            phs = [dato.ph for dato in datos if dato.ph is not None]
            humedades = [dato.humedad for dato in datos if dato.humedad is not None]
            temperaturas = [dato.temperatura for dato in datos if dato.temperatura is not None]
            if phs:
                ph_promedio = sum(phs) / len(phs)
            else:
                ph_promedio = 0
            if humedades:
                humedad_promedio = sum(humedades) / len(humedades)
            else:
                humedad_promedio = 0
            if temperaturas:
                temperatura_promedio = sum(temperaturas) / len(temperaturas)
            else:
                temperatura_promedio = 0
            abono_recomendado = recomendar_abono(ph_promedio, humedad_promedio, temperatura_promedio, tipo_abono_nombre)
            productos = Productos.objects.filter(nombre__icontains=abono_recomendado, finca=finca)
            productos_list = [{
                'nombre': producto.nombre,
                'descripcion': producto.descripcion
            } for producto in productos]
            return JsonResponse({
                'status': 'ok',
                'datos_suelo': datos_list,
                'productos_recomendados': productos_list,
                'tipo_abono': tipo_abono_nombre,
                'abono_recomendado': abono_recomendado
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Error en el formato JSON'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error del servidor: {str(e)}'
        }, status=500)


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

@csrf_exempt
def resultados_view(request):
    abono_recomendado = None
    productos_recomendados = []
    datos = []
    ph_promedio = None
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    temporada = request.GET.get('temporada') or request.GET.get('tipo_abono_nombre')
    finca_id = request.GET.get('finca_id')
    error_message = None

    if all([fecha_desde, fecha_hasta, temporada, finca_id]):
        try:
            fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            auth_user = AuthUser.objects.get(email=request.user.email)
            finca = get_object_or_404(Fincas, id=finca_id, usuario=auth_user)
            datos_qs = DatosSuelos.objects.filter(
                fecha__gte=fecha_desde_dt,
                fecha__lte=fecha_hasta_dt,
                arduino__finca=finca
            ).order_by('fecha')
            datos = [{
                'fecha': d.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'ph': d.ph,
                'humedad': d.humedad,
                'temperatura': d.temperatura,
                'arduino': d.arduino.nombre if d.arduino else None
            } for d in datos_qs]
            phs = [d['ph'] for d in datos if d['ph'] is not None]
            if phs:
                ph_promedio = sum(phs) / len(phs)
            else:
                ph_promedio = 0
            humedades = [d['humedad'] for d in datos if d['humedad'] is not None]
            if humedades:
                humedad_promedio = sum(humedades) / len(humedades)
            else:
                humedad_promedio = 0
            temperaturas = [d['temperatura'] for d in datos if d['temperatura'] is not None]
            if temperaturas:
                temperatura_promedio = sum(temperaturas) / len(temperaturas)
            else:
                temperatura_promedio = 0
            from .recomendador import recomendar_abono
            abono_recomendado = recomendar_abono(ph_promedio, humedad_promedio, temperatura_promedio, temporada)
            # Buscar el objeto TipoAbono correspondiente al abono recomendado
            tipo_abono_obj = TipoAbono.objects.filter(nombre__icontains=abono_recomendado).first()
            if tipo_abono_obj:
                productos = Productos.objects.filter(tipo_abono=tipo_abono_obj, finca=finca)
            else:
                productos = Productos.objects.filter(nombre__icontains=abono_recomendado, finca=finca)
            productos_recomendados = [{
                'nombre': p.nombre,
                'descripcion': p.descripcion
            } for p in productos]
            # Usar la descripción del primer producto relacionado al tipo_abono
            abono_descripcion = None
            if tipo_abono_obj:
                producto_con_desc = Productos.objects.filter(tipo_abono=tipo_abono_obj, descripcion__isnull=False).exclude(descripcion='').first()
                if producto_con_desc:
                    abono_descripcion = producto_con_desc.descripcion
            if not abono_descripcion and productos_recomendados:
                abono_descripcion = productos_recomendados[0]['descripcion']
        except Exception as e:
            error_message = str(e)
    else:
        error_message = 'Faltan parámetros requeridos para mostrar los resultados.'

    context = {
        'abono_recomendado': abono_recomendado,
        'productos_recomendados': productos_recomendados,
        'datos': datos,
        'ph_promedio': ph_promedio,
        'humedad_promedio': locals().get('humedad_promedio', None),
        'temperatura_promedio': locals().get('temperatura_promedio', None),
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'temporada': temporada,
        'error_message': error_message,
        'abono_descripcion': abono_descripcion,
    }
    return render(request, 'resultados.html', context)

