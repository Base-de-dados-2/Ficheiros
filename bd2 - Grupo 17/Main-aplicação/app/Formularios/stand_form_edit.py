from django import forms

class StandForm(forms.Form):
    nome = forms.CharField(
        label='Nome',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    localizacao = forms.CharField(
        label='Localização',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    responsavel = forms.CharField(
        label='Responsável',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def preencher_form(self, dados):
        """Preenche o formulário com os dados recebidos."""
        for key, value in dados.items():
            if key in self.fields:
                self.fields[key].initial = value
