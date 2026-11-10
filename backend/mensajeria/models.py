from django.db import models
from contacto.models import ClienteLead

# Create your models here.
class RegistroWhatsApp(models.Model):
    ESTADOS_MENSAJE = [
        ('PENDIENTE', 'Pendiente de envío'),
        ('ENVIADO', 'Enviado con éxito'),
        ('ENTREGADO', 'Entregado al dispositivo'),
        ('LEIDO', 'Leído por el cliente'),
        ('FALLIDO', 'Error en el envío'),
    ]

    cliente = models.ForeignKey(
        ClienteLead, 
        on_delete=models.CASCADE, 
        related_name="mensajes_whatsapp",
        verbose_name="Cliente"
    )
    
    # El ID único que Meta nos devuelve cuando enviamos un mensaje
    wamid = models.CharField(
        max_length=150, 
        blank=True, 
        null=True, 
        verbose_name="WhatsApp Message ID"
    )
    
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_MENSAJE, 
        default='PENDIENTE'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Si algo falla (ej. número bloqueado), guardamos el error exacto aquí
    error_log = models.TextField(blank=True, null=True, verbose_name="Detalles del error")

    def __str__(self):
        return f"Mensaje a {self.cliente.telefono} - {self.estado} - {self.fecha_creacion}"