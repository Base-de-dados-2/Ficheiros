from django import forms
import datetime  # Para obter a data atual

class FormUtilizadores(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(label='Telefone', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Campo 'tipo_utilizador' com apenas as opções 0 ou 1
    TIPO_UTILIZADOR_CHOICES = [
        (0, 'Cliente'),
        (1, 'Admin'),
    ]
    tipo_utilizador = forms.ChoiceField(
        label='Tipo de Utilizador',
        choices=TIPO_UTILIZADOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_criacao = forms.DateField(label='Data de Criação', widget=forms.DateInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Preenche o campo 'data_de_criacao' com a data atual se não for fornecida
        if not kwargs.get('initial'):
            kwargs['initial'] = {}
        kwargs['initial']['data_criacao'] = datetime.date.today()  # Define a data atual
        super().__init__(*args, **kwargs)

    def preencher_form(self, dados):
        """Preenche o formulário com os dados recebidos."""
        for key, value in dados.items():
            if key in self.fields:  # Certifique-se de que a chave existe no formulário
                self.fields[key].initial = value
