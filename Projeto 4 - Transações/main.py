import sqlite3


class SistemaComercioMonolitico:
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                                id INTEGER PRIMARY KEY,
                                status TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                                id INTEGER PRIMARY KEY,
                                nome_produto TEXT,
                                quantidade INTEGER)''')
        produtos = [
            ('Samsung S3000', 50),
            ('iPhone 79', 30),
            ('Xiaomi SuperMegaBlaster', 25),
            ('Positivo One', 20),
            ('Nokia Brick Xtreme', 10)
        ]

        # Inserir os produtos na tabela estoque
        self.cursor.executemany('INSERT INTO estoque (nome_produto, quantidade) VALUES (?, ?)', produtos)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pagamentos (
                                id INTEGER PRIMARY KEY,
                                id_pedido INTEGER,
                                valor REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS envio (
                                id INTEGER PRIMARY KEY,
                                id_pedido INTEGER,
                                status TEXT)''')
        self.conn.commit()

    def iniciar_transacao(self):
        self.conn.execute('BEGIN')

    def confirmar_transacao(self):
        self.conn.commit()

    def desfazer_transacao(self):
        self.conn.rollback()

    def realizar_pedido(self, nome_produto, quantidade, valor):
        try:
            self.iniciar_transacao()
            self.criar_pedido()
            self.atualizar_estoque(nome_produto, quantidade)
            self.processar_pagamento(valor)
            self.enviar_pedido()
            self.confirmar_transacao()
            print("Pedido realizado com sucesso")
        except Exception as e:
            self.desfazer_transacao()
            print(f"Falha ao realizar pedido: {e}")

    def criar_pedido(self):
        self.cursor.execute("INSERT INTO pedidos (status) VALUES ('criado')")
        self.id_pedido = self.cursor.lastrowid

    def atualizar_estoque(self, nome_produto, quantidade):
        self.cursor.execute("SELECT quantidade FROM estoque WHERE nome_produto = ?", (nome_produto,))
        resultado = self.cursor.fetchone()
        if resultado is None or resultado[0] < quantidade:
            raise Exception("Estoque insuficiente")
        nova_quantidade = resultado[0] - quantidade
        self.cursor.execute("UPDATE estoque SET quantidade = ? WHERE nome_produto = ?", (nova_quantidade, nome_produto))

    def processar_pagamento(self, valor):
        self.cursor.execute("INSERT INTO pagamentos (id_pedido, valor) VALUES (?, ?)", (self.id_pedido, valor))

    def enviar_pedido(self):
        self.cursor.execute("INSERT INTO envio (id_pedido, status) VALUES (?, 'enviado')", (self.id_pedido,))


# Uso
caminho_bd = 'comercio_monolitico.db'
sistema = SistemaComercioMonolitico(caminho_bd)
sistema.realizar_pedido('iPhone 79', 2, 100.0)