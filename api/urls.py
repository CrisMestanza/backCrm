from django.urls import path
from .views.login import *
from .views.asesores import *
from .views.leads import *
from .views.estados import *
from .views.iteraciones import *
from .views.origen import *
from .views.proyecto import *
from .views.historialEstadoLead import *
from .views.ventas import *
from .views.excel import *

urlpatterns = [
    path('login/', login, name='login'),
    
    # Asesores
    path('getasesores/', getAsesores, name='asesores'),
    
    #Leads 
    path('getleads/<int:id_asesor>/', getLead, name='leads'),
    path('totalleads/', totalLeads, name='total-leads'),
    path('totalleadshoy/', totalLeadsHoy, name='total-leads-hoy'),
    path('savelead/', saveLead, name='save-lead'),
    path('updatelead/<int:pk>/', updateLead, name='update-lead'),
    
    # Estados y Subestados
    path('getestados/', getEstados, name='estados'),
    path('getsubestados/<int:id_estado>/', getSubestados, name='subestados'),
    path('updateleadestado/<int:id_lead>/', updateLeadEstado, name='update-lead-estado'),
    path('updateleadsubestado/<int:id_lead>/', updateLeadSubEstado, name='update-lead-subestado'),
    
    # Iteraciones
    path('getiteraciones/<int:id_usuario>/<int:id_lead>/', getIteraciones, name='get-iteraciones'),
    path('saveiteracion/', saveIteraciones, name='save-iteracion'),
    path('gettipointeraccion/', getTipoIteracion, name='get-tipo-interaccion'),
    
    # Origen
    path('getorigen/', getOrigen, name='get-origen'),
    
    # Proyectos
    path('getpoyectos/', getProyectos, name='get-proyectos'),
    
    # Ventas
    path('saveventas/<int:id_lead>/', saveVentas, name='save-ventas'),
    path('getventas/', getVentas, name='get-ventas'), 
    path('totalleadsgeneral/', totalLeadsGeneral, name='total-leads-general'), 
    path('totalleadsVendidos/', totalLeadsVendidos, name='total-leads-vendidos'),
    
    # Ventas asesores
    path('getVentasASesor/<int:id_asesor>/', getVentasASesor, name='get-ventas-asesor'), 
    path('totalleadsgeneralAsesor/<int:id_asesor>/', totalLeadsGeneralAsesor, name='total-leads-general-asesor'), 
    path('totalleadsVendidosAsesor/<int:id_asesor>/', totalLeadsVendidosAsesor, name='total-leads-vendidos-asesor'),
   
    # Historial Estado Lead
    path('gethistorialestadolead/<int:id_asesor>/', getHistorialEstadoLead, name='get-historial-estado-lead'),
    
    # Excel
    path('getexcel/<int:id_asesor>/', getExcel, name='get-ventas'), 
    
]