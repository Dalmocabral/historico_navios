from django import forms

class LoginForm(forms.Form):
    matricula = forms.CharField(label="Matrícula", max_length=20)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
