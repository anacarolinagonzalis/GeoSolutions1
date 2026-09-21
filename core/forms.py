from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'ddi': forms.TextInput(attrs={
                'type': 'text',
                'inputmode': 'numeric',
                'maxlength': '3',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '55'
            }),
            'ddd': forms.TextInput(attrs={
                'type': 'text',
                'inputmode': 'numeric',
                'maxlength': '2',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '11'
            }),
            'telefone_numero': forms.TextInput(attrs={
                'type': 'text',
                'inputmode': 'numeric',
                'maxlength': '10',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '999999999'
            }),
        }