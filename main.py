import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
from trello_api import TrelloAPI
from database import buscar_token, criar_tabelas

#CONFIGURAÇÕES
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
REDIRECT_URL = "seu_link_aqui/trello-callback" #trocar link

criar_tabelas()

async def verificar_autenticacao(user_id: str) -> bool:
    token = buscar_token(user_id)
    return token is not None

async def start(update: Update, context: CallbackContext):
    mensagem = (
        "🤖 *Bem-vindo ao Trello Bot!*\n\n"
        "Eu posso te ajudar a gerenciar seus quadros, listas e tarefas no Trello diretamente pelo Telegram.\n\n"
        "🔹 *Como começar?*\n"
        "1. Use `/conectar` para vincular sua conta do Trello.\n"
        "2. Use `/criar_quadro Nome do Quadro` para criar seu primeiro quadro.\n"
        "3. Use `/ajuda` para ver todos os comandos disponíveis.\n\n"
        "📌 *Dica*: Use `/ajuda` a qualquer momento para ver instruções detalhadas."
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown")

async def conectar(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    auth_url = (
        f"https://trello.com/1/authorize"
        f"?expiration=never&scope=read,write"
        f"&response_type=token&key={TRELLO_API_KEY}"
        f"&callback_method=fragment"
        f"&return_url={REDIRECT_URL}?state={user_id}"
    )
    await update.message.reply_text(f"Clique no link para conectar sua conta do Trello:\n{auth_url}")

#QUADRO
async def criar_quadro(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    # Verifica se o usuário está autenticado
    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    nome_projeto = ' '.join(context.args)
    if not nome_projeto:
        await update.message.reply_text("Por favor, forneça um nome para o quadro. Exemplo: /criar_quadro Meu Novo Projeto")
        return

    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.create_board(nome_projeto)

    if response.status_code == 200:
        await update.message.reply_text(f'Projeto "{nome_projeto}" criado com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao criar o projeto: {response.text}")

async def listar_quadros(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    # Verifica se o usuário está autenticado
    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.list_boards()

    if response.status_code == 200:
        boards = response.json()
        if boards:
            mensagem = "Seus quadros no Trello:\n"
            for board in boards:
                mensagem += f"- {board['name']} (ID: {board['id']})\n"
            await update.message.reply_text(mensagem)
        else:
            await update.message.reply_text("Você não tem quadros no Trello.")
    else:
        await update.message.reply_text(f"Erro ao listar quadros: {response.text}")

async def editar_quadro(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    # Verifica se o usuário está autenticado
    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Por favor, forneça o ID do quadro e o novo nome. Exemplo: /editar_quadro ID_DO_QUADRO Novo Nome")
        return

    board_id = context.args[0]
    new_name = ' '.join(context.args[1:])
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.update_board(board_id, new_name)

    if response.status_code == 200:
        await update.message.reply_text(f'Quadro atualizado com sucesso! Novo nome: "{new_name}"')
    else:
        await update.message.reply_text(f"Erro ao atualizar o quadro: {response.text}")

async def apagar_quadro(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if not context.args:
        await update.message.reply_text("Por favor, forneça o ID do quadro. Exemplo: /apagar_quadro ID_DO_QUADRO")
        return

    board_id = context.args[0]
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.delete_board(board_id)

    if response.status_code == 200:
        await update.message.reply_text(f'Quadro apagado com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao apagar o quadro: {response.text}")

#LISTAS
async def listar_listas(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if not context.args:
        await update.message.reply_text("Por favor, forneça o ID do quadro. Exemplo: /listar_listas ID_DO_QUADRO")
        return

    board_id = context.args[0]
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.list_lists(board_id)

    if response.status_code == 200:
        lists = response.json()
        if lists:
            mensagem = "Listas no quadro:\n"
            for list in lists:
                mensagem += f"- {list['name']} (ID: {list['id']})\n"
            await update.message.reply_text(mensagem)
        else:
            await update.message.reply_text("Este quadro não tem listas.")
    else:
        await update.message.reply_text(f"Erro ao listar listas: {response.text}")

async def criar_lista(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Por favor, forneça o ID do quadro e o nome da lista. Exemplo: /criar_lista ID_DO_QUADRO Nome da Lista")
        return

    board_id = context.args[0]
    nome_lista = ' '.join(context.args[1:])

    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.create_list(board_id, nome_lista)

    if response.status_code == 200:
        await update.message.reply_text(f'Lista "{nome_lista}" criada com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao criar a lista: {response.text}")

async def listar_cards_lista(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if not context.args:
        await update.message.reply_text("Por favor, forneça o ID da lista. Exemplo: /listar_cards_em_lista ID_DA_LISTA")
        return

    list_id = context.args[0]
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.list_cards_in_list(list_id)

    if response.status_code == 200:
        cards = response.json()
        if cards:
            mensagem = "Cards na lista:\n"
            for card in cards:
                mensagem += f"- {card['name']} (ID: {card['id']})\n"
            await update.message.reply_text(mensagem)
        else:
            await update.message.reply_text("Esta lista não tem cards.")
    else:
        await update.message.reply_text(f"Erro ao listar cards: {response.text}")

async def listar_cards_quadro(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if not context.args:
        await update.message.reply_text("Por favor, forneça o ID do quadro. Exemplo: /listar_cards_em_quadro ID_DO_QUADRO")
        return

    board_id = context.args[0]
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.list_cards_board(board_id)

    if response.status_code == 200:
        cards = response.json()
        if cards:
            mensagem = "Cards no quadro:\n"
            for card in cards:
                mensagem += f"- {card['name']} (ID: {card['id']})\n"
            await update.message.reply_text(mensagem)
        else:
            await update.message.reply_text("Este quadro não tem cards.")
    else:
        await update.message.reply_text(f"Erro ao listar cards: {response.text}")


#TAREFAS
async def criar_card(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Por favor, forneça o ID da lista e o nome do card. Exemplo: /criar_card ID_DA_LISTA Nome do Card")
        return

    list_id = context.args[0]
    nome_card = ' '.join(context.args[1:])

    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.create_card(list_id, nome_card)

    if response.status_code == 200:
        await update.message.reply_text(f'Card "{nome_card}" criado com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao criar o card: {response.text}")

async def editar_card(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Por favor, forneça o ID do card e o novo nome. Exemplo: /editar_card ID_DO_CARD Novo Nome")
        return

    card_id = context.args[0]
    novo_nome = ' '.join(context.args[1:])

    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.update_card(card_id, novo_nome)

    if response.status_code == 200:
        await update.message.reply_text(f'Card atualizado com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao atualizar o card: {response.text}")

async def apagar_card(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    if not await verificar_autenticacao(user_id):
        await update.message.reply_text("Você precisa conectar sua conta do Trello primeiro. Use /conectar.")
        return

    if not context.args:
        await update.message.reply_text("Por favor, forneça o ID do card. Exemplo: /apagar_card ID_DO_CARD")
        return

    card_id = context.args[0]
    token = buscar_token(user_id)
    trello_api = TrelloAPI(token)
    response = trello_api.delete_card(card_id)

    if response.status_code == 200:
        await update.message.reply_text(f'Card apagado com sucesso!')
    else:
        await update.message.reply_text(f"Erro ao apagar o card: {response.text}")

#AJUDA
async def ajuda(update: Update, context: CallbackContext):
    mensagem = (
        "🤖 *Trello Bot - Ajuda*\n\n"
        "Aqui estão os comandos disponíveis:\n\n"
        "🔹 *Quadros*\n"
        "- `/criar_quadro Nome do Quadro`: Cria um novo quadro.\n"
        "- `/listar_quadros`: Lista todos os quadros.\n"
        "- `/editar_quadro ID_DO_QUADRO Novo Nome`: Edita o nome de um quadro.\n"
        "- `/apagar_quadro ID_DO_QUADRO`: Apaga um quadro.\n\n"
        "🔹 *Listas*\n"
        "- `/listar_listas ID_DO_QUADRO`: Lista todas as listas de um quadro.\n"
        "- `/criar_lista ID_DO_QUADRO Nome da Lista`: Cria uma nova lista em um quadro.\n\n"
        "🔹 *Cards (Tarefas)*\n"
        "- `/criar_card ID_DA_LISTA Nome do Card`: Cria um novo card em uma lista.\n"
        "- `/listar_cards_lista ID_DA_LISTA`: Lista todos os cards de uma lista.\n"
        "- `/listar_cards_quadro ID_DO_QUADRO`: Lista todos os cards de um quadro.\n"
        "- `/editar_card ID_DO_CARD Novo Nome`: Edita o nome de um card.\n"
        "- `/apagar_card ID_DO_CARD`: Apaga um card.\n\n"
        "🔹 *Outros*\n"
        "- `/conectar`: Conecta sua conta do Trello ao bot.\n"
        "- `/ajuda`: Exibe esta mensagem de ajuda.\n\n"
        "📌 *Dicas*\n"
        "- Use `/listar_quadros` para obter os IDs dos quadros.\n"
        "- Use `/listar_listas ID_DO_QUADRO` para obter os IDs das listas.\n"
        "- Use `/listar_cards_lista ID_DA_LISTA` para obter os IDs dos cards.\n"
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('conectar', conectar))
    application.add_handler(CommandHandler('criar_quadro', criar_quadro))
    application.add_handler(CommandHandler('editar_quadro', editar_quadro))
    application.add_handler(CommandHandler('apagar_quadro', apagar_quadro))
    application.add_handler(CommandHandler('listar_quadros', listar_quadros))
    application.add_handler(CommandHandler('listar_cards_quadro', listar_cards_quadro))
    application.add_handler(CommandHandler('listar_listas', listar_listas))
    application.add_handler(CommandHandler('criar_lista', criar_lista))
    application.add_handler(CommandHandler('criar_card', criar_card))
    application.add_handler(CommandHandler('listar_cards_lista', listar_cards_lista))
    application.add_handler(CommandHandler('editar_card', editar_card))
    application.add_handler(CommandHandler('apagar_card', apagar_card))
    application.add_handler(CommandHandler('ajuda', ajuda))

    application.run_polling()

if __name__ == '__main__':
    main()