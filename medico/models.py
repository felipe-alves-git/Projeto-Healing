from django.db import models
from django.contrib.auth.models import User

def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()
    

# Create your models here.
class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.especialidade
    

class DadosMedico(models.Model):
    crm = models.CharField(max_length=30)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField(max_length=100)
    rg = models.ImageField(upload_to='rgs')
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to='fotos_perfil')
    descricao = models.TextField()
    valor_consulta = models.FloatField(default=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.user.username
    
class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return self.data
    