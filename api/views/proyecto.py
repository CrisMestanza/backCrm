from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,OrigenLeadSerializer, ProyectosSerializer
from api.models import Leads, OrigenLead, Proyectos
from django.utils import timezone
from django.contrib.auth.hashers import check_password 


@api_view(['GET'])
def getProyectos(request):
    proyectos = Proyectos.objects.all()
    serializer = ProyectosSerializer(proyectos, many=True)
    return Response(serializer.data)