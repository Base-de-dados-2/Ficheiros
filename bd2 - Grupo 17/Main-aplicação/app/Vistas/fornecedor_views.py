from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.Fornecedor import (
    create_fornecedor, update_fornecedor, delete_fornecedor, readone_fornecedor, readjson_fornecedor
)
from ..Formularios.fornecedor_form import FormFornecedor

# Listar todos os fornecedores
def fornecedor_listar(request):
    try:
        fornecedores = readjson_fornecedor()
        return render(request, 'Fornecedores/listar.html', {'fornecedores': fornecedores})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Listar um fornecedor por ID
def fornecedor_listar_id(request, id):
    try:
        fornecedor = readone_fornecedor(id)
        if fornecedor:
            fornecedor = fornecedor[0]  # Acessa o primeiro item da lista
        return render(request, 'Fornecedores/listar_id.html', {'fornecedor': fornecedor})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")


# Registrar novo fornecedor
def fornecedor_registar(request):
    try:
        if request.method == 'POST':
            form = FormFornecedor(request.POST)
            if form.is_valid():
                # Garantir que 'veiculos_fornecedor' é tratado como uma string
                veiculos_fornecedor = str(form.cleaned_data['veiculos_fornecedor'])

                # Passar o valor como string para a função create_fornecedor
                create_fornecedor(
                    nome=form.cleaned_data['nome'],
                    contato=form.cleaned_data['contato'],
                    veiculos_fornecedor=veiculos_fornecedor  # Garantindo que seja string
                )
                return redirect("fornecedor_listar")
        else:
            form = FormFornecedor()
        return render(request, 'Fornecedores/registar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")


# Atualizar fornecedor existente
def fornecedor_atualizar(request, id):
    try:
        fornecedor = readone_fornecedor(id)
        if not fornecedor:
            return HttpResponse("Fornecedor não encontrado.")
        
        fornecedor = fornecedor[0]  # Primeiro item da lista

        if request.method == 'POST':
            form = FormFornecedor(request.POST)
            if form.is_valid():
                update_fornecedor(
                    id,
                    nome=form.cleaned_data['nome'],
                    contato=form.cleaned_data['contato'],
                    veiculos_fornecedor=form.cleaned_data['veiculos_fornecedor']
                )
                return redirect("fornecedor_listar")
        else:
            form = FormFornecedor(initial={
                'nome': fornecedor['nome'],
                'contato': fornecedor['contato'],
                'veiculos_fornecedor': fornecedor['veiculos_fornecedor'],
            })

        return render(request, 'Fornecedores/editar.html', {'form': form})

    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Remover fornecedor
def fornecedor_remover(request, id):
    try:
        delete_fornecedor(id)
        return redirect("fornecedor_listar")
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover o fornecedor: {e}")
