# 🍽️ Sistema de Gestão para Restaurante (Cardápio Digital & KDS)

Sistema web full-stack desenvolvido em **Python (Django)** para automatizar o atendimento de mesas, pedidos em tempo real (KDS - Kitchen Display System), gestão modular de estilos e controlo de comandas de restaurantes.

---

## 🚀 Funcionalidades do Projeto

### 📱 1. Cardápio Digital e Comanda do Cliente (`menu.html`)
* **Visualização por Categorias:** Navegação fluida por categorias de pratos e produtos disponíveis.
* **Carrossel de Chefs:** Secção dinâmica em destaque com a equipa de chefs utilizando a biblioteca *Swiper.js*.
* **Carrinho de Compras Interativo:** Adição, remoção e cálculo automático de subtotais e totais dos pratos selecionados diretamente no painel lateral.
* **Histórico da Comanda Acumulado:** Visualização em tempo real de todos os itens já enviados pela mesa para a cozinha, com somatório total acumulado.
* **Ações Rápidas da Mesa:**
  * 🔔 **Chamar Garçom:** Notificação imediata para o atendimento de salão.
  * 💳 **Pedir a Conta / Encerrar:** Solicitação direta de fecho de conta da mesa.
* **Notificações e Modais Personalizados:** Avisos visuais (*toasts*) e caixas de diálogo modais para validação de ações do cliente.

### 👨‍🍳 2. Painel da Cozinha / KDS (`cozinha.html`)
* **Gestão de Pedidos em Tempo Real:** Visualização imediata dos pedidos enviados pelas mesas.
* **Mudança de Estado de Produção:** Acompanhamento e atualização dinâmica do estado dos pratos (pendente, em preparação, concluído, entregue).
* **Filtros e Relatórios Integrados:** Abas dedicadas para gerir pedidos pendentes, entregues, contas fechadas e histórico faturado.



---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Django, SQLite
* **Frontend:** HTML5, CSS3, JavaScript
* **Bibliotecas:** Swiper.js (Carrosséis)
* **Controlo de Versões:** Git & GitHub

---

## 📦 Como Executar o Projeto Localmente

1. Clona o repositório:
   ```bash
   git clone [https://github.com/guimaraujo23/Restaurante.git](https://github.com/guimaraujo23/Restaurante.git)

   
