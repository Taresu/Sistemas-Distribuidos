import json

import pika


class ServicoEnvio:
    def __init__(self):
        self.conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='fila_envio')

    def ouvir_eventos(self):
        self.canal.basic_consume(queue='fila_envio', on_message_callback=self.tratar_evento_envio, auto_ack=True)
        print("Aguardando eventos de envio...")
        self.canal.start_consuming()

    def tratar_evento_envio(self, ch, method, properties, body):
        pedido = json.loads(body)
        print("Evento de envio recebido:", pedido)
        # Simulação da lógica de envio
        print(f"Enviando pedido para o produto: {pedido['nome_produto']}")
        print("Pedido processado e enviado com sucesso.")

# Executar serviço de envio
if __name__ == '__main__':
    servico_envio = ServicoEnvio()
    servico_envio.ouvir_eventos()