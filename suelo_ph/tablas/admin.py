from django.contrib import admin
from .models import Arduinos, Fincas, DatosSuelos, Productos, TipoAbono

admin.site.register(Fincas)
admin.site.register(DatosSuelos)
admin.site.register(Productos)
admin.site.register(TipoAbono)
admin.site.register(Arduinos)



# Register your models here.
