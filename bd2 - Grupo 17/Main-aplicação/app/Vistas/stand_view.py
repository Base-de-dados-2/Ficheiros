from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ..Database.Stands import create_stand, update_stand, delete_stand, readone_stand, readjson_stand
from ..Formularios.stand_form import FormStands


# 1. Listar todos os stands
def stand_listar(request):
    try:
        stands = readjson_stand()  # Função que busca todos os stands
        return render(request, 'stand/listar.html', {'stands': stands})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao listar os stands: {e}")

# 2. Registar um novo stand
from django.shortcuts import redirect

def stand_registar(request):
    if request.method == 'POST':
        form = FormStands(request.POST)  # Preenchendo o formulário com os dados recebidos via POST
        if form.is_valid():
            # Aqui você pode processar os dados, por exemplo, salvar no banco de dados
            nome = form.cleaned_data['nome']
            localizacao = form.cleaned_data['localizacao']
            responsavel = form.cleaned_data['responsavel']

            # Processar o stand (exemplo de como salvar no banco)
            # Supondo que você tenha uma função `create_stand` para inserir no banco de dados:
            create_stand(nome, localizacao, responsavel)

            # Após o registro, redireciona para a lista de stands ou para qualquer página desejada
            return redirect('stand_listar')  # Redireciona para a lista de stands
    else:
        form = FormStands()  # Criar um formulário vazio quando for uma requisição GET

    return render(request, 'stand/registar.html', {'form': form})


# 3. Listar um stand específico pelo ID
def stand_listar_id(request, id):
    try:
        stand = readone_stand(id)  # Função que busca um stand pelo ID
        if stand:
            stand = stand[0]  # Acessa o primeiro (e único) item da lista
        return render(request, 'stand/listar_id.html', {'stand': stand})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao buscar o stand: {e}")

# 4. Atualizar um stand específico pelo ID
def stand_atualizar(request, id):
    try:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            localizacao = request.POST.get('localizacao')
            responsavel = request.POST.get('responsavel')

            # Supondo que há uma função para atualizar um stand no banco de dados
            update_stand(id, nome, localizacao, responsavel)
            return HttpResponse("Stand atualizado com sucesso!")
        else:
            stand = readone_stand(id)  # Função que busca o stand atual
            if stand:
                stand = stand[0]  # Acessa o primeiro (e único) item da lista
            return render(request, 'stand/atualizar.html', {'stand': stand})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao atualizar o stand: {e}")

def stand_atualizar(request, id):
    try:
        if request.method == 'POST':
            form = FormStands(request.POST)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                localizacao = form.cleaned_data['localizacao']
                responsavel = form.cleaned_data['responsavel']

                # Atualiza os dados no banco
                update_stand(id, nome, localizacao, responsavel)

                # Após atualizar, busca os dados atualizados para exibição
                stand = readone_stand(id)  # Buscando o stand atualizado
                if stand:
                    stand = stand[0]  # Acessando os dados do stand

                # Verifica se a atualização foi bem-sucedida antes de redirecionar
                if stand:
                    return render(request, 'stand/listar_id.html', {'stand': stand})
                else:
                    return HttpResponse("Erro ao obter o stand atualizado.")
            else:
                # Caso o formulário não seja válido, retorna a mensagem de erro
                return HttpResponse("Formulário inválido.")
        else:
            # Para o método GET, preenche o formulário com os dados do stand
            stand = readone_stand(id)
            if stand:
                stand = stand[0]
                form = FormStands(initial={
                    'nome': stand['nome'],
                    'localizacao': stand['localizacao'],
                    'responsavel': stand['responsavel'],
                })
            else:
                return HttpResponse("Stand não encontrado.")

        # Caso o formulário não seja enviado, renderiza o formulário de edição
        return render(request, 'stand/editar.html', {'form': form})

    except Exception as e:
        # Exibe um erro caso alguma exceção ocorra
        return HttpResponse(f"Ocorreu um erro ao atualizar o stand: {e}")
    

def stand_remover(request, id):
    try:
        # Buscando o stand utilizando sua função personalizada
        stand = readone_stand(id)  # Retorna um stand com base no id
        if not stand:
            return HttpResponse("Stand não encontrado.")  # Caso o stand não seja encontrado

        # Aqui você deve usar a função de remoção do stand
        delete_stand(id)  # Função que remove o stand do banco de dados ou da estrutura

        # Redireciona para a lista de stands após a exclusão
        return redirect('stand_listar')
    except Exception as e:
        # Caso ocorra algum erro, exibe uma mensagem
        return HttpResponse(f"Ocorreu um erro ao excluir o stand: {e}")