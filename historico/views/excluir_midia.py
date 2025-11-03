from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import FotoVideoNavio, Navio

@login_required
def excluir_midia(request, pk):
    """
    Exclui a mídia se existir; caso contrário, exclui o cadastro de navio relacionado.
    """
    try:
        # 🔹 Tenta buscar uma mídia com esse ID
        midia = FotoVideoNavio.objects.filter(pk=pk).first()

        if midia:
            # ✅ Caso exista uma mídia
            if request.method == "POST":
                midia.delete()
                return redirect("pagina_pesquisa_midias")
            
            return render(request, "historico/excluir_midia.html", {"midia": midia})

        else:
            # 🔹 Caso não exista mídia, tenta buscar o NAVIO com esse ID
            navio = Navio.objects.filter(pk=pk).first()
            if not navio:
                # Nenhum registro encontrado em nenhuma das tabelas
                return render(request, "404.html", status=404)

            # ✅ Exclui o navio se for POST
            if request.method == "POST":
                navio.delete()
                return redirect("pagina_pesquisa_midias")

            # Reaproveita o mesmo template, mas indicando que é um navio
            return render(request, "historico/excluir_midia.html", {
                "midia": None,
                "navio": navio
            })

    except Exception as e:
        print("Erro ao excluir mídia/navio:", e)
        return render(request, "404.html", status=404)
