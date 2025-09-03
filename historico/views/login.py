from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ..forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data["matricula"]
            senha = form.cleaned_data["senha"]

            user = authenticate(request, username=matricula, password=senha)
            if user is not None:
                login(request, user)
                return redirect("dashboard")  # redireciona pro dashboard
            else:
                form.add_error(None, "Matrícula ou senha inválidos.")
    else:
        form = LoginForm()
    return render(request, "historico/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")
