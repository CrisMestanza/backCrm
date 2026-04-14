from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer
from api.models import Usuarios
from django.contrib.auth.hashers import check_password 

@api_view(['POST'])
def login(request):
    correo = request.data.get('email')
    password = request.data.get('password')
    print(f"Correo: {correo}, Password: {password}")  # Debugging line
    # Buscar usuario SOLO por email
    usuario = Usuarios.objects.filter(email=correo, password=password).first()
    print(f"Usuario encontrado: {usuario}")  # Debugging line
    if usuario :
        serializer = UsuariosSerializer(usuario)
        print(f"Usuario serializado: {serializer.data}") 
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(
        {"error": "Credenciales incorrectas"},
        status=status.HTTP_401_UNAUTHORIZED
    )