from django.db import models
from login.models import AuthUser


class Fincas(models.Model):
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    usuario = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fincas'




class TipoAbono(models.Model):
    nombre = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_abono'


class Productos(models.Model):
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_abono = models.ForeignKey(TipoAbono, models.DO_NOTHING, blank=True, null=True)
    finca = models.ForeignKey(Fincas, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'

class Arduinos(models.Model):
    finca = models.ForeignKey('Fincas', models.DO_NOTHING)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arduinos'
class DatosSuelos(models.Model):
    ph = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    arduino = models.ForeignKey(Arduinos, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos_suelos'


class TipoAbonoImagen(models.Model):
    # Relación con la tabla tipo_abono (que ya tienes definida arriba)
    tipo_abono = models.ForeignKey(
        TipoAbono,
        models.DO_NOTHING,             # no cambia nada en tu tabla original
        related_name="imagenes"        # permite acceder a abono.imagenes.all()
    )
    imagen = models.ImageField(upload_to="abonos/")  # se guarda en /media/abonos/
    titulo = models.CharField(max_length=150, blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)   # para ordenar varias imágenes
    es_principal = models.BooleanField(default=False)

    class Meta:
        db_table = "tipo_abono_imagenes"   # nombre de la tabla en la BD
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.tipo_abono_id} - {self.titulo or self.imagen.name}"




