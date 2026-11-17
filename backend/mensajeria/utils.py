from twilio.rest import Client
import os,json
from urllib.parse import quote
import io
import qrcode
from django.conf import settings

def generar_url_vendedor(slug_vendedor: str) -> str:
    base_url = settings.FRONTEND_BASE_URL.rstrip("/")
    return f"{base_url}/contacto/{slug_vendedor}"


def generar_qr_vendedor_bytes(slug_vendedor: str) -> bytes:
    url_destino = generar_url_vendedor(slug_vendedor)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(url_destino)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#000000", back_color="#FFFFFF")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def enviar_mensaje_whatsapp_plantilla(nombre_vendedor:str,nombre_prospecto:str,seguro_interes:str,telefono_destinatario:str,telefono_remitente:str,telefono_vendedor:str,template_sid:str):
    api_key = os.environ["TWILIO_API_KEY"]
    api_secret = os.environ["TWILIO_API_SECRET"]
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]


    client = Client(api_key, api_secret, account_sid)

    mensaje_autocompletado = (
        f"Hola {nombre_vendedor}, soy {nombre_prospecto}."
        f"Me interesa recibir información sobre el seguro de {seguro_interes}."
    )

    enlace_wa = f"https://wa.me/{telefono_vendedor}?text={quote(mensaje_autocompletado)}"
    variables_plantilla = json.dumps({
        "1": nombre_vendedor,   # {{1}} Nombre del vendedor
        "2": seguro_interes,    # {{2}} Seguro de interés
        "3": enlace_wa,         # {{3}} Enlace wa.me/...?text=...
    })
    message = client.messages.create(
        from_=f"whatsapp:{telefono_remitente}",
        to=f"whatsapp:{telefono_destinatario}",
        content_sid=template_sid,  # Plantilla válida del Sandbox,
        content_variables=variables_plantilla,
    )

    print("Mensaje enviado con éxito. SID:", message.sid)
    return message

def notificar_lead_al_vendedor(
    nombre_vendedor: str,
    telefono_vendedor: str,
    nombre_prospecto: str,
    telefono_prospecto: str,
    seguro_interes: str,
    telefono_remitente: str,
    template_sid: str,
):
    api_key = os.environ["TWILIO_API_KEY"]
    api_secret = os.environ["TWILIO_API_SECRET"]
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]

    client = Client(api_key, api_secret, account_sid)

    # Limpia el teléfono del prospecto para construir el enlace wa.me del vendedor hacia el cliente
    tel_prospecto_limpio = telefono_prospecto.replace("+", "").replace(" ", "").strip()
    if len(tel_prospecto_limpio) == 9:
        tel_prospecto_limpio = f"34{tel_prospecto_limpio}"

    mensaje_autocompletado = (
        f"Hola {nombre_prospecto}, soy {nombre_vendedor}, tu asesor de seguros. "
        f"He recibido tu solicitud sobre {seguro_interes}."
    )

    enlace_wa_prospecto = f"https://wa.me/{tel_prospecto_limpio}?text={quote(mensaje_autocompletado)}"

    variables_plantilla = json.dumps({
        "1": nombre_prospecto,       # {{1}} Nombre del cliente/prospecto
        "2": seguro_interes,         # {{2}} Seguro de interés
        "3": enlace_wa_prospecto,    # {{3}} Enlace wa.me hacia el móvil del prospecto
    })

    message = client.messages.create(
        from_=f"whatsapp:{telefono_remitente}",
        to=f"whatsapp:+34{telefono_vendedor}", #644275671
        content_sid=template_sid,
        content_variables=variables_plantilla,
    )

    return message