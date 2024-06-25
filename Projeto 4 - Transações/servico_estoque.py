import json

import pika


class ServicoEstoque:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_estoque')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_estoque', on_message_callback=self.tratar_evento_estoque, auto_ack=True)
        self.canal.start_consuming()

    def tratar_evento_estoque(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de estoque recebido", pedido)
        # Lógica de atualização de estoque aqui

# Executar serviço de estoque
servico_estoque = ServicoEstoque()
servico_estoque.ouvir_eventos()