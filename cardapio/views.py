import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Chef, Mesa, Pedido, ItemPedido
from django.utils import timezone

# -------------------------------------------------------------
# 1. VISÃO DO CLIENTE (TABLET DA MESA)
# -------------------------------------------------------------
from .models import Categoria, Prato, Chef, Mesa, Pedido, ItemPedido

def menu_mesa(request, mesa_numero=None):
    if not mesa_numero:
        mesa_numero = request.GET.get('mesa', 1)
        
    mesa = get_object_or_404(Mesa, numero=mesa_numero)
    
    # Busca pedidos ativos da mesa que ainda não foram encerrados no caixa
    pedidos_ativos = Pedido.objects.filter(mesa=mesa).exclude(status='CONCLUIDO')
    
    # Agrupa todos os itens dos pedidos para exibir no Histórico da Comanda
    itens_comanda = ItemPedido.objects.filter(pedido__in=pedidos_ativos)
    
    # Calcula o total acumulado da comanda
    total_comanda = sum(item.quantidade * (item.preco_unitario if hasattr(item, 'preco_unitario') else item.prato.preco) for item in itens_comanda)

    # Dados tradicionais do cardápio que tinham sumido
    categorias = Categoria.objects.all()
    pratos = Prato.objects.all()
    chefs = Chef.objects.all()

    return render(request, 'cardapio/menu.html', {
        'mesa': mesa,
        'itens_comanda': itens_comanda,
        'total_comanda': total_comanda,
        'categorias': categorias,
        'pratos': pratos,
        'chefs': chefs,
    })

def enviar_pedido_cozinha(request):
    if request.method == 'POST':
        numero_mesa = request.POST.get('mesa_id', 1)
        carrinho_raw = request.POST.get('carrinho_json', '[]')

        try:
            carrinho = json.loads(carrinho_raw)
        except json.JSONDecodeError:
            carrinho = []

        if not carrinho:
            return redirect(f'/?mesa={numero_mesa}')

        mesa = get_object_or_404(Mesa, numero=numero_mesa)

        # Procura APENAS um pedido que ainda esteja PENDENTE na cozinha
        pedido = Pedido.objects.filter(mesa=mesa, status='PENDENTE').first()

        if not pedido:
            # Se não houver nenhum pedido pendente (o anterior já foi entregue ou é o primeiro), cria um NOVO pedido!
            pedido = Pedido.objects.create(
                mesa=mesa,
                pago=False,
                status='PENDENTE'
            )
        else:
            # Se já houver um pedido pendente, apenas marca os antigos anteriores como não novos
            pedido.itens.update(novo=False)

        # Cria os novos itens vindos do carrinho associados ao pedido (novo ou pendente atual)
        for item in carrinho:
            ItemPedido.objects.create(
                pedido=pedido,
                prato_nome=item.get('nome', ''),
                quantidade=item.get('quantidade', 1),
                preco_unitario=item.get('preco', 0),
                novo=True
            )

        return redirect(f'/?mesa={numero_mesa}&sucesso=1')

    return redirect('/')

def marcar_entregue(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = 'ENTREGUE'  # Move para a lista de entregues
    pedido.save()
    
    pedido.itens.update(novo=False)
    return redirect('painel_cozinha')

# -------------------------------------------------------------
# 2. VISÃO DA COZINHA E PAINEL DO RESTAURANTE
# -------------------------------------------------------------
def painel_cozinha(request):

    """ Traz todos os pedidos para o painel para o JavaScript gerir as abas """
    pedidos = Pedido.objects.all().order_by('-data_criacao')  # Traz todos os estados (pendente, entregue, concluido)
    
    mesas_atendimento = Mesa.objects.filter(chamar_garcom=True)
    mesas_conta = Mesa.objects.filter(pedir_conta=True)

    return render(request, 'cardapio/cozinha.html', {
        'pedidos': pedidos,
        'mesas_atendimento': mesas_atendimento,
        'mesas_conta': mesas_conta,
        'agora': timezone.now()
    })
    

def marcar_entregue(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = 'ENTREGUE'  # Altera o status do pedido
    pedido.save()              # Salva permanentemente na base de dados
    
    pedido.itens.update(novo=False)
    return redirect('painel_cozinha')

def atualizar_status_pedido(request, pedido_id, novo_status):
    """ Altera o estado do pedido (ex: PENDENTE -> ENTREGUE -> CONCLUIDO) """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if novo_status == 'CONCLUIDO':
        pedido.status = 'CONCLUIDO'
        pedido.pago = True  # Fecha e encerra a comanda da mesa
    else:
        pedido.status = novo_status
        
    pedido.save()
    return redirect('painel_cozinha')

# Ações do Cliente no Cardápio
def chamar_garcom(request, mesa_id):
    mesa = get_object_or_404(Mesa, numero=mesa_id)
    mesa.chamar_garcom = True
    mesa.save()
    return redirect(f'/?mesa={mesa_id}&garcom=1')

# Ações da Cozinha para limpar os avisos separadamente
def atender_chamado(request, mesa_id):
    """ Limpa o aviso de chamar garçom """
    mesa = get_object_or_404(Mesa, numero=mesa_id)
    mesa.chamar_garcom = False
    mesa.save()
    return redirect('painel_cozinha')

def atender_conta(request, mesa_id):
    mesa = get_object_or_404(Mesa, numero=mesa_id)
    mesa.pedir_conta = False
    mesa.save()
    return redirect('painel_cozinha')

def fechar_conta(request, mesa_id):
    mesa = get_object_or_404(Mesa, numero=mesa_id)
    mesa.pedir_conta = True
    mesa.save()
    # Redireciona de volta para o cardápio usando exatamente o parâmetro 'conta_fechada' que o teu JS espera
    return redirect(f'/?mesa={mesa_id}&conta_fechada=1')

def finalizar_atendimento(request, mesa_numero):
    """ Encerra os pedidos ativos da mesa e limpa a comanda visual para novos clientes """

    mesa = get_object_or_404(Mesa, numero=mesa_numero)
    
    # Passa todos os pedidos ativos para CONCLUIDO (ficam registados para o histórico/faturamento)
    Pedido.objects.filter(mesa=mesa).exclude(status='CONCLUIDO').update(status='CONCLUIDO', pago=True)
    
    # Reseta os sinalizadores de atendimento e de conta
    mesa.chamar_garcom = False
    mesa.pedir_conta = False
    mesa.save()
    
    return redirect('painel_cozinha')

def painel_contas_fechadas(request):
    """ Redireciona para o painel principal onde a aba de contas fechadas está integrada """
    return redirect('painel_cozinha')

def apagar_pedido(request, pedido_id):
    """ Apaga um pedido específico do histórico da cozinha """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    return redirect('painel_cozinha')

def status_mesa(request, numero_mesa):
    """ API que retorna se a mesa tem pedidos ativos """
    mesa = get_object_or_404(Mesa, numero=numero_mesa)
    pedidos_ativos = Pedido.objects.filter(mesa=mesa).exclude(status='CONCLUIDO').exists()
    return JsonResponse({'pedidos_ativos': pedidos_ativos})