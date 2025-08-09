from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from tablas.models import Fincas
from login.models import AuthUser
from django.shortcuts import render, get_object_or_404



def crear_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        ubicacion = request.POST.get('ubicacion')  # Ubicación del usuario

        # Verificar si las contraseñas coinciden
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('crear_usuario')  # Redirigir para mostrar el mensaje
        if len(password1) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect('crear_usuario')

        if username != email:
            messages.error(request, "Los correos no coinciden")
            return redirect('crear_usuario')  # Redirigir para mostrar el mensaje

        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )

            # Asignar los demás datos
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, "Usuario creado correctamente")
            return redirect('login')  # Redirigir al usuario al login después de registrarse

        except Exception as e:
            messages.error(request, f"Error al crear el usuario: {str(e)}")
            return redirect('crear_usuario')  # Redirigir en caso de error

    return render(request, 'html/crear_usuario.html', {'title': 'Crear Usuario'})




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # Aquí defines 'user'

        if user is not None:
            auth_login(request, user)
            return redirect(reverse('login') + '?mostrar_modal=1')
        else:
            messages.error(request, "Credenciales incorrectas. Intenta de nuevo.")
            return render(request, 'html/login.html', {'title': 'Inicio de sesión'})

    else:
        abrir_modal = request.GET.get('mostrar_modal') == '1'
        return render(request, 'html/login.html', {
            'title': 'Inicio de sesión',
            'abrir_modal_fincas': abrir_modal
        })
    


@login_required
@csrf_exempt
def crear_finca_ajax(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        email = request.user.email  # email del usuario autenticado

        if not nombre or not ubicacion:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)

        # Obtener instancia AuthUser por email, o 404 si no existe
        usuario = get_object_or_404(AuthUser, email=email)

        # Crear finca relacionada con ese usuario
        finca = Fincas.objects.create(nombre=nombre, ubicacion=ubicacion, usuario=usuario)

        return JsonResponse({
            'id': finca.id,
            'nombre': finca.nombre,
            'ubicacion': finca.ubicacion,
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)



@login_required
def api_fincas(request):
    usuario_email = request.user.email  
    fincas = list(Fincas.objects.filter(usuario__email=usuario_email).values('id', 'nombre', 'ubicacion'))
    return JsonResponse({'fincas': fincas})




class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'html/nueva_contraseña.html' 
    success_url = '/index/login/nueva_contraseña/completo/'




