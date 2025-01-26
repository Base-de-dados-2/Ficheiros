from django import forms
from ..Database.Veiculos import readjson_veiculo  # Função para obter os veículos existentes

class FormHistoricoVeiculo(forms.Form):
    """Formulário para registrar ou atualizar o histórico do veículo."""
    
    id_veiculo = forms.ChoiceField(
        label="Veículo", 
        choices=[],  # As opções serão preenchidas dinamicamente com os veículos
        required=True
    )
    
    manutencoes = forms.CharField(
        label="Manutenções Realizadas", 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva as manutenções realizadas'}),
        required=False
    )
    
    acidentes = forms.CharField(
        label="Acidentes", 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva os acidentes ocorridos'}),
        required=False
    )
    
    dono_anterior = forms.CharField(
        label="Dono Anterior", 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o dono anterior'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe pai
        super(FormHistoricoVeiculo, self).__init__(*args, **kwargs)

        # Preenche os campos dinamicamente
        veiculos = readjson_veiculo()  # Pega os veículos existentes

        # Preenche as opções para os veículos
        self.fields['id_veiculo'].choices = [(veiculo['id'], f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})") for veiculo in veiculos]
