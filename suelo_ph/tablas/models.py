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





