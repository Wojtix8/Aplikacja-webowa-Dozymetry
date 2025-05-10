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
        fields = ['nazwa', 'rok_produkcji', 'numer_ref', 'sala']

class DozymetrForm(forms.ModelForm):
    class Meta:
        model = Dozymetr
        fields = ['IDdozymetru', 'data_ostatniej_kontroli', 'status', 'typ', 'sala', 'osoba']
        widgets = {
            'data_ostatniej_kontroli': forms.DateInput(attrs={'type':'date'}),
        }
