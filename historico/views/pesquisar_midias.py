from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from django.templatetags.static import static
from ..models import FotoVideoNavio, Navio


@login_required
def pagina_pesquisa_midias(request):
    """Renderiza a página de pesquisa de mídias"""
    return render(request, "historico/pesquisa_midias.html")


@login_required
def pesquisar_midias(request):
    query = request.GET.get("q", "").strip()

    # 🔹 Busca todas as mídias com filtro
    midias = FotoVideoNavio.objects.select_related("navio")
    navios = Navio.objects.all()

    if query:
        filtros_midias = (
            Q(tipo_peca__icontains=query) |
            Q(observacao__icontains=query) |
            Q(navio__navio__icontains=query) |
            Q(navio__agencia__icontains=query) |
            Q(navio__armador__icontains=query)
        )

        filtros_navios = (
            Q(navio__icontains=query) |
            Q(agencia__icontains=query) |
            Q(armador__icontains=query)
        )

        # tenta converter em data
        try:
            data_formatada = datetime.strptime(query, "%d/%m/%Y").date()
            filtros_midias |= (
                Q(navio__inicio_operacao__date=data_formatada) |
                Q(navio__fim_operacao__date=data_formatada)
            )
            filtros_navios |= (
                Q(inicio_operacao__date=data_formatada) |
                Q(fim_operacao__date=data_formatada)
            )
        except ValueError:
            pass

        midias = midias.filter(filtros_midias).order_by("-data_criacao")
        navios = navios.filter(filtros_navios)
    else:
        midias = midias.order_by("-data_criacao")

    data = []

    # 🔹 Mídias com imagem/vídeo
    for midia in midias:
        data.append({
            "id": midia.id,
            "arquivo": midia.arquivo.url if midia.arquivo else static("images/placeholder_navio.jpg"),
            "is_image": midia.is_image(),
            "is_video": midia.is_video(),
            "tipo_peca": midia.tipo_peca or "Sem descrição",
            "navio": getattr(midia.navio, "navio", "---"),
            "navio_id": midia.navio.id,
            "agencia": getattr(midia.navio, "agencia", "---"),
            "armador": getattr(midia.navio, "armador", "---"),
            "inicio": midia.navio.inicio_operacao.strftime("%d/%m/%Y %H:%M") if midia.navio.inicio_operacao else None,
            "fim": midia.navio.fim_operacao.strftime("%d/%m/%Y %H:%M") if midia.navio.fim_operacao else None,
        })

    # 🔹 Navios sem mídia (usa placeholder)
    for navio in navios.exclude(id__in=midias.values_list("navio_id", flat=True)):
        data.append({
            "id": navio.id,
            "arquivo": static("images/placeholder_navio.jpg"),
            "is_image": True,
            "is_video": False,
            "tipo_peca": "(sem mídia)",
            "navio": navio.navio,
            "navio_id": navio.id,
            "agencia": getattr(navio, "agencia", "---"),
            "armador": getattr(navio, "armador", "---"),
            "inicio": navio.inicio_operacao.strftime("%d/%m/%Y %H:%M") if navio.inicio_operacao else None,
            "fim": navio.fim_operacao.strftime("%d/%m/%Y %H:%M") if navio.fim_operacao else None,
        })

    return JsonResponse({"resultados": data})
