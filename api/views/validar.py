from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def facebook_webhook(request):
    if request.method == 'GET':
        # Parámetros que envía Meta para la verificación
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        # TU_TOKEN_DE_VERIFICACION debe coincidir con el que pongas en el Dashboard de Meta
        VERIFY_TOKEN = 'ramosgrupo#'

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFICADO")
            return HttpResponse(challenge)
        else:
            return HttpResponse('Error de verificación', status=403)
            
    elif request.method == 'POST':
        # Aquí recibirás las notificaciones reales (leads, mensajes, etc.)
        data = request.body
        print(f"Evento recibido: {data}")
        return HttpResponse('EVENT_RECEIVED', status=200)