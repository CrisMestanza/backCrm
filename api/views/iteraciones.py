from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer, InteraccionesSerializer, TipoInteraccionSerializer, SaveInteraccionesSerializer
from api.models import Interacciones, TipoInteraccion, Usuarios, Leads
from django.contrib.auth.hashers import check_password 
from django.utils import timezone

@api_view(['POST'])
def saveIteraciones(request):

    data = request.data.copy()
    data['fecha'] = timezone.now()

    serializer = SaveInteraccionesSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTipoIteracion(request):
    tipo_interaccion = TipoInteraccion.objects.all()
    serializer = TipoInteraccionSerializer(tipo_interaccion, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getIteraciones(request, id_usuario, id_lead):
    print("ID USUARIO:", id_usuario)
    print("ID LEAD:", id_lead)
    iteraciones = Interacciones.objects.filter(id_usuario = id_usuario, id_lead = id_lead).order_by('-fecha')
    serializer = InteraccionesSerializer(iteraciones, many=True)
    return Response(serializer.data)
