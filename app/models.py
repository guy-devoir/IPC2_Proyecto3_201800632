from django.db import models

# Create your models here.
class Factura(models.Model):
    lugar = models.TextField()
    fecha = models.DateTimeField()
    referencia = models.CharField(max_length=40)
    nit_e = models.CharField(max_length= 21)
    nit_r = models.CharField(max_length= 21)
    _valor = models.DecimalField(decimal_places=2, max_digits=6)
    iva = models.DecimalField(decimal_places=2, max_digits=6)
    total = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.referencia