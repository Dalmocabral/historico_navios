# admin.py
from django import forms
from django.contrib import admin
from .models import Colaborador, Navio, FotoVideoNavio, DocumentoNavio


# === COLABORADOR ===
class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        exclude = ['user']  # Exclui o campo user do formulário


class ColaboradorAdmin(admin.ModelAdmin):
    form = ColaboradorForm
    readonly_fields = ['user']
    list_display = ['nome', 'sobrenome', 'matricula', 'cpf']
    search_fields = ['nome', 'sobrenome', 'matricula', 'cpf']


# === NAVIO ===
class NavioAdmin(admin.ModelAdmin):
    list_display = ['navio', 'armador', 'agencia', 'eta', 'pob', 'inicio_operacao', 'fim_operacao']
    list_filter = ['agencia', 'armador']
    search_fields = ['navio', 'armador', 'agencia']
    date_hierarchy = 'eta'
    ordering = ['-eta']


# === FOTO / VÍDEO NAVIO ===
class FotoVideoNavioAdmin(admin.ModelAdmin):
    list_display = ['navio', 'tipo_peca', 'data_criacao']
    list_filter = ['tipo_peca', 'data_criacao']
    search_fields = ['navio__navio', 'tipo_peca']


# === DOCUMENTO NAVIO ===
class DocumentoNavioAdmin(admin.ModelAdmin):
    list_display = ['navio', 'arquivo']
    search_fields = ['navio__navio']


# === REGISTROS ===
admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Navio, NavioAdmin)
admin.site.register(FotoVideoNavio, FotoVideoNavioAdmin)
admin.site.register(DocumentoNavio, DocumentoNavioAdmin)
