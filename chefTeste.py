import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos')

def callback(ch, method, properties, body):
    print("Pedido recebido:", body.decode())
    time.sleep(5)  # Simulando o tempo de preparo
    print("Pedido pronto")

channel.basic_consume(queue='pedidos', on_message_callback=callback, auto_ack=True)

print("Aguardando pedidos...")
channel.start_consuming()