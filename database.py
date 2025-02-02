import sqlite3

def criar_conexao():
    return sqlite3.connect('bot.db', check_same_thread=False)

def criar_tabelas():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE NOT NULL,
            trello_token TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_token(telegram_id, trello_token):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO usuarios (telegram_id, trello_token) VALUES (?, ?)', (telegram_id, trello_token))
    conn.commit()
    conn.close()

def buscar_token(telegram_id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT trello_token FROM usuarios WHERE telegram_id = ?', (telegram_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None