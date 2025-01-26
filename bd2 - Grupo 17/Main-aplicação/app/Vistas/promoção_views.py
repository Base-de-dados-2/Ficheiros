from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.promocao import (
    create_promocao, update_promocao, delete_promocao, readone_promocao, readjson_promocao
)
from ..Database.Veiculos import readjson_veiculo
from ..Formularios.promocao_form import FormPromocao

# Listar todas as promoções
def promocao_listar(request):
    try:
        promocoes = readjson_promocao()
        return render(request, 'Promocao/listar.html', {'promocoes': promocoes})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao listar promoções: {e}")

# Detalhes de uma promoção
def promocao_detalhes(request, id):
    try:
        promocao = readone_promocao(id)
        veiculos = readjson_veiculo()

        if promocao:
            promocao = promocao[0]  # Pegar o primeiro item da lista

        return render(request, 'Promocao/detalhes.html', {
            'promocao': promocao,
            'veiculos': veiculos,
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao buscar detalhes da promoção: {e}")

# Registrar nova promoção
def promocao_registar(request):
    try:
        veiculos = readjson_veiculo()

        if request.method == 'POST':
            form = FormPromocao(request.POST)
            if form.is_valid():
                create_promocao(
                    nome_promocao=form.cleaned_data['nome_promocao'],
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    categoria=form.cleaned_data['categoria'],
                    data_inicio=form.cleaned_data['data_inicio'],
                    data_terminada=form.cleaned_data['data_terminada'],
                    percentual_desconto=form.cleaned_data['percentual_desconto'],
                    descricao=form.cleaned_data['descricao']
                )
                return redirect('promocao_listar')
        else:
            form = FormPromocao()

        return render(request, 'Promocao/registar.html', {
            'form': form,
            'veiculos': veiculos
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao registrar promoção: {e}")

# Atualizar uma promoção existente
def promocao_atualizar(request, id):
    try:
        promocao = readone_promocao(id)
        veiculos = readjson_veiculo()

        if not promocao:
            return HttpResponse("Promoção não encontrada.")

        promocao = promocao[0]

        if request.method == 'POST':
            form = FormPromocao(request.POST)
            if form.is_valid():
                update_promocao(
                    id_promocao=id,
                    nome_promocao=form.cleaned_data['nome_promocao'],
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    categoria=form.cleaned_data['categoria'],
                    data_inicio=form.cleaned_data['data_inicio'],
                    data_terminada=form.cleaned_data['data_terminada'],
                    percentual_desconto=form.cleaned_data['percentual_desconto'],
                    descricao=form.cleaned_data['descricao']
                )
                return redirect('promocao_listar')
        else:
            form = FormPromocao(initial={
                'nome_promocao': promocao['nome_promocao'],
                'id_veiculo': promocao['id_veiculo'],
                'categoria': promocao['categoria'],
                'data_inicio': promocao['data_inicio'],
                'data_terminada': promocao['data_terminada'],
                'percentual_desconto': promocao['percentual_desconto'],
                'descricao': promocao['descricao']
            })

        return render(request, 'Promocao/editar.html', {
            'form': form,
            'veiculos': veiculos
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao atualizar a promoção: {e}")

# Remover uma promoção
def promocao_remover(request, id):
    try:
        delete_promocao(id)
        return redirect('promocao_listar')
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover a promoção: {e}")
