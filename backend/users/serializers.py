

from rest_framework import serializers
from users.models import Users

class VendedorPublicoSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = [
            'id',
            'slug',
            'first_name',
            'last_name',
            'nombre_completo',
            'email',
            'phone',
            'city',
            'state',
            'country',
        ]

    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()