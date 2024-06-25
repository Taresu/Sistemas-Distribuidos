import json

import pika


class ServicoPagamentos:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_pagamentos')
        self.canal.queue_declare(queue='fila_envio')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_pagamentos', on_message_callback=self.tratar_evento_pagamento, auto_ack=True)
        print("Aguardando eventos de pagamentos...")
        self.canal.start_consuming()

    def tratar_evento_pagamento(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de pagamento recebido:", pedido)
        # Simulação da lógica de processamento de pagamento
        print(f"Processando pagamento no valor de: {pedido['valor']}")
        pedido['status'] = 'pedido_enviado'
        self.canal.basic_publish(exchange='', routing_key='fila_envio', body=json.dumps(pedido))

# Executar serviço de pagamentos
if __name__ == '__main__':
    servico_pagamentos = ServicoPagamentos()
    servico_pagamentos.ouvir_eventos()