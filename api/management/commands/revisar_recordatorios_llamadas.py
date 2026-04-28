from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from api.models import Leads
from api.views.leads import MINUTOS_ANTES_RECORDATORIO_LLAMADA, _enviar_aviso_llamada


class Command(BaseCommand):
    help = 'Envia recordatorios de llamadas proximas por WhatsApp a los asesores.'

    def handle(self, *args, **options):
        ahora = timezone.now()
        limite = ahora + timedelta(minutes=MINUTOS_ANTES_RECORDATORIO_LLAMADA)

        leads = Leads.objects.select_related('id_asesor').filter(
            estado=1,
            fecha_llamada__gte=ahora,
            fecha_llamada__lte=limite,
        ).filter(Q(recordatorio_proximo_enviado=0) | Q(recordatorio_proximo_enviado__isnull=True))

        enviados = 0
        for lead in leads:
            aviso_whatsapp = _enviar_aviso_llamada(lead, 'proximo')
            aviso_enviado = bool(aviso_whatsapp.get('ok'))
            lead.recordatorio_proximo_enviado = 1 if aviso_enviado else 0
            lead.save(update_fields=['recordatorio_proximo_enviado'])
            enviados += 1 if aviso_enviado else 0

        self.stdout.write(self.style.SUCCESS(f'Recordatorios enviados: {enviados}'))
