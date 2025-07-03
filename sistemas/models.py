from django.db import models


class Tema(models.Model):
    id_tema = models.CharField(max_length=3, primary_key=True)
    nombre_tema = models.CharField(max_length=32)
    
    def __str__(self):
        return self.nombre_tema


class Sistema(models.Model):
    id_sistema = models.BigAutoField(primary_key=True)
    dir3_id = models.CharField(max_length=9)
    codigo = models.CharField(max_length=32, unique=True)
    nombre = models.CharField(max_length=220)
    descripcion = models.CharField(max_length=512)
    explicacion = models.TextField(blank=True, default='')
    temas = models.ManyToManyField(
        Tema,
        related_name='sistemas',
        through='Clasificacion',
        )
    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Clasificacion(models.Model):
    id_clasificacion = models.BigAutoField(primary_key=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.PROTECT)
