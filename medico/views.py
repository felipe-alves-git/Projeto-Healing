from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import *
from datetime import datetime, timedelta
from paciente.models import *


# Create your views here.
def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico')
        return redirect('/medicos/abrir_horario')

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        context = {'especialidades': especialidades}
        return render(request, 'cadastro_medico.html', context)
    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        crm = request.POST.get('crm')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            especialidade_id=especialidade,
            descricao=descricao,
            valor_consulta=valor_consulta,
            user = request.user
        )

        dados_medico.save()

        messages.add_message(request, constants.SUCCESS, "Cadastro médico realizado com sucesso!")

        return redirect ('/medicos/abrir_horario')
    
def abrir_horario(request):
    
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, "Somente médicos podem abrir horários!")
        return redirect('/usuarios/sair')
    
    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        context = {'dados_medicos': dados_medicos, 'datas_abertas': datas_abertas}
        return render(request, 'abrir_horario.html', context)
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, "A data não pode ser anterior a data atual")
            return redirect ('/medicos/abrir_horario')
        
        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
        )

        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário Cadastrado com Sucesso!')
        return redirect ('/medicos/abrir_horario')

def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, "Somente médicos podem abrir horários!")
        return redirect('/usuarios/sair')
    
    hoje = datetime.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje +timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))
    context = {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes}
    return render(request, 'consultas_medico.html', context)