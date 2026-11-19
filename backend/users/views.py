from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import Users
from users.serializers import VendedorPublicoSerializer
# Create your views here.

class UsersView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, slug=None):
        # Soporta tanto /api/contacto/<slug>/ como /api/contacto/?slug=...
        slug = slug or request.query_params.get('slug')
        
        if not slug:
            return Response(
                {'error': 'Slug requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        vendedor = get_object_or_404(Users, slug=slug, is_active=True)
        serializer = VendedorPublicoSerializer(vendedor)

        return Response({
            'id': vendedor.id,
            'slug': vendedor.slug,
            'nombre_completo': f"{vendedor.first_name} {vendedor.last_name}".strip(),
            'email': vendedor.email,
            'phone': vendedor.phone,
            'city': vendedor.city,
            'state': vendedor.state,
            'country': vendedor.country,
        }, status=status.HTTP_200_OK)