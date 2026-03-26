from django.db import models

class EstadoLead(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado_lead'


class HistorialEstadoLead(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_lead = models.ForeignKey('Leads', models.DO_NOTHING, db_column='id_lead')
    id_estado = models.ForeignKey(EstadoLead, models.DO_NOTHING, db_column='id_estado')
    id_subestado = models.ForeignKey('SubestadoLead', models.DO_NOTHING, db_column='id_subestado', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_estado_lead'
         


class Interacciones(models.Model):
    id_interaccion = models.AutoField(primary_key=True)
    id_lead = models.ForeignKey('Leads', models.DO_NOTHING, db_column='id_lead')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    id_tipo_interaccion = models.ForeignKey('TipoInteraccion', models.DO_NOTHING, db_column='id_tipo_interaccion')
    duracion_segundos = models.IntegerField(blank=True, null=True)
    duracion_minutos = models.IntegerField(blank=True, null=True)
    resultado = models.CharField(max_length=150, blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interacciones'


class Leads(models.Model):
    id_lead = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    id_origen = models.ForeignKey('OrigenLead', models.DO_NOTHING, db_column='id_origen', blank=True, null=True)
    id_proyecto_interes = models.ForeignKey('Proyectos', models.DO_NOTHING, db_column='id_proyecto_interes', blank=True, null=True)
    id_estado = models.ForeignKey(EstadoLead, models.DO_NOTHING, db_column='id_estado', blank=True, null=True)
    id_subestado = models.ForeignKey('SubestadoLead', models.DO_NOTHING, db_column='id_subestado', blank=True, null=True)
    id_asesor = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_asesor', blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_asignacion = models.DateTimeField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    nombreAsesor = models.CharField(max_length=150)
   
    class Meta:
        managed = False
        db_table = 'leads'


class OrigenLead(models.Model):
    id_origen = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'origen_lead'


class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    precio_desde = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyectos'


class SubestadoLead(models.Model):
    id_subestado = models.AutoField(primary_key=True)
    id_estado = models.ForeignKey(EstadoLead, models.DO_NOTHING, db_column='id_estado')
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'subestado_lead'


class TipoInteraccion(models.Model):
    id_tipo_interaccion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_interaccion'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=6)
    estado = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_lead = models.ForeignKey(Leads, models.DO_NOTHING, db_column='id_lead')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario')
    id_proyecto = models.ForeignKey(Proyectos, models.DO_NOTHING, db_column='id_proyecto')
    descripcion_venta = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fecha_venta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'