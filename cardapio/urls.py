from django.urls import path
from . import views

urlpatterns = [
    # Visão do Cliente
    path('', views.menu_mesa, name='cardapio'),
    path('fazer-pedido/', views.enviar_pedido_cozinha, name='enviar_pedido_cozinha'),
    
    # Visão da Cozinha
    path('cozinha/', views.painel_cozinha, name='painel_cozinha'),
    path('cozinha/entregar/<int:pedido_id>/', views.marcar_entregue, name='marcar_entregue'),

    # Chamada do Garçom e Gestão de Alertas
    path('chamada_garcom/<int:mesa_id>/', views.chamar_garcom, name='chamar_garcom'),
    path('atender_chamado/<int:mesa_id>/', views.atender_chamado, name='atender_chamado'), # <-- ADICIONADO AQUI
    path('atender_conta/<int:mesa_id>/', views.atender_conta, name='atender_conta'),
    path('fechar_conta/<int:mesa_id>/', views.fechar_conta, name='fechar_conta'),
    path('finalizar-atendimento/<int:mesa_numero>/', views.finalizar_atendimento, name='finalizar_atendimento'),

    # Painel de Histórico e Contas Fechadas
    path('cozinha/contas-fechadas/', views.painel_contas_fechadas, name='contas_fechadas'),
    path('cozinha/apagar/<int:pedido_id>/', views.apagar_pedido, name='apagar_pedido'),
    
    # API de Status da Mesa (Consumida exclusivamente pelo cardápio online)
    path('status-mesa/<int:numero_mesa>/', views.status_mesa, name='status_mesa'),
]