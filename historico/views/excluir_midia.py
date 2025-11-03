from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import FotoVideoNavio, Navio

@login_required
def excluir_midia(request, pk):
    """
    Exclui o registro principal (Navio) vinculado à mídia informada.
    Se o ID pertencer a uma mídia, o navio relacionado será excluído.
    Se o ID pertencer diretamente a um navio, ele será excluído junto com tudo.
    """
    try:
        # 🔹 Tenta identificar se o ID pertence a uma mídia
        midia = FotoVideoNavio.objects.filter(pk=pk).first()

        if midia:
            navio = midia.navio  # Pega o navio da mídia
        else:
            # 🔹 Caso contrário, tenta achar o navio diretamente
            navio = Navio.objects.filter(pk=pk).first()

        if not navio:
            # Nenhum registro encontrado
            return redirect("pagina_pesquisa_midias")

        # ✅ Exclui o navio (e automaticamente as mídias e documentos ligados)
        if request.method == "POST":
            navio.delete()
            return redirect("pagina_pesquisa_midias")

        # Reaproveita o mesmo template para confirmação
        return render(request, "historico/excluir_midia.html", {
            "midia": midia,
            "navio": navio
        })

    except Exception as e:
        print("Erro ao excluir registro:", e)
        return redirect("pagina_pesquisa_midias")
