from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import NavioForm, DocumentoNavioForm, FotoVideoNavioForm
from ..models import Navio, DocumentoNavio, FotoVideoNavio
@login_required
def cadastrar_navio(request):
    cadastro_sucesso = False  # Flag para modal

    if request.method == "POST":
        navio_form = NavioForm(request.POST)
        documento_form = DocumentoNavioForm(request.POST, request.FILES)
        midias_files = request.FILES.getlist('midias')
        arquivos_pdf = request.FILES.getlist('arquivos')
        observacoes = request.POST.getlist('observacoes')

        if navio_form.is_valid():
            navio = navio_form.save(commit=False)
            navio.criado_por = request.user
            navio.save()

            # Salvar PDFs
            for arquivo in arquivos_pdf:
                if arquivo.content_type == 'application/pdf':
                    DocumentoNavio.objects.create(navio=navio, arquivo=arquivo)

            # Salvar fotos/vídeos
            for idx, file in enumerate(midias_files):
                obs = observacoes[idx] if idx < len(observacoes) else ""
                FotoVideoNavio.objects.create(navio=navio, arquivo=file, observacao=obs)

            cadastro_sucesso = True  # Para disparar modal
            navio_form = NavioForm()  # Limpa o formulário
            documento_form = DocumentoNavioForm()  # Limpa PDFs
        else:
            messages.error(request, "Corrija os erros no formulário.")

    else:
        navio_form = NavioForm()
        documento_form = DocumentoNavioForm()

    return render(request, "historico/cadastro_navio.html", {
        "navio_form": navio_form,
        "documento_form": documento_form,
        "cadastro_sucesso": cadastro_sucesso
    })
