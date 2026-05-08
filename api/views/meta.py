

from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
import requests
from requests import RequestException
from datetime import datetime
from api.serializers import EmpresaSerializer
from api.models import Empresa, Proyectos
import os
import sys
import unicodedata
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
# Configuración
VERIFY_TOKEN = "nexuscrm"
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "1104656259400123")


def normalizar_texto(texto):
    texto = texto or ""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")


def obtener_id_proyecto_desde_mensaje(mensaje):
    mensaje_normalizado = normalizar_texto(mensaje)
    proyectos = list(Proyectos.objects.filter(estado=1))

    for proyecto in sorted(proyectos, key=lambda item: len(item.nombre_proyecto), reverse=True):
        nombre_normalizado = normalizar_texto(proyecto.nombre_proyecto)
        if nombre_normalizado and nombre_normalizado in mensaje_normalizado:
            print("Proyecto detectado:", proyecto.nombre_proyecto)
            return proyecto.id_proyecto

    proyecto_otros = Proyectos.objects.filter(nombre_proyecto__iexact="Otros").first()
    if proyecto_otros:
        print("Proyecto detectado: Otros")
        return proyecto_otros.id_proyecto

    print("Proyecto detectado: Otros no encontrado, usando ID 13 ejemplo")
    return 13

# 🔹 Enviar mensaje WhatsApp
def enviar_mensaje_detalle(destino, texto):
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

    if not TOKEN:
        return {
            "ok": False,
            "status_code": None,
            "error": "No se encontro WHATSAPP_TOKEN en el .env del backend.",
            "response": None,
        }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
    except RequestException as exc:
        print(" Error enviando WhatsApp:", str(exc))
        return {
            "ok": False,
            "status_code": None,
            "error": f"No se pudo conectar con Meta: {exc}",
            "response": None,
        }

    try:
        response_data = response.json()
    except ValueError:
        response_data = response.text

    print(" Enviado:", response.status_code, response_data)
    error = None
    if not response.ok:
        if isinstance(response_data, dict):
            error = response_data.get("error", {}).get("message") or str(response_data)
        else:
            error = str(response_data)

    return {
        "ok": response.ok,
        "status_code": response.status_code,
        "error": error,
        "response": response_data,
    }


def enviar_mensaje(destino, texto):
    return enviar_mensaje_detalle(destino, texto)["ok"]


# 🔹 Guardar lead en tu API
def guardar_lead(numero, mensaje):
    url = "https://api.ramosgrupo.lat/api/savelead/"
    id_proyecto_interes = obtener_id_proyecto_desde_mensaje(mensaje)

    payload = {
        "nombre": "facebook",
        "telefono": numero,
        "email": "",
        "observacion": "Lead desde WhatsApp",
        "id_origen": 1,
        "id_proyecto_interes": id_proyecto_interes,
        "id_asesor": None,
        "id_estado": 5,
        "id_subestado": 15,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_asignacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombreAsesor": "Admin",
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

            print(f"De {numero}: {mensaje}")
            #  Guardar lead automáticamente
            guardar_lead(numero, mensaje)
            enviar_mensaje(numero, "Hola, en un momento un asesor se comunicara contigo")

            #  Reenviar a otro número
            
            numero_destino = f"51{get_numero_empresa()}"
    
            texto = f"""*ALERTA DE MENSAJE*

            ------------------------
            Cliente: {numero}
            Mensaje:
            {mensaje}
            ------------------------
            """
            enviar_mensaje(numero_destino, texto)

        except Exception as e:
            print("Evento diferente o error:")
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
