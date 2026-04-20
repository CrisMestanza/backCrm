

from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
import requests
from datetime import datetime
from api.serializers import EmpresaSerializer
from api.models import Empresa
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
# Configuración
VERIFY_TOKEN = "nexuscrm"
PHONE_ID = "1089219270943492"

# 🔹 Enviar mensaje WhatsApp
def enviar_mensaje(destino, texto):
    url = f"https://graph.facebook.com/v25.0/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": destino,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(" Enviado:", response.status_code, response.text)


# 🔹 Guardar lead en tu API
def guardar_lead(numero):
    url = "https://api.ramosgrupo.lat/api/savelead/"

    payload = {
        "nombre": "facebook",
        "telefono": numero,
        "email": "",
        "observacion": "Lead desde WhatsApp",
        "id_origen": 1,
        "id_proyecto_interes": 1,
        "id_asesor": 11,
        "id_estado": 5,
        "id_subestado": 15,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_asignacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombreAsesor": "Verito",
        "estado":1
    }

    try:
        response = requests.post(url, json=payload)
        print(" Lead enviado:", response.status_code, response.text)
    except Exception as e:
        print("Error enviando lead:", str(e))


# 🔹 Webhook principal
@api_view(['GET', 'POST'])
def webhook(request):

    #  Verificación Meta
    if request.method == 'GET':
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge, content_type="text/plain")
        return HttpResponse("Error de verificacion", status=403)

    #  Recibir mensajes
    elif request.method == 'POST':
        data = request.data

        try:
            #  Obtener mensaje y número
            mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']


            #  Guardar lead automáticamente
            guardar_lead(numero)

            #  Reenviar a otro número
            
            numero_destino = f"51{get_numero_empresa()}"

            texto = f"""📥 *ALERTA DE MENSAJE*

            ━━━━━━━━━━━━━━━
            👤 *Cliente:* {numero}
            💬 *Mensaje:*
            {mensaje}
            ━━━━━━━━━━━━━━━
            """

            enviar_mensaje(numero_destino, texto)

        except Exception as e:
            print("Evento diferente o error:", data)
            print("Error:", str(e))

        return Response({"status": "ok"})



def get_numero_empresa():
    empresa = Empresa.objects.first()
    print("Número empresa:", empresa.numero if empresa else "No encontrado")
    return empresa.numero if empresa else None


@api_view(['POST'])
def postNumero(request):
    numero = request.data.get('numero')
    empresa, created = Empresa.objects.get_or_create(id_empresa=1)

    empresa.numero = numero
    empresa.save()

    if created:
        return Response({"status": "Empresa creada y número guardado"})
    else:
        return Response({"status": "Número actualizado"})
