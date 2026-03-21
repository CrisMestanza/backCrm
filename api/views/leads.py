from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,LeadsSaveSerializer
from api.models import Leads
from django.utils import timezone
from django.contrib.auth.hashers import check_password 


@api_view(['GET'])
def getLead(request, id_asesor):
    leads = Leads.objects.filter(id_asesor=id_asesor).order_by('-fecha_registro')
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

    print("Datos recibidos:", request.data)  # Imprime los datos recibidos para depuración
    request.data['id_subestado'] = 1
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



