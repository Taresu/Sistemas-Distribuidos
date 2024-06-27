import sqlite3

class SistemaPedido():
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.id_pedido_atual = 0
        
    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                                id INTEGER PRIMARY KEY,
                                status TEXT)''')
        self.conn.commit()
        
    def criar_pedido(self):
        self.id_pedido_atual = self.id_pedido_atual + 1
        return self.id_pedido_atual
    
    def commit_pedido(self):
        self.conn.execute('BEGIN')
        self.cursor.execute("INSERT INTO pedidos (status) VALUES ('criado')")
        self.conn.commit()
        
    def rollback_pedido(self):
        self.id_pedido_atual = self.id_pedido_atual - 1