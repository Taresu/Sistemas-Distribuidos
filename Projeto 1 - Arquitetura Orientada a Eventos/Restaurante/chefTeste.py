import pika, time

# Estabelecer conexão com RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Criando um canal
canal = connection.channel()

# Declarando uma fila
canal.queue_declare(queue='pedidos')

# Define função de retorno (callback)
def callback(ch, method, properties, body):
    print("Pedido recebido:", body.decode())
    time.sleep(5)  # Simulando o tempo de preparo
    print("Pedido pronto")

canal.basic_consume(queue='pedidos', on_message_callback=callback, auto_ack=True)

print("Aguardando pedidos...")
canal.start_consuming()