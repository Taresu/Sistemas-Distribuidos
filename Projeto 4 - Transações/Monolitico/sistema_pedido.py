import sqlite3

class SistemaEstoque():
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.id_pedido_atual = None
        
    def criar_tabelas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                                id INTEGER PRIMARY KEY,
                                status TEXT)''')
        
    def criar_pedido(self):
        self.cursor.execute("INSERT INTO pedidos (status) VALUES ('criado')")
        self.id_pedido_atual = self.cursor.lastrowid
        return self.id_pedido_atual