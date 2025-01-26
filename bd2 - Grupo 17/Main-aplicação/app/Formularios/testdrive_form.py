from django import forms
from ..Database.Cliente import readjson_cliente  # Função para obter os clientes existentes
from ..Database.Veiculos import readjson_veiculo  # Função para obter os veículos existentes

class FormTestDrive(forms.Form):
    """Formulário para registrar ou atualizar um test drive."""
    
    id_cliente = forms.ChoiceField(
        label="Cliente", 
        choices=[],  # As opções serão preenchidas dinamicamente com os clientes
        required=True
    )
    
    id_veiculo = forms.ChoiceField(
        label="Veículo", 
        choices=[],  # As opções serão preenchidas dinamicamente com os veículos
        required=True
    )
    
    data_hora_testdrive = forms.DateTimeField(
        label="Data e Hora do Test Drive", 
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        required=True
    )
    
    feedback_cliente = forms.CharField(
        label="Feedback do Cliente", 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Digite o feedback do cliente'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe pai
        super(FormTestDrive, self).__init__(*args, **kwargs)

        # Preenche os campos dinâmicamente
        clientes = readjson_cliente()  # Pega os clientes existentes
        veiculos = readjson_veiculo()  # Pega os veículos existentes

        # Preenche as opções para os clientes
        self.fields['id_cliente'].choices = [(cliente['id_cliente'], f"{cliente['id_cliente']} - {cliente['nome']}") for cliente in clientes]

        # Preenche as opções para os veículos
        self.fields['id_veiculo'].choices = [(veiculo['id'], f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})") for veiculo in veiculos]
