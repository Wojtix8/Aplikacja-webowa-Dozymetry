from django import forms
from .models import Sala, Osoba, Sprzet, Dozymetr

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nr_sali', 'oddzial']

class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = ['imie', 'nazwisko']

class SprzetForm(forms.ModelForm):
    class Meta:
        model = Sprzet
        fields = [
            'model',
            'producent',
            'typ_sprzetu',
            'data_ostatniego_przegladu',
            'promieniujacy',
            'status',
            'numer_seryjny',
            'rok_zakupu',
            'numer_kontaktowy_serwis',
            'sala',
        ]
        widgets = {
            'data_ostatniego_przegladu': forms.DateInput(attrs={'type': 'date'}),
        }

class DozymetrForm(forms.ModelForm):
    class Meta:
        model = Dozymetr
        fields = ['IDdozymetru', 'data_ostatniej_kontroli', 'status', 'typ', 'sala', 'osoba']
        widgets = {
            'data_ostatniej_kontroli': forms.DateInput(attrs={'type':'date'}),
        }
