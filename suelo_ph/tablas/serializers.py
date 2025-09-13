from rest_framework import serializers
from .models import Fincas, TipoAbono, TipoAbonoImagen

class FincasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fincas
        fields = ['id', 'nombre', 'ubicacion', 'usuario']

class TipoAbonoImagenSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = TipoAbonoImagen
        fields = ("id", "titulo", "orden", "es_principal", "url")

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.imagen:
            return request.build_absolute_uri(obj.imagen.url) if request else obj.imagen.url
        return None

class TipoAbonoSerializer(serializers.ModelSerializer):
    imagen_principal = serializers.SerializerMethodField()
    imagenes = TipoAbonoImagenSerializer(many=True, read_only=True)

    class Meta:
        model = TipoAbono
        fields = ("id", "nombre", "imagen_principal", "imagenes")

    def get_imagen_principal(self, obj):
        request = self.context.get("request")
        img = obj.imagenes.filter(es_principal=True).first() or obj.imagenes.first()
        if img and img.imagen:
            return request.build_absolute_uri(img.imagen.url) if request else img.imagen.url
        return None
