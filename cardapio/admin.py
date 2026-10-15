from django.contrib import admin
from .models import Categoria, Prato ,Chef

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')

@admin.register(Prato)
class PratoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel')
    list_filter = ('categoria', 'disponivel')
    search_fields = ('nome', 'descricao')

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display =('nome', 'ativo')
    list_filter =('ativo',)