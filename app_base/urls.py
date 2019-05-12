from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('logout',views.my_logout,name='my_logout'),
    path('cooperativa/create/', views.cooperativa_create,name='cooperativa_create'),
    path('cooperativa/view/', views.cooperativa_view,name='cooperativa_view'),
    path('cooperativa/update/<int:id>', views.cooperativa_update,name='cooperativa_update'),
    path('endereco/update/<int:id>', views.endereco_update,name='endereco_update'),
    path('producao/list/', views.producao_list,name='producao_list'),
    path('producao/create/', views.producao_create,name='producao_create'),
    path('producao/update/<int:id>', views.producao_update,name='producao_update'),
    path('producao/delete/<int:id>', views.producao_delete,name='producao_delete'),
    path('produto/list/', views.produto_list,name='produto_list'),
    path('produto/view/<int:id>', views.produto_view,name='produto_view'),
    path('assinatura/create/', views.assinatura_create,name='assinatura_create'),
    path('assinatura/list/', views.assinatura_list,name='assinatura_list'),
    path('assinatura/update/<int:id>', views.assinatura_update,name='assinatura_update'),
    path('assinatura/delete/<int:id>', views.assinatura_delete,name='assinatura_delete')
]
