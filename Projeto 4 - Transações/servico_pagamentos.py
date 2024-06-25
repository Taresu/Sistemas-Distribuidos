import json

import pika


class ServicoPagamentos:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_pagamentos')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_pagamentos', on_message_callback=self.tratar_evento_pagamento, auto_ack=True)
        self.canal.start_consuming()

    def tratar_evento_pagamento(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de pagamento recebido", pedido)
        # Lógica de processamento de pagamento aqui

# Executar serviço de pagamentos
servico_pagamentos = ServicoPagamentos()
servico_pagamentos.ouvir_eventos()