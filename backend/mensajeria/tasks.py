from celery import shared_task
from mensajeria.models import RegistroWhatsApp
from contacto.models import ClienteLead
from mensajeria.utils import enviar_mensaje_whatsapp_plantilla,notificar_lead_al_vendedor

@shared_task
def enviar_mensaje_whatsapp_async(lead_id: int) -> bool:
    lead = ClienteLead.objects.select_related('vendedor').filter(id=lead_id).first()
    
    if not lead:
        return False

    if lead.vendedor and lead.vendedor.phone:
        nombre_vendedor = f"{lead.vendedor.first_name or ''} {lead.vendedor.last_name or ''}".strip()
        
        enviar_mensaje_whatsapp_plantilla(
            telefono_destinatario=lead.telefono,
            nombre_prospecto=lead.nombre,
            nombre_vendedor=nombre_vendedor,
            telefono_vendedor=lead.vendedor.phone,
            seguro_interes=lead.get_producto_interes_display(),
            telefono_remitente="+14155238886",
            template_sid="HX9e477c19c9a718f9ae221bb29e445feb",
        )
        message_twilio = notificar_lead_al_vendedor(
            telefono_prospecto=lead.telefono,
            nombre_prospecto=lead.nombre,
            nombre_vendedor=nombre_vendedor,
            telefono_vendedor=lead.vendedor.phone,
            seguro_interes=lead.get_producto_interes_display(),
            telefono_remitente="+14155238886",
            template_sid="HXf869e3f265c3c8454085c5805915f982",
        )
        RegistroWhatsApp.objects.create(
            cliente=lead,
            wamid=message_twilio.sid
        )
        return True
    return False