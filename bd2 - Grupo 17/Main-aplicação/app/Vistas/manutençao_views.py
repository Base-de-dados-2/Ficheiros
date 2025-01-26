from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.Manuteção import (
    create_manutencao, update_manutencao, delete_manutencao, readone_manutencao, readjson_manutencao
)
from ..Formularios.manutenção_form import FormManutencao
from ..Database.Veiculos import readone_veiculo

# Listar todas as manutenções
def manutencao_listar(request):
    try:
        manutencoes = readjson_manutencao()
        return render(request, 'Manutenção/listar.html', {'manutencoes': manutencoes})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Listar uma manutenção por ID
from ..Database.Veiculos import readjson_veiculo  # Importar a função para listar todos os veículos

def manutencao_listar_id(request, id):
    try:
        manutencao = readone_manutencao(id)
        if manutencao:
            manutencao = manutencao[0]  # Primeiro item da lista
        veiculos = readjson_veiculo()  # Obter todos os veículos
        return render(request, 'Manutenção/listar_id.html', {'manutencao': manutencao, 'veiculos': veiculos})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")


# Registrar nova manutenção
def manutencao_registar(request):
    try:
        if request.method == 'POST':
            form = FormManutencao(request.POST)
            if form.is_valid():
                create_manutencao(
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    data_manutencao=form.cleaned_data['data_manutencao'],
                    tipo_manutencao=form.cleaned_data['tipo_manutencao'],
                    descricao=form.cleaned_data['descricao'],
                    oficina_responsavel=form.cleaned_data['oficina_responsavel']
                )
                return redirect("manutencao_listar")
        else:
            form = FormManutencao()
        return render(request, 'Manutenção/registar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Atualizar manutenção existente
def manutencao_atualizar(request, id):
    try:
        manutencao = readone_manutencao(id)
        if not manutencao:
            return HttpResponse("Manutenção não encontrada.")
        
        manutencao = manutencao[0]  # Primeiro item da lista

        if request.method == 'POST':
            form = FormManutencao(request.POST)
            if form.is_valid():
                update_manutencao(
                    id,
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    data_manutencao=form.cleaned_data['data_manutencao'],
                    tipo_manutencao=form.cleaned_data['tipo_manutencao'],
                    descricao=form.cleaned_data['descricao'],
                    oficina_responsavel=form.cleaned_data['oficina_responsavel']
                )
                return redirect("manutencao_listar")
        else:
            form = FormManutencao(initial={
                'id_veiculo': manutencao['id_veiculo'],
                'data_manutencao': manutencao['data_manutencao'],
                'tipo_manutencao': manutencao['tipo_manutencao'],
                'descricao': manutencao['descricao'],
                'oficina_responsavel': manutencao['oficina_responsavel']
            })

        return render(request, 'Manutenção/editar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Remover manutenção
def manutencao_remover(request, id):
    try:
        delete_manutencao(id)
        return redirect("manutencao_listar")
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover a manutenção: {e}")
