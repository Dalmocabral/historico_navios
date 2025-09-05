from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import FotoVideoNavio, DocumentoNavio

@login_required
def visualizar_midia(request, pk):
    midia = get_object_or_404(FotoVideoNavio, pk=pk)
    documentos = DocumentoNavio.objects.filter(navio=midia.navio)
    return render(request, "historico/visualizar_midia.html", {
        "midia": midia,
        "documentos": documentos
    })
