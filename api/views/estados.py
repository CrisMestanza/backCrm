from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from api.models import SubestadoLead, EstadoLead
from django.utils import timezone
from django.contrib.auth.hashers import check_password 


@api_view(['GET'])
def getEstados(request):
    leads = EstadoLead.objects.all()
    serializer = EstadoLeadSerializer(leads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSubestados(request, id_estado):
    leads = SubestadoLead.objects.filter(id_estado=id_estado)
    serializer = SubestadoLeadSerializer(leads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def updateLeadEstado(request, id_lead):
    try:
        # 1. Traemos el lead por su ID
        lead = Leads.objects.get(pk=id_lead)

        # 2. Obtenemos el id_subestado del request
        nuevo_estado_id = request.data.get('id_estado')

        # 3. Asignamos el estado
        lead.id_estado_id = nuevo_estado_id

        # 4. Guardamos
        lead.save(update_fields=['id_estado'])

        return Response({'message': 'estado actualizado correctamente'}, status=status.HTTP_200_OK)

    except Leads.DoesNotExist:
        return Response({'error': 'Lead no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateLeadSubEstado(request, id_lead):
    try:
        # 1. Traemos el lead
        lead = Leads.objects.get(pk=id_lead)

        # 2. Obtenemos el ID del subestado del request
        nuevo_subestado_id = request.data.get('id_subestado')

        # 3. Actualizamos el subestado del Lead usando el sufijo _id
        lead.id_subestado_id = nuevo_subestado_id
        lead.save(update_fields=['id_subestado']) # Asegúrate que el campo se llame así

        # 4. Guardar en HistorialEstadoLead
        # Usamos el sufijo _id para los campos que son ForeignKey
        historial = HistorialEstadoLead(
            id_lead=lead, 
            id_estado=lead.id_estado,
            id_subestado_id=nuevo_subestado_id, # <--- CAMBIO AQUÍ
            fecha=timezone.now(),
            id_usuario=lead.id_asesor, # Asumiendo que id_asesor ya es una instancia
            comentario=request.data.get('comentario', '')
        )
        historial.save()

        return Response({'message': 'subestado actualizado correctamente'}, status=status.HTTP_200_OK)

        
    except Leads.DoesNotExist:
        return Response({'error': 'Lead no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("ERROR REAL:", str(e)) # Esto saldrá en tu consola de VSCode/Terminal
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)