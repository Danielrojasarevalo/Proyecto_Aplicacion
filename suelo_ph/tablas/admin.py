from django.contrib import admin
from .models import Arduinos, Fincas, DatosSuelos, Productos, TipoAbono, TipoAbonoImagen

# Modelos simples (sin configuración especial)
admin.site.register(Fincas)
admin.site.register(DatosSuelos)
admin.site.register(Productos)
admin.site.register(Arduinos)

# Inline para mostrar imágenes dentro del formulario de TipoAbono
class TipoAbonoImagenInline(admin.TabularInline):  # o admin.StackedInline si prefieres
    model = TipoAbonoImagen
    extra = 1

# Admin de TipoAbono con imágenes embebidas
@admin.register(TipoAbono)
class TipoAbonoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    inlines = [TipoAbonoImagenInline]

# Admin directo de las imágenes (opcional, se verá aparte en el panel)
@admin.register(TipoAbonoImagen)
class TipoAbonoImagenAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_abono", "titulo", "orden", "es_principal")
    list_filter = ("es_principal",)
