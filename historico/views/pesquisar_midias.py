from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from ..models import FotoVideoNavio

@login_required
def pagina_pesquisa_midias(request):
    """Renderiza a página de pesquisa de mídias"""
    return render(request, "historico/pesquisa_midias.html")


@login_required
def pesquisar_midias(request):
    """Retorna os resultados da busca em JSON"""
    query = request.GET.get("q", "").strip()
    resultados = FotoVideoNavio.objects.select_related("navio")

    if query:
        resultados = resultados.filter(
            Q(tipo_peca__icontains=query) |
            Q(observacao__icontains=query) |
            Q(navio__navio__icontains=query)
        )
    else:
        resultados = resultados.order_by("-data_criacao")

    data = []
    for midia in resultados:
        data.append({
            "id": midia.id,
            "tipo_peca": midia.tipo_peca,
            "arquivo": midia.arquivo.url,
            "is_image": midia.is_image(),
            "is_video": midia.is_video(),
            "navio": midia.navio.navio if midia.navio else "",
            "inicio": midia.navio.inicio_operacao.strftime("%d/%m/%Y %H:%M") if midia.navio.inicio_operacao else "",
            "fim": midia.navio.fim_operacao.strftime("%d/%m/%Y %H:%M") if midia.navio.fim_operacao else "",
        })
    return JsonResponse({"resultados": data})



@login_required
def editar_midia(request, pk):
    midia = get_object_or_404(FotoVideoNavio, pk=pk)
    # aqui você pode implementar formulário de edição
    return render(request, "historico/editar_midia.html", {"midia": midia})


@login_required
def excluir_midia(request, pk):
    midia = get_object_or_404(FotoVideoNavio, pk=pk)
    if request.method == "POST":
        midia.delete()
        return redirect("pesquisar_midias")
    return render(request, "historico/excluir_midia.html", {"midia": midia})
