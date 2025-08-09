from django.urls import path
from . import views  # Importa las vistas de la app tablas


urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('login/historial/', views.historial_view, name='historial'),  # Añadir esta ruta para historial

    path('login/datos/', views.datos_view, name='datos'),

    path('login/recomendaciones/', views.recomendaciones_view, name='recomendaciones'),  # Añadir esta ruta para recomendaciones
    path('datos_json/', views.datos_json, name='datos_json'),    

]
# En la app 'tablas', urls.py


