from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from api.models import Ventas, Leads
from django.utils import timezone
from django.contrib.auth.hashers import check_password 

@api_view(['POST'])
def saveVentas(request, id_lead):
    try:
        lead = Leads.objects.get(pk=id_lead)
        
        # Pasamos los datos del request al serializer
        serializer = VentasSerializer(data=request.data)
        
        if serializer.is_valid():
            # Al llamar a save(), inyectamos los campos faltantes
            serializer.save(
                id_lead=lead,
                id_usuario=lead.id_asesor, # Objeto Usuario
                id_proyecto=lead.id_proyecto_interes, # Objeto Proyecto
                fecha_venta=timezone.now(),
                # Mapeamos 'monto' del JSON al campo 'precio_venta' del modelo
                precio_venta=request.data.get('monto') 
            )

            # Actualizar estado del Lead a Vendido (ID 4)
            # Nota: Asegúrate de que lead.id_estado es el nombre correcto en tu modelo Leads
            lead.id_estado_id = 4 
            lead.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Si falla, esto te devolverá exactamente qué campo falta o está mal
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Leads.DoesNotExist:
        return Response({'error': 'Lead no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getVentas(request):
    ventas = Ventas.objects.all()
    serializer = GetVentasSerializer(ventas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def totalLeadsGeneral(request):
    leads = Leads.objects.all().count()
    return Response({'total': leads}, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalLeadsVendidos(request):
    leads_vendidos = Ventas.objects.all().count()
    return Response({'total_vendidos': leads_vendidos}, status=status.HTTP_200_OK)

# Para el asesor
@api_view(['GET'])
def getVentasASesor(request, id_asesor):
    ventas = Ventas.objects.filter(id_usuario=id_asesor)
    serializer = GetVentasSerializer(ventas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def totalLeadsGeneralAsesor(request, id_asesor):
    leads = Leads.objects.filter(id_asesor=id_asesor).count()
    return Response({'total': leads}, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalLeadsVendidosAsesor(request, id_asesor):
    leads_vendidos = Ventas.objects.filter(id_usuario=id_asesor).count()
    return Response({'total_vendidos': leads_vendidos}, status=status.HTTP_200_OK)

