from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html')

def nosotros(request):
    return render(request, 'html/nosotros.html')

def sesion(request):
    return render(request, 'html/sesion.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def contactanos(request):
    mensaje_enviado = False
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        autorizacion = request.POST.get('autorizacion')

        asunto = f"Nuevo mensaje de contacto: {nombre} {apellido}"
        cuerpo = (
            f"Nombre: {nombre} {apellido}\n"
            f"Email: {email}\n"
            f"Mensaje:\n{mensaje}\n"
            f"Autorización: {'Sí' if autorizacion else 'No'}"
        )

        send_mail(
            asunto,
            cuerpo,
            'rojasarevalodaniel@gmail.com', 
            ['rojasarevalodaniel@gmail.com'],  
            fail_silently=False,
        )
        mensaje_enviado = True

    return render(request, 'html/contactanos.html', {'mensaje_enviado': mensaje_enviado})





