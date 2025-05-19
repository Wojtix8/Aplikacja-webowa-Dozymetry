from django.db import models

class Sala(models.Model):
    nr_sali = models.CharField(max_length=10, primary_key=True)
    oddzial = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nr_sali} – {self.oddzial}"

class Osoba(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Sprzet(models.Model):
    STATUS_CHOICES = [
        ('aktywne', 'Aktywne'),
        ('w_naprawie', 'W naprawie'),
        ('wycofane', 'Wycofane'),
        ('uszkodzone', 'Uszkodzone'),
    ]

    TYP_SPRZETU_CHOICES = [
        ('RTG', 'Aparat RTG'),
        ('TK', 'Tomograf komputerowy'),
        ('USG', 'Ultrasonograf'),
        ('PET', 'PET'),
        ('SPECT', 'SPECT'),
        ('MRI', 'Rezonans magnetyczny'),
        ('CID', 'Detektor promieniowania jonizującego'),
        ('GAUGE', 'Miernik promieniowania'),
        ('INNE', 'Inne'),
    ]

    model = models.CharField(max_length=100)
    producent = models.CharField(max_length=100)
    typ_sprzetu = models.CharField(max_length=50, choices=TYP_SPRZETU_CHOICES)
    data_ostatniego_przegladu = models.DateField(blank=True, null=True)
    promieniujacy = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktywne')
    numer_seryjny = models.CharField(max_length=100)
    rok_zakupu = models.CharField(max_length=4)  
    numer_kontaktowy_serwis = models.CharField(max_length=20, blank=True, null=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nazwa} – {self.producent_model}"

class Dozymetr(models.Model):
    STATUS_CHOICES = [
        ('aktywny','Aktywny'),
        ('wycofany','Wycofany'),
        ('w_naprawie','W naprawie'),
        ('zutylizowany','Zutylizowany'),
    ]

    IDdozymetru = models.CharField(max_length=20, primary_key=True)
    data_ostatniej_kontroli = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    typ = models.CharField(max_length=50)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='dozymetry')
    osoba = models.ForeignKey(Osoba, on_delete=models.CASCADE, related_name='dozymetry')

    def __str__(self):
        return self.IDdozymetru
