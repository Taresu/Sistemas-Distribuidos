import pika
import time
import threading

def enviar_pedido(pedido):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='pedidos')
    channel.basic_publish(exchange='', routing_key='pedidos', body=pedido)
    print("Pedido enviado:", pedido)
    connection.close()

def consumir_pedidos():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='pedidos')

    def callback(ch, method, properties, body):
        print("Pedido recebido:", body.decode())
        time.sleep(5)  # Simulando o tempo de preparo
        print("Pedido pronto")
        print("Pedido entregue:", body.decode())

    channel.basic_consume(queue='pedidos', on_message_callback=callback, auto_ack=True)
    print("Aguardando pedidos...")
    channel.start_consuming()
    connection.close()

# Enviando pedidos de dois produtores diferentes
enviar_pedido("Pizza")
enviar_pedido("Hambúrguer")

# Criando dois consumidores diferentes para processar os pedidos
threading.Thread(target=consumir_pedidos).start()
threading.Thread(target=consumir_pedidos).start()
