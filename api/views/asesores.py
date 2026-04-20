from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer
from api.models import Usuarios
from django.contrib.auth.hashers import check_password 
from django.utils import timezone

@api_view(['GET'])
def getAsesores(request):
    usuarios = Usuarios.objects.filter(estado=1).order_by('-id_usuario')
    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def postAsesores(request):
    # Extraemos los datos que vienen del frontend
    data = request.data
    
    try:
        # Creamos el nuevo registro en la base de datos
        nuevo_asesor = Usuarios.objects.create(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            password=data.get('password'), # Recuerda encriptar esto luego
            rol='asesor',                  # Asignamos el rol automáticamente
            estado=1,
            fecha_creacion=timezone.now()
        )
        
        return Response({
            "message": "Asesor creado con éxito",
            "id": nuevo_asesor.id_usuario
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def deleteAsesor(request, id_usuario):
    asesor = Usuarios.objects.filter(id_usuario=id_usuario).first()

    if not asesor:
        return Response({
            "error": "Asesor no encontrado"
        }, status=status.HTTP_404_NOT_FOUND)

    asesor.estado = 0
    asesor.save(update_fields=['estado'])

    return Response({
        "message": "Asesor eliminado con exito",
        "id": asesor.id_usuario,
        "estado": asesor.estado
    }, status=status.HTTP_200_OK)