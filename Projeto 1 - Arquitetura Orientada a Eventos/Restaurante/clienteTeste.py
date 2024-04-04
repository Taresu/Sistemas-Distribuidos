import pika

# Estabelecer conexão com RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Criando um canal
canal = connection.channel()

# Declarando uma fila
canal.queue_declare(queue='pedidos')

# Função para enviar o pedido (publisher)
def enviar_pedido(nomePrato):
    canal.basic_publish(exchange='', routing_key='pedidos', body=pedido)
    print("Pedido enviado:", pedido)

def pedido():
    
enviar_pedido("Pizza")
enviar_pedido("Hambúrguer")
enviar_pedido("Sushi")

connection.close()