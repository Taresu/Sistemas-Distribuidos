import json

import pika


class ServicoEstoque:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_estoque')
        self.canal.queue_declare(queue='fila_pagamentos')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_estoque', on_message_callback=self.tratar_evento_estoque, auto_ack=True)
        print("Aguardando eventos de estoque...")
        self.canal.start_consuming()

    def tratar_evento_estoque(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de estoque recebido:", pedido)
        # Simulação da lógica de atualização de estoque
        print(f"Atualizando estoque para o produto: {pedido['nome_produto']}, quantidade: {pedido['quantidade']}")
        pedido['status'] = 'pagamento_processado'
        self.canal.basic_publish(exchange='', routing_key='fila_pagamentos', body=json.dumps(pedido))

# Executar serviço de estoque
if __name__ == '__main__':
    servico_estoque = ServicoEstoque()
    servico_estoque.ouvir_eventos()