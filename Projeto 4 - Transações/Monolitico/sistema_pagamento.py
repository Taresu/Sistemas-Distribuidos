import sqlite3

class SistemaPagamento():
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.id_pedido_atual = None
        self.custo = None
        
    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pagamentos (
                        id INTEGER PRIMARY KEY,
                        id_pedido INTEGER,
                        valor REAL)''')
        self.conn.commit()
    
    def verificar_dindin(self, quantidade, dinheiro_cliente, valor, id_pedido):
        self.custo = valor * int(quantidade)
        if self.custo > int(dinheiro_cliente):
            print ("Dinheiro Insuficiente")
            return False
        self.id_pedido_atual = id_pedido
        return True
        
    def processar_pagamento(self):
        self.conn.execute('BEGIN')
        self.cursor.execute("INSERT INTO pagamentos (id_pedido, valor) VALUES (?, ?)", (self.id_pedido_atual, self.custo))
        self.conn.commit()
        
    def rollback_pagamento(self):
        self.id_pedido_atual = None
        self.custo = None