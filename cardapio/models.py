from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

class Prato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='pratos')
    nome = models.CharField(max_length=150)
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço')
    imagem = models.ImageField(upload_to='pratos/',null =True, blank=True,verbose_name='Image do Prato')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')
    destaque = models.BooleanField(default=False,verbose_name="Destaques dos Mais Pedidos")

class Chef(models.Model):

       
       nome = models.CharField(max_length=100)
       carg0 = models.CharField(max_length=100, default="Chef Exercutivo")
       bio = models.TextField(verbose_name="Descrição/Biografia")
       foto = models.ImageField(upload_to='chef/')
       ativo = models.BooleanField(default=False,help_text="Exibir no site")


       def __str__(self):
          return self.nome

class Mesa(models.Model):

    numero = models.IntegerField(unique=True,verbose_name="Numero da Mesa")
    ativa = models.BooleanField(default=True,verbose_name="Mesa Ocupada?")
    chamar_garcom = models.BooleanField(default=False) # Apenas para o atendimento
    pedir_conta = models.BooleanField(default=False)

    def __str__(self):
       return f"Mesa{self.numero}"
     
class Pedido(models.Model):
    STATUS_CHOICES =[
        ('PENDENTE', 'Em Preparo(Cozinha)'),
        ('PRONTO','Prato Pronto'),
        ('ENTREGUE', 'Entrega para Salão'),
        ('CONCLUIDO', 'Conta Paga/ Fechada'),
    ]
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='PENDENTE')
    pago = models.BooleanField(default=False)

    def total_pedido(self):
        return sum(item.subtotal() for item in self.itens.all())
    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    prato_nome = models.CharField(max_length=150)
    preco_unitario = models.DecimalField(max_digits=8,decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)
    novo = models.BooleanField(default=True)

    def subtotal(self):
        return self.preco_unitario * self.quantidade
    
    def __str__(self):
        return f"{self.quantidade}x {self.prato_nome}"