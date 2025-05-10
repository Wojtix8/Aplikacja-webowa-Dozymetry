from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from .models import Sala, Osoba, Sprzet, Dozymetr
from .forms import SalaForm, OsobaForm, SprzetForm, DozymetrForm
from django.db.models import Prefetch
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
import openpyxl
from io import BytesIO
from django.http import HttpResponseBadRequest
import pandas as pd

def startowa_strona(request):
    context = {
        'message': "Co chcesz wybrać Drogi Użytkowniku?",
        'selected': None,
    }

    if request.method == 'POST':
        context['selected'] = request.POST.get('wybor', 'Nic nie wybrano')

    return render(request, 'start.html', context)

# Lista i tworzenie Sali
def sala_list(request):
    sale = Sala.objects.all()
    sprzety = Sprzet.objects.all()
    dozymetry = Dozymetr.objects.select_related('sala')

    sprzety_by_sala = {}
    dozymetry_by_sala = {}

    for sprzet in sprzety:
        sprzety_by_sala.setdefault(sprzet.sala, []).append(sprzet)

    for dozymetr in dozymetry:
        dozymetry_by_sala.setdefault(dozymetr.sala, []).append(dozymetr)

    return render(request, 'sala_list.html', {
        'sale': sale,
        'sprzety_by_sala': sprzety_by_sala,
        'dozymetry_by_sala': dozymetry_by_sala,
    })

def sala_create(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sala_list')
    else:
        form = SalaForm()
    return render(request, 'sala_form.html', {'form': form})

# Lista i tworzenie Osoby
def osoba_list(request):
    osoby = Osoba.objects.all()
    dozymetry = Dozymetr.objects.select_related('osoba')
    
    dozymetry_by_osoba = {}

    for d in dozymetry:
        if d.osoba not in dozymetry_by_osoba:
            dozymetry_by_osoba[d.osoba] = []
        
        # Obliczenie daty najbliższej kontroli(dodajemy 90 dni do daty ostatniej kontroli)
        next_calibration_date = d.data_ostatniej_kontroli + timedelta(days=90)
        
        # Obliczamy liczbę dni do następnej kontroli
        days_left = (next_calibration_date - date.today()).days
        
        dozymetry_by_osoba[d.osoba].append({
            'id': d.IDdozymetru,
            'data_kontroli': d.data_ostatniej_kontroli,
            'days_left': days_left,
            'needs_calibration_alert': days_left < 14  # Dodajemy flagę dla alertu
        })

    return render(request, 'osoba_list.html', {
        'osoby': osoby,
        'dozymetry_by_osoba': dozymetry_by_osoba
    })

def osoba_create(request):
    if request.method == 'POST':
        form = OsobaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('osoba_list')
    else:
        form = OsobaForm()
    return render(request, 'osoba_form.html', {'form': form})

# Lista i tworzenie Sprzętu
def sprzet_list(request):
    return render(request, 'sprzet_list.html', {'sprzety': Sprzet.objects.select_related('sala').all()})

def sprzet_create(request):
    if request.method == 'POST':
        form = SprzetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sprzet_list')
    else:
        form = SprzetForm()
    return render(request, 'sprzet_form.html', {'form': form})

# Lista i tworzenie Dozymetrów
def dozymetr_list(request):
    return render(request, 'dozymetr_list.html', {'dozymetry': Dozymetr.objects.select_related('sala','osoba').all()})

def dozymetr_create(request):
    if request.method == 'POST':
        form = DozymetrForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dozymetr_list')
    else:
        form = DozymetrForm()
    return render(request, 'dozymetr_form.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

# Widoki do usuwania
@require_POST
def sala_delete(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    try:
        sala.delete()
        messages.success(request, 'Sala została pomyślnie usunięta.')
    except Exception as e:
        messages.error(request, f'Wystąpił błąd podczas usuwania sali: {e}')
    return redirect('sala_list')

@require_POST
def osoba_delete(request, pk):
    osoba = get_object_or_404(Osoba, pk=pk)
    try:
        osoba.delete()
        messages.success(request, 'Osoba została pomyślnie usunięta.')
    except Exception as e:
        messages.error(request, f'Wystąpił błąd podczas usuwania osoby: {e}')
    return redirect('osoba_list')

@require_POST
def sprzet_delete(request, pk):
    sprzet = get_object_or_404(Sprzet, pk=pk)
    try:
        sprzet.delete()
        messages.success(request, 'Sprzęt został pomyślnie usunięty.')
    except Exception as e:
        messages.error(request, f'Wystąpił błąd podczas usuwania sprzętu: {e}')
    return redirect('sprzet_list')

@require_POST
def dozymetr_delete(request, pk):
    dozymetr = get_object_or_404(Dozymetr, pk=pk)
    try:
        dozymetr.delete()
        messages.success(request, 'Dozymetr został pomyślnie usunięty.')
    except Exception as e:
        messages.error(request, f'Wystąpił błąd podczas usuwania dozymetru: {e}')
    return redirect('dozymetr_list')

class ExportXLSXView(View):
    models = {
        'sale': {
            'model': Sala,
            'fields': ['nr_sali', 'oddzial', 'sprzety', 'dozymetry'],  
            'filename': 'lista_sal.xlsx'
        },
        'osoby': {
            'model': Osoba,
            'fields': ['imie', 'nazwisko', 'dozymetry'],
            'filename': 'lista_osob.xlsx'
        },
        'sprzety': {
            'model': Sprzet,
            'fields': ['nazwa', 'rok_produkcji', 'numer_ref', 'sala'],
            'filename': 'lista_sprzetu.xlsx'
        },
        'dozymetry': {
            'model': Dozymetr,
            'fields': ['IDdozymetru', 'typ', 'status', 'data_ostatniej_kontroli', 'sala', 'osoba'],
            'filename': 'lista_dozymetrow.xlsx'
        }
    }

    def get(self, request, model_name):
        if model_name not in self.models:
            return HttpResponse("Nieprawidłowy model", status=400)

        config = self.models[model_name]
        queryset = config['model'].objects.all()
        
        return self.generate_xlsx(queryset, config['fields'], config['filename'])

    def generate_xlsx(self, queryset, fields, filename):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Dane"

        for col_num, field in enumerate(fields, 1):
            worksheet.cell(row=1, column=col_num, value=field)

        for row_num, obj in enumerate(queryset, 2):
            for col_num, field in enumerate(fields, 1):
                value = getattr(obj, field)
                if hasattr(value, '__dict__'):
                    value = str(value)
                worksheet.cell(row=row_num, column=col_num, value=value)

        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


