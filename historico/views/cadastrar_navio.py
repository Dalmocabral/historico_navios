from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..forms import NavioForm, DocumentoNavioForm
from ..models import Navio, DocumentoNavio, FotoVideoNavio

@login_required
def cadastrar_navio(request):
    if request.method == "POST":
        navio_form = NavioForm(request.POST)
        documento_form = DocumentoNavioForm(request.POST, request.FILES)
        midias_files = request.FILES.getlist('midias')
        arquivos_pdf = request.FILES.getlist('arquivos')
        observacoes = request.POST.getlist('observacoes')
        tipos_pecas = request.POST.getlist('tipo_peca')  # Adicione esta linha

        if navio_form.is_valid():
            # Salvar o navio
            navio = navio_form.save(commit=False)
            navio.criado_por = request.user
            navio.save()

            # Salvar PDFs
            for arquivo in arquivos_pdf:
                if arquivo.content_type == 'application/pdf':
                    DocumentoNavio.objects.create(navio=navio, arquivo=arquivo)

            # Salvar fotos/vídeos com tipo de peça
            for idx, file in enumerate(midias_files):
                obs = observacoes[idx] if idx < len(observacoes) else ""
                tipo_peca = tipos_pecas[idx] if idx < len(tipos_pecas) else ""  # Adicione esta linha
                FotoVideoNavio.objects.create(
                    navio=navio, 
                    arquivo=file, 
                    observacao=obs,
                    tipo_peca=tipo_peca  # Adicione esta linha
                )

            # Mensagem de sucesso
            messages.success(request, "Navio cadastrado com sucesso!")
            
            # REDIRECT em vez de render - Isso evita o reenvio ao recarregar
            return redirect(reverse('cadastrar_navio') + '?sucesso=true')
        
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    
    else:
        navio_form = NavioForm()
        documento_form = DocumentoNavioForm()

    # Verifica se veio de um redirect de sucesso
    sucesso = request.GET.get('sucesso', False)
    
    return render(request, "historico/cadastro_navio.html", {
        "navio_form": navio_form,
        "documento_form": documento_form,
        "cadastro_sucesso": sucesso
    })