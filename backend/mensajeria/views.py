from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Users
from mensajeria.utils import generar_qr_vendedor_bytes
# Create your views here.
def descargar_qr_vendedor(request, slug):
    agente = get_object_or_404(Users, slug=slug)
    qr_bytes = generar_qr_vendedor_bytes(agente.slug)

    response = HttpResponse(qr_bytes, content_type="image/png")
    response["Content-Disposition"] = f'inline; filename="qr_{agente.slug}.png"'
    return response