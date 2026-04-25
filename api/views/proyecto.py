from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ProyectosSerializer
from api.models import Proyectos


@api_view(['GET'])
def getProyectos(request):
    proyectos = Proyectos.objects.exclude(estado=0).order_by('-id_proyecto')
    serializer = ProyectosSerializer(proyectos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def postProyectos(request):
    serializer = ProyectosSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(estado=1)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateProyecto(request, id_proyecto):
    proyecto = Proyectos.objects.filter(id_proyecto=id_proyecto).first()

    if not proyecto:
        return Response({
            "error": "Proyecto no encontrado"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProyectosSerializer(proyecto, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def deleteProyecto(request, id_proyecto):
    proyecto = Proyectos.objects.filter(id_proyecto=id_proyecto).first()

    if not proyecto:
        return Response({
            "error": "Proyecto no encontrado"
        }, status=status.HTTP_404_NOT_FOUND)

    proyecto.estado = 0
    proyecto.save(update_fields=['estado'])

    return Response({
        "message": "Proyecto eliminado con exito",
        "id": proyecto.id_proyecto,
        "estado": proyecto.estado
    }, status=status.HTTP_200_OK)
