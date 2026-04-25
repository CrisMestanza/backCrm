from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer
from api.models import Usuarios

@api_view(['POST'])
def login(request):
    correo = request.data.get('email')
    password = request.data.get('password')

    if not correo or not password:
        return Response(
            {"error": "Ingresa tu correo y contrasena."},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario = Usuarios.objects.filter(email=correo).first()

    if not usuario:
        return Response(
            {"error": "No existe un usuario registrado con ese correo."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if usuario.password != password:
        return Response(
            {"error": "La contrasena ingresada es incorrecta."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if usuario.estado == 0:
        return Response(
            {"error": "Tu usuario esta inactivo. Contacta al administrador."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = UsuariosSerializer(usuario)
    return Response(serializer.data, status=status.HTTP_200_OK)
