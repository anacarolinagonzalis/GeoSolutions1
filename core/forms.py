from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'ddi': forms.TextInput(attrs={
                'type': 'number',
                'maxlength': '3',
                'oninput': 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
                'placeholder': '55'
            }),
            'ddd': forms.TextInput(attrs={
                'type': 'number',
                'maxlength': '2',
                'oninput': 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
                'placeholder': '11'
            }),
            'telefone_numero': forms.TextInput(attrs={
                'type': 'number',
                'maxlength': '9',
                'oninput': 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
                'placeholder': '999999999'
            }),
        }