from rest_framework import serializers
from contacto.models import ClienteLead
from users.models import Users

class ClienteLeadSerializer(serializers.ModelSerializer):
    # Mapea "correo" del frontend al campo "email" del modelo
    correo = serializers.EmailField(source="email")
    # Recibe el slug del vendedor desde Next.js
    slug = serializers.SlugField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = ClienteLead
        fields = [
            "id",
            "nombre",
            "correo",
            "telefono",
            "producto_interes",
            "preguntas",
            "slug",
        ]

    def create(self, validated_data):
        slug_vendedor = validated_data.pop("slug", None)
        vendedor = None

        if slug_vendedor:
            vendedor = Users.objects.filter(slug=slug_vendedor, is_active=True).first()

        return ClienteLead.objects.create(vendedor=vendedor, **validated_data)