import requests
import os
from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')

class TrelloAPI:
    def __init__(self, token):
        self.token = token

    #QUADRO
    def create_board(self, name):
        url = "https://api.trello.com/1/boards/"
        params = {
            'name': name,
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.post(url, params=params)
        return response

    def list_boards(self):
        url = "https://api.trello.com/1/members/me/boards"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.get(url, params=params)
        return response

    def update_board(self, board_id, new_name):
        url = f"https://api.trello.com/1/boards/{board_id}"
        params = {
            'name': new_name,
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.put(url, params=params)
        return response

    def delete_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.delete(url, params=params)
        return response

    #LISTA
    def list_lists(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.get(url, params=params)
        return response

    def create_list(self, board_id, name):
        url = "https://api.trello.com/1/lists"
        params = {
            'name': name,
            'idBoard': board_id,
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.post(url, params=params)
        return response

    #TAREFAS
    def create_card(self, list_id, name):
        url = "https://api.trello.com/1/cards"
        params = {
            'name': name,
            'idList': list_id,
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.post(url, params=params)
        return response

    def list_cards_in_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.get(url, params=params)
        return response

    def list_cards_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.get(url, params=params)
        return response

    def update_card(self, card_id, name=None):
        url = f"https://api.trello.com/1/cards/{card_id}"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        if name:
            params['name'] = name
        response = requests.put(url, params=params)
        return response

    def delete_card(self, card_id):
        url = f"https://api.trello.com/1/cards/{card_id}"
        params = {
            'key': TRELLO_API_KEY,
            'token': self.token
        }
        response = requests.delete(url, params=params)
        return response
