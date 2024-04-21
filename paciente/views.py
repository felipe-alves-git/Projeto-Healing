from django.shortcuts import render
from medico.models import *
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        especialidade_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedico.objects.all()

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)

        if especialidade_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidade_filtrar)

        especialidades = Especialidades.objects.all()
        context = {'medicos': medicos, 'especialidades': especialidades}
        return render(request, 'home.html', context)

def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        context = {'medico': medico, 'datas_abertas': datas_abertas}
    return render(request,'escolher_horario.html', context)