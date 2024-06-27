import sqlite3
from sistema_estoque import SistemaEstoque
from sistema_pedido import SistemaPedido

class SistemaComercioMonolitico:
    def __init__(self, caminho_bd):
        self.conn = sqlite3.connect(caminho_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
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

    def realizar_pedido(self, nome_produto, quantidade, dinheiro, pedido ,estoque):
        try:
            # self.iniciar_transacao()
            id_pedido = self.criar_pedido()
            estoque.reservar_estoque(nome_produto, quantidade)
            estoque.atualizar_estoque()
            self.processar_pagamento(nome_produto, id_pedido)
            self.enviar_pedido(id_pedido)
            # self.confirmar_transacao()
            print("Pedido realizado com sucesso")
        except Exception as e:
            self.desfazer_transacao()
            print(f"Falha ao realizar pedido: {e}")

    def processar_pagamento(self, nome_produto, id_pedido):
        self.cursor.execute("SELECT quantidade FROM estoque WHERE nome_produto = ?", (nome_produto,))
        valor = self.cursor.fetchone()
        if valor is None:
            raise Exception("Valor não está cadastrado")
        self.cursor.execute("INSERT INTO pagamentos (id_pedido, valor) VALUES (?, ?)", (id_pedido, valor[0]))

    def enviar_pedido(self, id_pedido):
        self.cursor.execute("INSERT INTO envio (id_pedido, status) VALUES (?, 'enviado')", (id_pedido,))



# Uso
caminho_bd = 'comercio_monolitico.db'
sistema = SistemaComercioMonolitico(caminho_bd)
pedido = SistemaPedido(caminho_bd)
estoque = SistemaEstoque(caminho_bd)
while(True):
    estoque.imprimir_produtos()
    produto_desejado = input("Digite o produto desejado: ")
    quantidade_desejada = input("Digite a quantidade desejada: ")
    dinheiro = input("Digite quanto dinheiro tem disponível")
    sistema.realizar_pedido(produto_desejado, quantidade_desejada, dinheiro, estoque)