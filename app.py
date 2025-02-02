from flask import Flask, request, send_from_directory, jsonify
import os
from database import salvar_token

app = Flask(__name__)

# Rota para exibir a página de callback
@app.route('/trello-callback')
def trello_callback_page():
    return send_from_directory(os.getcwd(), 'callback.html')

# Rota para receber o token via POST do callback.html
@app.route('/trello-callback', methods=['POST'])
def trello_callback():
    data = request.get_json()
    token = data.get('token')
    user_id = data.get('state')

    if not user_id or not token:
        return jsonify({"error": "Parâmetros inválidos."}), 400

    # Salva o token no banco de dados
    salvar_token(user_id, token)

    return jsonify({"message": "Conta do Trello conectada com sucesso!"})

if __name__ == '__main__':
    app.run(port=5000)