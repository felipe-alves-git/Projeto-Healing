from django.shortcuts import render, redirect
from medico.models import *
from datetime import datetime
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import constants

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
        context = {'medicos': medicos, 'especialidades': especialidades, 'is_medico': is_medico(request.user)}
        return render(request, 'home.html', context)

def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        context = {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)}
    return render(request,'escolher_horario.html', context)

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente = request.user,
            data_aberta = data_aberta
        )

        horario_agendado.save()

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Consulta agendada com sucesso')

        return redirect ('/pacientes/minhas_consultas')
    
def minhas_consultas(request):
    minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
    context = {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)}
    return render(request, 'minhas_consultas.html', context)