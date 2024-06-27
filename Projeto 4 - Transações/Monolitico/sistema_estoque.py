import sqlite3


class SistemaEstoque():
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.produto = None
        self.quantidadeTotal = None
        self.quantidadeReservada = None
    
    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                                id INTEGER PRIMARY KEY,
                                nome_produto TEXT,
                                quantidade INTEGER,
                                valor INTEGER)''')
        produtos = [
            ('Samsung S3000', 50, 10000),
            ('iPhone 79', 30, 10000),
            ('Xiaomi SuperMegaBlaster', 25, 7000),
            ('Positivo One', 20, 100),
            ('Nokia Brick Xtreme', 10, 1600)
        ]

        # Inserir os produtos na tabela estoque
        self.cursor.executemany('INSERT INTO estoque (nome_produto, quantidade, valor) VALUES (?, ?, ?)', produtos)
    
    def imprimir_produtos(self):
        self.cursor.execute("SELECT nome_produto, quantidade, valor FROM estoque")
        produtos = self.cursor.fetchall()
        print(f"Produto      |    Quantidade    |       Preço");
        for produto in produtos:
            print(f"{produto[0]}  |  {produto[1]}  |  R$ {produto[2]},00")
        
    def reservar_estoque(self, nome_produto, quantidade):
        self.cursor.execute("SELECT quantidade FROM estoque WHERE nome_produto = ?", (nome_produto,))
        resultado = self.cursor.fetchone()
        if resultado is None:
            print ("Produto Inexistente") 
            return False     
        self.quantidadeReservada = resultado[0]
        if self.quantidadeReservada < quantidade:
            print ("Estoque insuficiente")
            return False
        self.produto = nome_produto
        self.quantidade = quantidade
        return True
            
    def atualizar_estoque(self):
        self.quantidade = self.quantidade - self.quantidadeReservada
        self.cursor.execute("UPDATE estoque SET quantidade = ? WHERE nome_produto = ?", (self.quantidade, self.produto))
        