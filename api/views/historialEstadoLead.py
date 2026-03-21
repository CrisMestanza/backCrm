from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,LeadsSaveSerializer, HistorialEstadoLeadSerializer
from api.models import Leads, HistorialEstadoLead
from django.utils import timezone
from django.contrib.auth.hashers import check_password 


@api_view(['GET'])
def getHistorialEstadoLead(request, id_asesor):
    historialLeads = HistorialEstadoLead.objects.filter(id_lead=id_asesor)
    serializer = HistorialEstadoLeadSerializer(historialLeads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)