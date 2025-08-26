from django.db import models


class Norma(models.Model):
    id_norma = models.BigAutoField(primary_key=True)
    nombre_norma = models.TextField(max_length=620, unique=True)
    sobrenombre = models.CharField(max_length=32, blank=True)
    url = models.URLField(max_length=320, blank=True)
    id_juriscan = models.IntegerField(default=0)

    def __str__(self):
        if self.sobrenombre:
            return f'{self.sobrenombre} - {self.nombre_norma}'
        return self.nombre_norma

