from django.core.management.base import BaseCommand
from django.utils.timezone import now
from core1.models import Solicitud


class Command(BaseCommand):
    help= 'verifica y actualiza solicitudes'
    def handle(self, *args, **kwargs):
        solicitudes= Solicitud.objects.filter(expirada=False, fecha_expiracion__lt=now().date())
        for solicitud in solicitudes:
            solicitud.check_expiracion()
            self.stdout.write(self.style.SUCCESS(f'{solicitudes.count()} solicitudes actualizadas.'))
        
