import serial
import django
import os
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suelo_ph.settings')
django.setup()

from tablas.models import DatosSuelos

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

MAX_REGISTROS = 33
posicion = 0

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            try:
                humedad = float(linea)
            except ValueError:
                print(f"Valor no numérico recibido: {linea}")
                continue

            registros = DatosSuelos.objects.all().order_by('id')

            if registros.count() < MAX_REGISTROS:
                DatosSuelos.objects.create(humedad=humedad, fecha=datetime.now())
                print(f"Nuevo dato creado: Humedad={humedad}")
            else:
                registro = registros[posicion]
                registro.humedad = humedad
                registro.fecha = datetime.now()
                registro.save()
                print(f"Dato actualizado en posición {posicion + 1}: Humedad={humedad}")

                posicion = (posicion + 1) % MAX_REGISTROS

    except Exception as e:
        print(f"Error general: {e}")
