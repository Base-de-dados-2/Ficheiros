from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.testdrive import create_testdrive, update_testdrive, delete_testdrive, readone_testdrive, readjson_testdrive
from ..Formularios.testdrive_form import FormTestDrive
from ..Database.Cliente import readjson_cliente
from ..Database.Veiculos import readjson_veiculo


# Listar todos os test drives
def testdrive_listar(request):
    try:
        testdrives = readjson_testdrive()  # Lê todos os test drives
        for testdrive in testdrives:
            print(f"Test drive ID: {testdrive.get('id_testdrive')}")  # Verifique se o id_testdrive está correto
            if not testdrive.get('id_testdrive'):
                print("Test drive com ID inválido:", testdrive)
        return render(request, 'Test_drive/listar.html', {'testdrives': testdrives})  # Certifique-se de usar a extensão .html
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")



# Exibir detalhes de um test drive
def testdrive_detalhes(request, id_testdrive):
    try:
        testdrive = readone_testdrive(id_testdrive)
        if testdrive:
            testdrive = testdrive[0]  # Acessa o primeiro item da lista
        else:
            return HttpResponse("Test drive não encontrado.")
        
        # Pega os clientes e veículos existentes
        clientes = readjson_cliente()
        veiculos = readjson_veiculo()

        return render(request, 'Test_drive/detalhes.html', {
            'testdrive': testdrive,
            'clientes': clientes,
            'veiculos': veiculos,
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")


# Registrar um novo test drive
def testdrive_registrar(request):
    try:
        clientes = readjson_cliente()  # Lista de clientes
        veiculos = readjson_veiculo()  # Lista de veículos

        if request.method == 'POST':
            form = FormTestDrive(request.POST)
            if form.is_valid():
                create_testdrive(
                    id_cliente=form.cleaned_data['id_cliente'],
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    data_hora_testdrive=form.cleaned_data['data_hora_testdrive'],
                    feedback_cliente=form.cleaned_data['feedback_cliente']
                )
                return redirect('testdrive_listar')  # Redireciona para a lista
            else:
                print("Erros do formulário:", form.errors)
                return HttpResponse("Formulário inválido.")

        else:
            form = FormTestDrive()

        return render(request, 'Test_drive/registar.html', {
            'form': form,
            'clientes': clientes,
            'veiculos': veiculos,
        })

    except Exception as e:
        print(f"Erro ao registrar Test Drive: {e}")
        return HttpResponse(f"Ocorreu um erro: {e}")





# Atualizar um test drive existente
from django.utils import timezone

def testdrive_atualizar(request, id_testdrive):
    try:
        testdrive = readone_testdrive(id_testdrive)
        if not testdrive:
            return HttpResponse("Test drive não encontrado.")

        testdrive = testdrive[0]  # Pega o primeiro item da lista (deve ser um único item)

        # Pega a lista de clientes e veículos para preencher os campos do formulário
        clientes = readjson_cliente()  # Lista de clientes
        veiculos = readjson_veiculo()  # Lista de veículos

        # Formatação da data para o formato esperado no input datetime-local
        data_hora_testdrive = testdrive['data_hora_testdrive']
        if isinstance(data_hora_testdrive, str):
            data_hora_testdrive = timezone.make_aware(timezone.datetime.strptime(data_hora_testdrive, '%Y-%m-%d %H:%M:%S'))

        data_hora_testdrive_formatada = data_hora_testdrive.strftime('%Y-%m-%dT%H:%M')

        if request.method == 'POST':
            form = FormTestDrive(request.POST)
            if form.is_valid():
                update_testdrive(
                    id_testdrive=id_testdrive,
                    id_cliente=form.cleaned_data['id_cliente'],
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    data_hora_testdrive=form.cleaned_data['data_hora_testdrive'],
                    feedback_cliente=form.cleaned_data['feedback_cliente']
                )
                return redirect('testdrive_listar')  # Redireciona para a lista de test drives
        else:
            form = FormTestDrive(initial={
                'id_cliente': testdrive['id_cliente'],
                'id_veiculo': testdrive['id_veiculo'],
                'data_hora_testdrive': data_hora_testdrive_formatada,  # Usa a data formatada
                'feedback_cliente': testdrive['feedback_cliente']
            })

        return render(request, 'Test_drive/editar.html', {
            'form': form,
            'clientes': clientes,  # Passa a lista de clientes para o template
            'veiculos': veiculos,  # Passa a lista de veículos para o template
        })

    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")




# Remover um test drive
def testdrive_remover(request, id_testdrive):
    try:
        delete_testdrive(id_testdrive)  # Função para remover o test drive pelo ID
        return redirect('testdrive_listar')  # Redireciona para a lista de test drives
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover o test drive: {e}")

def testdrive_listar_id(request, id):
    try:
        testdrive = readone_testdrive(id)
        clientes = readjson_cliente()
        veiculos = readjson_veiculo()

        if testdrive:
            testdrive = testdrive[0]  # Acessa o primeiro item da lista

        return render(request, 'Test_drive/detalhes.html', {
            'testdrive': testdrive,
            'clientes': clientes,
            'veiculos': veiculos,
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")