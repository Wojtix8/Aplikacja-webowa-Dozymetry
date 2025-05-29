"""
URL configuration for projektapka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mojaapka.views import startowa_strona
from mojaapka import views
from mojaapka.views import ImportXLSXView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', startowa_strona, name='start'),
    
    # Ścieżki dla sal
    path('sala/', views.sala_list, name='sala_list'),
    path('sala/dodaj/', views.sala_create, name='sala_create'),
    path('sala/<str:pk>/usun/', views.sala_delete, name='sala_delete'),
    
    # Ścieżki dla osób
    path('osoba/', views.osoba_list, name='osoba_list'),
    path('osoba/dodaj/', views.osoba_create, name='osoba_create'),
    path('osoba/<str:pk>/usun/', views.osoba_delete, name='osoba_delete'),
    
    # Ścieżki dla sprzętu
    path('sprzet/', views.sprzet_list, name='sprzet_list'),
    path('sprzet/dodaj/', views.sprzet_create, name='sprzet_create'),
    path('sprzet/<str:pk>/usun/', views.sprzet_delete, name='sprzet_delete'),
    
    # Ścieżki dla dozymetrów
    path('dozymetr/', views.dozymetr_list, name='dozymetr_list'),
    path('dozymetr/dodaj/', views.dozymetr_create, name='dozymetr_create'),
    path('dozymetr/<str:pk>/usun/', views.dozymetr_delete, name='dozymetr_delete'),
    
    #inport/export XLSX
    path('', views.home_view, name='home'),
    path('export/xlsx/<str:model_name>/', views.ExportXLSXView.as_view(), name='export_xlsx'),
    path('import/xlsx/<str:model_name>/', ImportXLSXView.as_view(), name='import_xlsx'),


]