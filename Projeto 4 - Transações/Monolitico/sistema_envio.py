import sqlite3

class Sistemaenvio():
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.id_pedido = None
            
    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS envio (
                                id INTEGER PRIMARY KEY,
                                id_pedido INTEGER,
                                status TEXT)''')
        self.conn.commit()
        
    def registrar_id(self, id):
        self.id_pedido = id
        return True
        
    def enviar_pedido(self):
        self.conn.execute('BEGIN')
        self.cursor.execute("INSERT INTO envio (id_pedido, status) VALUES (?, 'enviado')", (self.id_pedido,))
        self.conn.commit()
        
    def rollback_envio(self):
        self.id_pedido = None