from django.db import models

# Create your models here.
class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.especialidade