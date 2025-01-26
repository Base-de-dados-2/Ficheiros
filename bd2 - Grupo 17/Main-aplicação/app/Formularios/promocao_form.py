from django import forms
from ..Database.Veiculos import readjson_veiculo  # Importar os veículos para popular o campo id_veiculo

class FormPromocao(forms.Form):
    nome_promocao = forms.CharField(
        label="Nome da Promoção",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    id_veiculo = forms.ChoiceField(
        label="Veículo",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    categoria = forms.CharField(
        label="Categoria",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    data_inicio = forms.DateField(
        label="Data de Início",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    data_terminada = forms.DateField(
        label="Data de Término",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    percentual_desconto = forms.DecimalField(
        label="Percentual de Desconto",
        max_digits=5,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    
    descricao = forms.CharField(
        label="Descrição",
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Popula o campo id_veiculo com os veículos do banco de dados
        veiculos = readjson_veiculo()
        self.fields['id_veiculo'].choices = [
            (veiculo['id'], f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})")
            for veiculo in veiculos
        ]
