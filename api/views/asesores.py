from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer
from api.models import Usuarios
from django.contrib.auth.hashers import check_password 

@api_view(['GET'])
def getAsesores(request):
    usuarios = Usuarios.objects.all()
    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)