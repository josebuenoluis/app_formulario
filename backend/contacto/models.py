from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class ClienteLead(models.Model):
    OPCIONES_POLIZA = [
        ('SALUD_DECESOS', 'Póliza de Bienestar Salud (incluye Decesos)'),
        ('SOLO_DECESOS', 'Solo Póliza de Decesos'),
    ]
    nombre = models.CharField(max_length=100,null=False)
    email = models.EmailField(null=False)
    validador_telefono = RegexValidator(
        regex=r'^\+\d{9,15}$',
        message="El número de teléfono debe incluir el prefijo del país usando el formato: '+34600000000'. Máximo 15 dígitos."
    )
    producto_interes = models.CharField(
        max_length=20, 
        choices=OPCIONES_POLIZA, 
        verbose_name="Producto a contratar"
    )
    # Aplicamos el validador aquí
    telefono = models.CharField(
        validators=[validador_telefono], 
        max_length=20, 
        verbose_name="Teléfono (WhatsApp)"
    )
    preguntas = models.TextField(blank=True, null=True, verbose_name="Preguntas o dudas")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"