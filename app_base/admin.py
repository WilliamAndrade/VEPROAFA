from django.contrib import admin
from .models import Produto,Producao,TipoPagamento,Cooperativa,Assinatura,Endereco,Cliente

# Register your models here.

admin.site.register(Produto)
admin.site.register(Producao)
admin.site.register(TipoPagamento)
admin.site.register(Cooperativa)
admin.site.register(Assinatura)
admin.site.register(Endereco)
admin.site.register(Cliente)