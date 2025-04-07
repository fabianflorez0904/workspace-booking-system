from django.core.management.base import BaseCommand
from reservations.tasks import update_reservation_statuses


class Command(BaseCommand):
    help = 'Actualiza los estados de las reservas basado en el tiempo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Actualizando estados de reservas...')
        result = update_reservation_statuses()
        self.stdout.write(self.style.SUCCESS(f'Estados de reservas actualizados: {result}')) 