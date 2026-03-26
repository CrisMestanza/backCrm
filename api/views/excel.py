from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Leads

@api_view(['GET'])
def getExcel(request, id_asesor):
    # .select_related realiza los INNER JOIN automáticamente
    # Asegúrate de usar los nombres de los campos exactos definidos en tu modelo Leads
    leads_queryset = Leads.objects.filter(id_asesor=id_asesor).select_related(
        'id_proyecto_interes', 
        'id_origen', 
        'id_estado', 
        'id_subestado', 
        'id_asesor'
    )

    data = []
    for lead in leads_queryset:
        data.append({
            "nombre": lead.nombre,
            "fecha_registro": lead.fecha_registro,
            "fecha_asignacion": lead.fecha_asignacion,
            "telefono": lead.telefono,
            # Accedemos a los objetos relacionados de forma sencilla
            "nombre_proyecto": lead.id_proyecto_interes.nombre_proyecto if lead.id_proyecto_interes else None,
            "origen": lead.id_origen.nombre if lead.id_origen else None,
            "estado": lead.id_estado.nombre if lead.id_estado else None,
            "sub_estado": lead.id_subestado.nombre if lead.id_subestado else None,
            "asesor": lead.id_asesor.nombre if lead.id_asesor else None,
        })

    return Response(data)