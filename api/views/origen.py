from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,OrigenLeadSerializer
from api.models import Leads, OrigenLead
from django.utils import timezone
from django.contrib.auth.hashers import check_password 


@api_view(['GET'])
def getOrigen(request):
    origen = OrigenLead.objects.all()
    serializer = OrigenLeadSerializer(origen, many=True)
    return Response(serializer.data)