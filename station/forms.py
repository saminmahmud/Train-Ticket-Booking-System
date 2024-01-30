from django import forms
from .models import Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name']

    def save(self, commit=True):
        station = super().save(commit=False)
        station.slug = self.cleaned_data['name'].replace(' ', '-').lower()
        if commit:
            station.save()
        return station