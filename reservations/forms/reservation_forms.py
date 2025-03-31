from django import forms
from django.utils import timezone
from datetime import timedelta, time, datetime


class ReservationForm(forms.Form):
    people = forms.IntegerField(min_value=1)
    date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()

    def clean_date(self):
        date = self.cleaned_data['date']
        hoy = timezone.localdate()
        if date < hoy:
            raise forms.ValidationError("No puede reservar en el pasado")
        if date > hoy + timedelta(days=14):
            raise forms.ValidationError("Máximo 14 días de anticipación")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if not all([date, start_time, end_time]):
            return

        # Validar horarios
        if start_time < time(7) or start_time >= time(23):
            self.add_error('start_time', "Hora inicio inválida")

        if end_time > time(23):
            self.add_error('end_time', "Hora fin inválida")

        if start_time >= end_time:
            self.add_error('end_time', "Hora fin debe ser posterior")

        # Duración
        inicio = datetime.combine(date, start_time)
        fin = datetime.combine(date, end_time)
        if (fin - inicio).total_seconds() > 28800:  # 8 horas
            self.add_error(None, "Duración máxima excedida")

        # Validar hora actual para hoy
        if date == timezone.localdate():
            ahora = timezone.localtime().time()
            if start_time < ahora:
                self.add_error(
                    'start_time', "Hora debe ser posterior al ahora")

        return cleaned_data
