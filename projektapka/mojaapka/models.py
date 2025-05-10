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
    nazwa = models.CharField(max_length=100)
    rok_produkcji = models.PositiveSmallIntegerField(null=True, blank=True)
    numer_ref = models.CharField(max_length=50, unique=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sprzety')

    def __str__(self):
        return self.nazwa

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
