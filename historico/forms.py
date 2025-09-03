from django import forms
from .models import Navio, FotoVideoNavio, DocumentoNavio




# Agora defina os formulários que usam MultipleFileField
class LoginForm(forms.Form):
    matricula = forms.CharField(label="Matrícula", max_length=20)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class DocumentoNavioForm(forms.Form):
    arquivos = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'application/pdf'}),
        required=False,
        label="Selecionar PDFs"
    )

class NavioForm(forms.ModelForm):
    class Meta:
        model = Navio
        fields = [
            "boca", "armador", "agencia", "lado", "eta", "pob",
            "local_atracacao", "inicio_operacao", "ternos", "tempo_operacao",
            "volume_descarga", "clientes_descarga", "volume_embarque", "clientes_embarque",
        ]
        widgets = {
            "eta": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "pob": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "inicio_operacao": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class FotoVideoNavioForm(forms.ModelForm):
    class Meta:
        model = FotoVideoNavio
        fields = ["arquivo", "observacao"]
        widgets = {"observacao": forms.Textarea(attrs={"rows": 2})}
