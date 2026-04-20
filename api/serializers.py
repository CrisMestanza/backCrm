from rest_framework import serializers
from .models import *  # Cambia 'TuModelo' por el nombre real (ej. Propiedad o Lote)

class UsuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuarios
        fields = '__all__'

class LeadsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leads
        fields = '__all__'
        depth = 1
        
class LeadsSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leads
        fields = '__all__'

class SubestadoLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubestadoLead
        fields = '__all__'

class EstadoLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstadoLead
        fields = '__all__'
        
class InteraccionesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interacciones
        fields = '__all__'
        depth = 1
        
class SaveInteraccionesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interacciones
        fields = '__all__'
        
class TipoInteraccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoInteraccion
        fields = '__all__'
        
class OrigenLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrigenLead
        fields = '__all__'
        
class ProyectosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proyectos
        fields = '__all__'
        
        
class HistorialEstadoLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistorialEstadoLead
        fields = '__all__'
        
        
class HistorialEstadoLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistorialEstadoLead
        fields = '__all__'
        depth = 1
        
class VentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'
        # Estos campos no se validarán al recibir el JSON, 
        # permitiendo que is_valid() pase sin ellos.
        read_only_fields = [
            'id_lead', 
            'id_usuario', 
            'id_proyecto', 
            'fecha_venta'
        ]
        
class GetVentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'
        # Estos campos no se validarán al recibir el JSON, 
        # permitiendo que is_valid() pase sin ellos.
        depth = 1
        
class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = '__all__'