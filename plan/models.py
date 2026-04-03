from django.db import models

from sistemas.models import Sistema


class Backlog(models.Model):

    """
    El **backlog** es una lista priorizada de las tareas
    pendientes en el contexto de un proyeecto o sistema. Se
    considera una forma de documentación (**Artifact** en terminos
    de SCRUM).

    El *product owner* es el responsable de asignar la prioridad,
    miestras que el equipo de desarrollo es responsable de estimar
    el esfuerzo que llevaría imprmentarlo.

    Desde el punto de vista del Equipo, el *product backlog* es el
    trabajo que se podría hacer algún día, mientras que el *sprint
    backlog* y es el trabajo que el equipo se ha comprometido a hacer
    ahora. Esta clase solo se usa para el *product backlog*.
    """

    class Meta:
        verbose_name = 'Backlog'
        verbose_name_plural = 'Backlogs'

    class Estimacion(models.IntegerChoices):
        XS = (5, "Trivial")
        SM = (12, "Fácil")
        MD = (30, "Normal")
        LG = (70, "Complicada")
        XL = (150, "Muy difícil")

    class Prioridad(models.IntegerChoices):

        MUY_BAJA = (5, "Muy baja")
        BAJA = (12, "Baja")
        MEDIA = (30, "Media")
        ALTA = (70, "Alta")
        CRITICA = (150, "Crítica")

    id_backlog = models.BigAutoField(primary_key=True)
    sistema = models.ForeignKey(
        Sistema, 
        related_name='backlog',
        on_delete=models.CASCADE,
        )
    titulo = models.CharField(
        'Título',
        max_length=512,
        )
    explicacion = models.TextField(
        'Explicación',
        default=None,
        null=True,
        blank=True,
        )
    estimacion = models.SmallIntegerField(
        'Estimación de la complejidad',
        choices=Estimacion,
        default=Estimacion.MD,
        )
    prioridad = models.SmallIntegerField(
        'Prioridad',
        choices=Prioridad,
        default=Prioridad.MEDIA,
        )
    f_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    f_modificacion = models.DateTimeField(auto_now=True, editable=False)
    f_finalizacion = models.DateTimeField(blank=True, null=True, default=None)

    @classmethod
    def load_backlog(cls, pk: int):
        try:
            return cls.objects.get(id_backlog=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.titulo

    def touch(self):
        self.save(update_fields=['f_notificacion'])
        self.sistema.touch()

    def impacto(self):
        return self.prioridad / self.estimacion
