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
    print(f"Intento de login con email: {correo}")  
    print(f"Intento de login con password: {password}")  
    
    # Validar campos vacíos
    if not correo or not password:
        return Response(
            {"success": False, "message": "Email y password son requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Buscar usuario
    usuario = Usuarios.objects.filter(email=correo, password=password).first()

    if usuario:
        serializer = UsuariosSerializer(usuario)
        return Response(
            {
                "success": True,
                "message": "Login correcto",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "success": False,
            "message": "Credenciales incorrectas"
        },
        status=status.HTTP_401_UNAUTHORIZED
    )