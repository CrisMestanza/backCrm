from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,LeadsSaveSerializer
from api.models import Leads
from django.utils import timezone
from django.contrib.auth.hashers import check_password 
from datetime import datetime, timedelta
from django.db.models import Q
from api.views.meta import enviar_mensaje_detalle

MINUTOS_ANTES_RECORDATORIO_LLAMADA = 15
MINUTOS_TOLERANCIA_RECORDATORIO_LLAMADA = 2


@api_view(['GET'])
def getLead(request, id_asesor):
    leads = Leads.objects.filter(id_asesor=id_asesor,estado=1).order_by('-fecha_registro')
    serializer = LeadsSerializer(leads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalLeads(request):
    leads = Leads.objects.filter(id_estado = 5).count()
    return Response({'total': leads}, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalLeadsHoy(request):
    hoy = timezone.now().date()
    
    # Filtrar por el campo fecha_registro (solo la parte de la fecha)
    leads_hoy = Leads.objects.filter(fecha_registro__date=hoy, id_estado = 5).count()
    print(f"Leads registrados hoy: {leads_hoy}")  # Imprime el número de leads registrados hoy para depuración
    return Response({'total': leads_hoy}, status=status.HTTP_200_OK)

@api_view(['POST'])
def saveLead(request):
    request.data['id_subestado'] = 1
    request.data['estado'] = 1
    print(f"Datos recibidos para guardar lead: {request.data}")
    serializer = LeadsSaveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateLead(request, pk):
    try:
        # 1. Traemos el lead por su ID
        lead = Leads.objects.get(pk=pk)

        # 2. Obtenemos el id_asesor del request
        nuevo_asesor_id = request.data.get('id_asesor')

        # 3. Asignamos el asesor
        lead.id_asesor_id = nuevo_asesor_id

        # 4. Asignamos la fecha actual
        lead.fecha_asignacion = timezone.now()

        # 5. Guardamos
        lead.save(update_fields=['id_asesor', 'fecha_asignacion'])

        return Response({'message': 'Asesor actualizado correctamente'}, status=status.HTTP_200_OK)

    except Leads.DoesNotExist:
        return Response({'error': 'Lead no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def _normalizar_numero_peru(numero):
    numero = ''.join(caracter for caracter in str(numero or '') if caracter.isdigit())
    if not numero:
        return None
    if numero.startswith('51'):
        return numero
    return f'51{numero}'


def _formatear_fecha_llamada(fecha):
    if not fecha:
        return ''
    fecha_local = timezone.localtime(fecha) if timezone.is_aware(fecha) else fecha
    return fecha_local.strftime('%d/%m/%Y %H:%M')


def _enviar_aviso_llamada(lead, tipo='programada'):
    if not lead.id_asesor or not lead.id_asesor.telefono or not lead.fecha_llamada:
        return {
            'ok': False,
            'error': 'El lead no tiene asesor, telefono de asesor o fecha de llamada.',
            'destino': None,
        }

    destino = _normalizar_numero_peru(lead.id_asesor.telefono)
    if not destino:
        return {
            'ok': False,
            'error': 'El telefono del asesor no es valido.',
            'destino': None,
        }

    fecha_texto = _formatear_fecha_llamada(lead.fecha_llamada)
    prefijo = 'Recordatorio proximo' if tipo == 'proximo' else 'Llamada programada'
    texto = (
        f'{prefijo}\n\n'
        f'Lead: {lead.nombre}\n'
        f'Telefono: {lead.telefono or "Sin telefono"}\n'
        f'Fecha y hora: {fecha_texto}'
    )
    resultado = enviar_mensaje_detalle(destino, texto)
    return {
        **resultado,
        'destino': destino,
    }


@api_view(['PATCH'])
def programarLlamadaLead(request, id_lead):
    try:
        lead = Leads.objects.select_related('id_asesor').get(pk=id_lead)
        fecha_llamada = request.data.get('fecha_llamada')

        if not fecha_llamada:
            lead.fecha_llamada = None
            lead.recordatorio_whatsapp_enviado = 0
            lead.recordatorio_proximo_enviado = 0
            lead.save(update_fields=['fecha_llamada', 'recordatorio_whatsapp_enviado', 'recordatorio_proximo_enviado'])
            serializer = LeadsSerializer(lead)
            return Response(serializer.data, status=status.HTTP_200_OK)

        fecha_parseada = datetime.fromisoformat(str(fecha_llamada).replace('Z', '+00:00'))
        if timezone.is_naive(fecha_parseada):
            fecha_parseada = timezone.make_aware(fecha_parseada, timezone.get_current_timezone())

        lead.fecha_llamada = fecha_parseada
        lead.recordatorio_whatsapp_enviado = 0
        lead.recordatorio_proximo_enviado = 0
        lead.save(update_fields=['fecha_llamada', 'recordatorio_whatsapp_enviado', 'recordatorio_proximo_enviado'])

        serializer = LeadsSerializer(lead)
        return Response(
            {
                'lead': serializer.data,
                'aviso_whatsapp_enviado': False,
                'aviso_whatsapp_programado': True,
                'aviso_whatsapp_minutos_antes': MINUTOS_ANTES_RECORDATORIO_LLAMADA,
            },
            status=status.HTTP_200_OK
        )

    except Leads.DoesNotExist:
        return Response({'error': 'Lead no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Fecha invalida. Usa formato ISO 8601.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def revisarRecordatoriosLlamadas(request, id_asesor):
    ahora = timezone.now()
    desde = ahora - timedelta(minutes=MINUTOS_TOLERANCIA_RECORDATORIO_LLAMADA)
    limite = ahora + timedelta(minutes=MINUTOS_ANTES_RECORDATORIO_LLAMADA)

    leads = Leads.objects.select_related('id_asesor').filter(
        id_asesor=id_asesor,
        estado=1,
        fecha_llamada__gte=desde,
        fecha_llamada__lte=limite,
    ).filter(Q(recordatorio_proximo_enviado=0) | Q(recordatorio_proximo_enviado__isnull=True))

    avisos = []
    for lead in leads:
        aviso_whatsapp = _enviar_aviso_llamada(lead, 'proximo')
        aviso_enviado = bool(aviso_whatsapp.get('ok'))
        lead.recordatorio_proximo_enviado = 1 if aviso_enviado else 0
        lead.save(update_fields=['recordatorio_proximo_enviado'])
        avisos.append({
            'id_lead': lead.id_lead,
            'nombre': lead.nombre,
            'fecha_llamada': lead.fecha_llamada,
            'aviso_whatsapp_enviado': aviso_enviado,
            'aviso_whatsapp_error': aviso_whatsapp.get('error'),
            'aviso_whatsapp_status': aviso_whatsapp.get('status_code'),
        })

    return Response({'avisos': avisos}, status=status.HTTP_200_OK)



