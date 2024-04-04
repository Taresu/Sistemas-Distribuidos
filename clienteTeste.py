import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos')

def enviar_pedido(pedido):
    channel.basic_publish(exchange='', routing_key='pedidos', body=pedido)
    print("Pedido enviado:", pedido)

enviar_pedido("Pizza")
enviar_pedido("Hambúrguer")
enviar_pedido("Sushi")

connection.close()