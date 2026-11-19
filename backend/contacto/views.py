from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from contacto.models import ClienteLead
from contacto.serializers import ClienteLeadSerializer
from mensajeria.tasks import enviar_mensaje_whatsapp_async
# Create your views here.

class ClienteLeadView(viewsets.ModelViewSet):
    queryset = ClienteLead.objects.all()
    serializer_class = ClienteLeadSerializer
    permission_classes=[AllowAny]

    def perform_create(self, serializer):
        try:
            lead = serializer.save()
            enviar_mensaje_whatsapp_async.delay(lead.id)
            # # Si el lead tiene un vendedor asignado con teléfono, envía el WhatsApp
            # if lead.vendedor and lead.vendedor.phone:
            #     message_twilio = enviar_mensaje_whatsapp_plantilla(
            #         telefono_destinatario=lead.telefono,
            #         nombre_prospecto=lead.nombre,
            #         nombre_vendedor=f"{lead.vendedor.first_name or ''} {lead.vendedor.last_name or ''}".strip(),
            #         telefono_vendedor=lead.vendedor.phone,
            #         seguro_interes=lead.get_producto_interes_display(),
            #         telefono_remitente="+14155238886",
            #         template_sid="HX9e477c19c9a718f9ae221bb29e445feb",
            #     )
            #     message_twilio = notificar_lead_al_vendedor(
            #         telefono_prospecto=lead.telefono,
            #         nombre_prospecto=lead.nombre,
            #         nombre_vendedor=f"{lead.vendedor.first_name or ''} {lead.vendedor.last_name or ''}".strip(),
            #         telefono_vendedor=lead.vendedor.phone,
            #         seguro_interes=lead.get_producto_interes_display(),
            #         telefono_remitente="+14155238886",
            #         template_sid="HXf869e3f265c3c8454085c5805915f982",
            #     )
            #     RegistroWhatsApp(
            #         cliente = lead,  
            #         wamid = message_twilio.sid
            #     ).save()
            # else:
            #     print(f"⚠️ Lead {lead.id} guardado sin vendedor válido o sin teléfono asignado.")

        except Exception as e:
            print("❌ ERROR EN PERFORM_CREATE:", e)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ClienteLead.objects.filter(vendedor=self.request.user)
        
        return ClienteLead.objects.none()