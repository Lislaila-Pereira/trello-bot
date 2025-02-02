# Trello Bot 🤖

Bem-vindo ao **Trello Bot**, um bot para Telegram que permite gerenciar quadros, listas e tarefas no Trello diretamente pelo chat! Com ele, você pode criar, editar, listar e excluir quadros, listas e cards de forma simples e rápida.

Este trabalho foi desenvolvido para a disciplina de **Programação Web** na **UFLA** (Universidade Federal de Lavras).

---

## 📌 Ideia do Projeto

O Trello Bot foi criado para facilitar o gerenciamento de tarefas no Trello sem precisar sair do Telegram. Ele se conecta à API do Trello e permite que você execute ações como:

- Criar, editar e apagar quadros.
- Criar listas dentro de quadros.
- Criar, editar e apagar cards (tarefas) em listas.
- Listar quadros, listas e cards.

Tudo isso através de comandos simples no Telegram!

---

## 🛠 Tecnologias Usadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework para criar o servidor que lida com o callback do Trello.
- **python-telegram-bot**: Biblioteca para criar o bot do Telegram.
- **Trello API**: API do Trello para interagir com quadros, listas e cards.
- **SQLite3**: Banco de dados local para armazenar tokens de usuários.
- **Ngrok**: Ferramenta para expor o servidor local na internet.
- **dotenv**: Biblioteca para gerenciar variáveis de ambiente.

---

## 🔑 Como Configurar o Projeto

### 1. **Obtenha as Chaves e Tokens**

#### a) Trello

1. Crie uma conta no [Trello](https://trello.com/).
2. Acesse o [Trello Developer Portal](https://trello.com/power-ups/admin) para criar um **Power-Up**.
3. Gere uma **API Key** e um **Token** no Trello Developer Portal.

#### b) Telegram

1. Crie um bot no Telegram usando o [BotFather](https://core.telegram.org/bots#botfather).
2. Anote o **Token do Bot** fornecido pelo BotFather.

### 2. **Configure o `.env`**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```plaintext
TELEGRAM_TOKEN=seu_token_do_telegram
TRELLO_API_KEY=sua_chave_api_do_trello
TRELLO_API_TOKEN=seu_token_do_trello
```

### 3. **Use o Ngrok**

Como o Trello precisa de uma URL pública para enviar o token de autenticação, usamos o **Ngrok** para expor o servidor Flask local na internet.

1. Baixe e instale o [Ngrok](https://ngrok.com/).
2. Execute o Ngrok com o comando:

   ```bash
   ngrok http 5000
   ```

3. Anote a URL gerada pelo Ngrok (ex.: `https://1234.ngrok.io`).
4. Adicione essa URL ao **Power-Up** no Trello Developer Portal.

### 4. **Estrutura do Projeto**

- **`main.py`**: Ponto de entrada do bot do Telegram. Contém os comandos e a lógica principal.
- **`trello_api.py`**: Classe que encapsula as chamadas à API do Trello.
- **`database.py`**: Gerencia o banco de dados SQLite para armazenar tokens de usuários.
- **`app.py`**: Servidor Flask que lida com o callback do Trello.
- **`callback.html`**: Página HTML que processa o token de autenticação do Trello.
- **`.env`**: Armazena as variáveis de ambiente (tokens e chaves).

---

## 🗂 Estrutura do Código

### 1. **Banco de Dados (SQLite3)**

O SQLite3 é usado para armazenar os tokens de autenticação dos usuários. A tabela `usuarios` contém:

- `id`: ID único do usuário.
- `telegram_id`: ID do usuário no Telegram.
- `trello_token`: Token de autenticação do Trello.

### 2. **Flask e Callback**

O servidor Flask (`app.py`) expõe uma rota (`/trello-callback`) que recebe o token de autenticação do Trello após o usuário autorizar o acesso. Esse token é salvo no banco de dados.

### 3. **Bot do Telegram**

O bot (`main.py`) usa a biblioteca `python-telegram-bot` para processar comandos como:

- `/start`: Mensagem inicial.
- `/conectar`: Gera o link de autenticação do Trello.
- `/criar_quadro`, `/listar_quadros`, `/editar_quadro`, `/apagar_quadro`: Comandos para gerenciar quadros.
- `/criar_lista`, `/listar_listas`: Comandos para gerenciar listas.
- `/criar_card`, `/listar_cards_lista`, `/editar_card`, `/apagar_card`: Comandos para gerenciar cards.

### 4. **Trello API**

A classe `TrelloAPI` (`trello_api.py`) encapsula as chamadas à API do Trello, como:

- Criar, editar e apagar quadros.
- Criar listas e cards.
- Listar quadros, listas e cards.

---

## 🌐 Callback HTML

O arquivo `callback.html` é uma página simples que processa o token de autenticação do Trello e o envia para o servidor Flask. Ele é acessado após o usuário autorizar o acesso ao Trello.

---

## 🚀 Como Executar o Projeto

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute o servidor Flask:

   ```bash
   python app.py
   ```

3. Execute o bot do Telegram:

   ```bash
   python main.py
   ```

4. Use o Ngrok para expor o servidor Flask:

   ```bash
   ngrok http 5000
   ```

5. Conecte-se ao bot no Telegram e comece a usar os comandos!

---

## 📝 Comandos Disponíveis

### **Quadros**

- `/criar_quadro Nome do Quadro`
- `/listar_quadros`
- `/editar_quadro ID_DO_QUADRO Novo Nome`
- `/apagar_quadro ID_DO_QUADRO`

### **Listas**

- `/criar_lista ID_DO_QUADRO Nome da Lista`
- `/listar_listas ID_DO_QUADRO`

### **Cards (Tarefas)**

- `/criar_card ID_DA_LISTA Nome do Card`
- `/listar_cards_lista ID_DA_LISTA`
- `/editar_card ID_DO_CARD Novo Nome`
- `/apagar_card ID_DO_CARD`

### **Outros**

- `/conectar`
- `/ajuda`

---

## 📌 Dicas

- Use `/listar_quadros` para obter os IDs dos quadros.
- Use `/listar_listas ID_DO_QUADRO` para obter os IDs das listas.
- Use `/listar_cards_lista ID_DA_LISTA` para obter os IDs dos cards.

---

## 🚀 Melhorias Futuras

Para melhorar a usabilidade do bot, podemos implementar as seguintes funcionalidades:

1. **Menus Interativos**:

   - Criar menus de seleção para quadros, listas e cards, eliminando a necessidade de digitar IDs manualmente.
   - Exemplo: Ao usar `/listar_quadros`, o bot exibe uma lista de quadros com botões para selecionar um.

2. **Navegação por Etapas**:

   - Guiar o usuário passo a passo para criar quadros, listas e cards.
   - Exemplo: Ao usar `/criar_card`, o bot pergunta em qual lista o card deve ser criado e exibe opções.

3. **Feedback Visual**:

   - Usar emojis e formatação Markdown para tornar as mensagens mais atraentes e fáceis de ler.

4. **Hospedagem na Nuvem**:
   - Hospedar o bot em um serviço como Heroku ou AWS para garantir disponibilidade 24/7.
