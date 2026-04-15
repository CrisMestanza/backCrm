from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def facebook_webhook(request):
    if request.method == 'GET':
        # Meta envía los parámetros con 'hub.' al principio
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        # Tu token secreto
        VERIFY_TOKEN = 'ramosgrupo#'

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFICADO CON ÉXITO")
            # Es vital devolver el challenge TAL CUAL lo envía Meta
            return HttpResponse(challenge, content_type="text/plain")
        else:
            print("FALLO LA VERIFICACION: Token incorrecto o modo invalido")
            return HttpResponse('Error de verificacion', status=403)
            
    elif request.method == 'POST':
        # Aquí es donde llegarán los leads
        data = request.body
        print(f"Lead recibido: {data}")
        return HttpResponse('EVENT_RECEIVED', status=200)