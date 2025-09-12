from django.db import models

class Organismo(models.Model):
    id_organismo = models.BigIntegerField(primary_key=True)
    nombre_organismo = models.CharField(
        max_length=144,
        unique=True,
        )
    dir3 = models.CharField(max_length=9, unique=True)
    id_sirhus = models.IntegerField(unique=True)
    categoria = models.CharField(max_length=40)
    depende_de = models.ForeignKey(
        'Organismo',
        related_name='organismos_dependientes',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        )
    ruta = models.CharField(
        max_length=128,
        default='',
        )

    @classmethod
    def load_organismo(cls, pk:int):
        try:
            return cls.objects.get(id_organismo=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def upsert(cls, id_organismo, **kwargs):
         organismo, created = cls.objects.update_or_create(
            pk=id_organismo,
            defaults=kwargs,
            )
         return organismo, created

    

    def __str__(self):
        return self.nombre_organismo

    def calcula_ruta(self):
        self.ruta = f'{self.depende.ruta}{SEP}{self.depende_de.pk}'

    def es_primer_nivel(self) -> bool:
        return self.depende_de.pk == 1
    
    
