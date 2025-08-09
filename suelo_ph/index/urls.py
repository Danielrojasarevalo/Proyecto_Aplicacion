from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),     # Página principal
    path('nosotros/', views.nosotros, name='nosotros'),  # Página Nosotros
    path('contactanos/', views.contactanos, name='contactanos'),  # Página Contáctanos
]

