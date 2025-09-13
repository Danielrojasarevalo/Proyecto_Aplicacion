from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import TipoAbonoViewSet

router = DefaultRouter()
router.register(r"tipo-abonos", TipoAbonoViewSet, basename="tipoabono")

urlpatterns = router.urls + [
    path('login/historial/', views.historial_view, name='historial'),
    path('login/datos/', views.datos_view, name='datos'),
    path('login/recomendaciones/', views.recomendaciones_view, name='recomendaciones'),
    path('login/recomendaciones/resultados', views.resultados_view, name='resultados'),

    path('datos_json/', views.datos_json, name='datos_json'),
    path('historial_datos/', views.historial_datos_api, name='historial_datos'),
    path('resultados_json/', views.resultados_json, name='resultados_json'),

    path('resultados/', views.resultados_view, name='resultados'),
    path('buscar_fecha/', views.buscar_datos_por_fecha, name='buscar_fecha'),
]
