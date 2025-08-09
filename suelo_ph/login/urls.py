from django.urls import path    
from . import views
from .views import CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import include
from login.views import crear_finca_ajax

urlpatterns = [
    path('login/', views.login, name='login'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    
    # Vista personalizada donde se escribe el correo para recuperar
    path('recuperar_contraseña/', auth_views.PasswordResetView.as_view(
        template_name='html/recuperar_contraseña.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='enviado/'
    ), name='recuperar_contraseña'),

    path('recuperar_contraseña/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Esta ruta es la que se abre desde el enlace del correo (y carga tu HTML personalizado)
    path('nueva_contraseña/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Vista final de éxito
    path('nueva_contraseña/completo/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Puedes eliminar esto si `crear_contraseña/` es duplicado
    path('crear_contraseña/', views.crear_usuario, name='crear_contraseña'),
    path('api/fincas/', views.api_fincas, name='api_fincas'),
    path('crear_finca_ajax/', crear_finca_ajax, name='crear_finca_ajax'),
]




