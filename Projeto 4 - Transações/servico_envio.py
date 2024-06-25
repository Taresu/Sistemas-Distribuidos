import json

import pika


class ServicoEnvio:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_envio')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_envio', on_message_callback=self.tratar_evento_envio, auto_ack=True)
        self.canal.start_consuming()

    def tratar_evento_envio(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de envio recebido", pedido)
        # Lógica de envio aqui

# Executar serviço de envio
servico_envio = ServicoEnvio()
servico_envio.ouvir_eventos()