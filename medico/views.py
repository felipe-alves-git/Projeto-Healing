from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import *


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


