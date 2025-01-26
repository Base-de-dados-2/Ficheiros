from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Formularios.vendedor_form import FormVendedor
from ..Database.Vendedor import readjson_vendedor, readone_vendedor, create_vendedor, update_vendedor
from ..Database.Utilizador import readjson_utilizador 

def vendedor_listar(request):
    try:
        vendedores = readjson_vendedor()  # Lê todos os vendedores
        return render(request, 'Vendedor/listar.html', {'vendedores': vendedores})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

def vendedor_listar_id(request, id):
    try:
        vendedor = readone_vendedor(id)
        if vendedor:
            vendedor = vendedor[0]  # Acessa o primeiro item da lista

        # Obter todos os utilizadores para passar para o template
        utilizadores = readjson_utilizador()

        return render(request, 'Vendedor/detalhes.html', {'vendedor': vendedor, 'utilizadores': utilizadores})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

def vendedor_registar(request):
    try:
        utilizadores = readjson_utilizador()  # Pega os utilizadores existentes

        if request.method == 'POST':
            form = FormVendedor(request.POST)
            if form.is_valid():
                create_vendedor(
                    id_utilizador=form.cleaned_data['id_utilizador'],
                    cargo=form.cleaned_data['cargo'],
                    vendas_realizadas=form.cleaned_data['vendas_realizadas']
                )
                return redirect("vendedor_listar")
        else:
            form = FormVendedor()

        return render(request, 'Vendedor/registar.html', {
            'form': form,
            'utilizadores': utilizadores
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

def vendedor_atualizar(request, id):
    try:
        vendedor = readone_vendedor(id)
        utilizadores = readjson_utilizador()  # Pega os utilizadores existentes

        if not vendedor:
            return HttpResponse("Vendedor não encontrado.")
        
        vendedor = vendedor[0]  # Primeiro item da lista

        if request.method == 'POST':
            form = FormVendedor(request.POST)
            if form.is_valid():
                update_vendedor(
                    id_vendedor=id,
                    id_utilizador=form.cleaned_data['id_utilizador'],
                    cargo=form.cleaned_data['cargo'],
                    vendas_realizadas=form.cleaned_data['vendas_realizadas']
                )
                return redirect("vendedor_listar")
        else:
            form = FormVendedor(initial={
                'id_utilizador': vendedor['id_utilizador'],
                'cargo': vendedor['cargo'],
                'vendas_realizadas': vendedor['vendas_realizadas'],
            })

        return render(request, 'Vendedor/editar.html', {
            'form': form,
            'utilizadores': utilizadores
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

from ..Database.Vendedor import delete_vendedor

def vendedor_remover(request, id):
    try:
        delete_vendedor(id)
        return redirect("vendedor_listar")
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover o vendedor: {e}")
