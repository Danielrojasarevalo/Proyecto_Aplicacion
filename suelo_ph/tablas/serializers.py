from rest_framework import serializers # type: ignore
from .models import Fincas

class FincasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fincas
        fields = ['id', 'nombre', 'ubicacion', 'usuario']
