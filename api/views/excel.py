from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import LeadsSerializer,LeadsSaveSerializer
from api.models import Leads
from django.utils import timezone
from django.contrib.auth.hashers import check_password 
from django.db import connection

@api_view(['GET'])
def getExcel(request, id_asesor):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.nombre, l.fecha_registro, 
                l.fecha_asignacion, l.telefono, 
                p.nombre_proyecto, ol.nombre,
                el.nombre, sl.nombre,
                u.nombre
            FROM crminmobiliaria.leads l
            INNER JOIN proyectos p ON p.id_proyecto = l.id_proyecto_interes
            INNER JOIN origen_lead ol ON ol.id_origen = l.id_origen
            INNER JOIN estado_lead el ON el.id_estado = l.id_estado
            INNER JOIN subestado_lead sl ON sl.id_subestado = l.id_subestado
            INNER JOIN usuarios u ON u.id_usuario = l.id_asesor
            WHERE l.id_asesor = %s
        """, [id_asesor])

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    data = [dict(zip(columns, row)) for row in rows]

    return Response(data)