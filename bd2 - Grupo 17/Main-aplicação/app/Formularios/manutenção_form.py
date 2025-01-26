from django import forms
from ..Database.Veiculos import readjson_veiculo  # Importar os veículos para popular o campo id_veiculo

class FormManutencao(forms.Form):
    id_veiculo = forms.ChoiceField(
        label="Veículo",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    data_manutencao = forms.DateField(
        label="Data da Manutenção",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    tipo_manutencao = forms.CharField(
        label="Tipo de Manutenção",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    descricao = forms.CharField(
        label="Descrição",
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )
    
    oficina_responsavel = forms.CharField(
        label="Oficina Responsável",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Popula o campo id_veiculo com os veículos do banco de dados
        veiculos = readjson_veiculo()
        self.fields['id_veiculo'].choices = [
            (veiculo['id'], f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})")
            for veiculo in veiculos
        ]
