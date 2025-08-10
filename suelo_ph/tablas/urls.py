from django.urls import path
from . import views  # Importa las vistas de la app tablas


urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('login/historial/', views.historial_view, name='historial'),  # Añadir esta ruta para historial

    path('login/datos/', views.datos_view, name='datos'),

    path('login/recomendaciones/', views.recomendaciones_view,name='recomendaciones'), 
    path('datos_json/', views.datos_json, name='datos_json'),
    path('historial_datos/', views.historial_datos_api, name='historial_datos'),

]
# En la app 'tablas', urls.py


