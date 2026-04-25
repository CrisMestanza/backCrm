from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UsuariosSerializer
from api.models import Usuarios
from django.utils import timezone


@api_view(['GET'])
def getAsesores(request):
    usuarios = Usuarios.objects.filter(estado=1).order_by('-id_usuario')
    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def postAsesores(request):
    data = request.data

    try:
        nuevo_asesor = Usuarios.objects.create(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            password=data.get('password'),
            rol=data.get('rol', 'ASESOR').upper(),
            estado=1,
            fecha_creacion=timezone.now()
        )

        return Response({
            "message": "Asesor creado con exito",
            "id": nuevo_asesor.id_usuario
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateAsesor(request, id_usuario):
    asesor = Usuarios.objects.filter(id_usuario=id_usuario).first()

    if not asesor:
        return Response({
            "error": "Asesor no encontrado"
        }, status=status.HTTP_404_NOT_FOUND)

    campos_permitidos = ['nombre', 'email', 'telefono', 'password', 'rol', 'estado']
    campos_actualizados = []

    for campo in campos_permitidos:
        if campo in request.data:
            valor = request.data.get(campo)
            if campo == 'rol' and valor:
                valor = valor.upper()
            setattr(asesor, campo, valor)
            campos_actualizados.append(campo)

    if campos_actualizados:
        asesor.save(update_fields=campos_actualizados)

    serializer = UsuariosSerializer(asesor)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
