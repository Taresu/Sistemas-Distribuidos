import json

import pika


class ServicoPedidos:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_pedidos')
        self.canal.queue_declare(queue='fila_estoque')
        self.canal.queue_declare(queue='fila_pagamentos')
        self.canal.queue_declare(queue='fila_envio')

    def realizar_pedido(self, nome_produto, quantidade, valor):
        pedido = {
            'nome_produto': nome_produto,
            'quantidade': quantidade,
            'valor': valor,
            'status': 'pedido_criado'
        }
        self.canal.basic_publish(exchange='', routing_key='fila_pedidos', body=json.dumps(pedido))
        print("Pedido realizado e enviado para processamento.")

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_pedidos', on_message_callback=self.tratar_evento_pedido, auto_ack=True)
        print("Aguardando eventos de pedidos...")
        self.canal.start_consuming()

    def tratar_evento_pedido(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de pedido recebido:", pedido)
        pedido['status'] = 'estoque_atualizado'
        self.canal.basic_publish(exchange='', routing_key='fila_estoque', body=json.dumps(pedido))

# Executar serviço de pedidos
if __name__ == '__main__':
    servico_pedidos = ServicoPedidos()
    servico_pedidos.realizar_pedido('produto1', 2, 100.0)
    servico_pedidos.ouvir_eventos()