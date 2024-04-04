import pika

conexao = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
canal = conexao.channel()

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())

def entrarEmQueue(fila):
    canal.queue_declare(queue=fila)
    canal.basic_consume(queue=fila, on_message_callback=callback ,auto_ack=True)

filaConectada = input("Digite o Nome do Restaurante, que quer receber o cardapio:")

entrarEmQueue(filaConectada)

# Começar a consumir mensagens
canal.start_consuming()

    