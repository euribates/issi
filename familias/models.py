from django.db import models
from django.db.models.functions import Coalesce


class FamiliaManager(models.Manager):

    def with_counts(self):
        return self.annotate(num_sistemas=Coalesce(models.Count("sistemas"), 0))


class Familia(models.Model):
    class Meta:
        verbose_name = "familia"
        verbose_name_plural = "familias"
        db_table = 'fam_familia'
        ordering = [
            "id_familia",
        ]

    id_familia = models.CharField(max_length=3, primary_key=True)
    nombre_familia = models.CharField(max_length=128)

    objects = FamiliaManager()

    @classmethod
    def load_familia(cls, pk: str):
        try:
            return cls.objects.get(id_familia=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self) -> str:
        return str(self.nombre_familia)

    def no_definida(self) -> bool:
        return self.pk == "UNK"
