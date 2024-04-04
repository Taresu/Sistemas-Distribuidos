import pika
import sys

conexao = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

canal = conexao.channel()

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())
    
def criacaoCardapio():
    canal.exchange_declare(exchange=nomeRest, exchange_type='fanout')
    message = "Bem vindo ao cardapio do " + nomeRest + "!"
    canal.basic_publish(exchange=nomeRest, routing_key=nomeRest, body=message)
    print(f" [x] Sent {message}")

    nomeQueue = "Restaurante " + nomeRest
    canal.queue_declare(queue=nomeQueue)
    canal.queue_bind(exchange=nomeRest, queue=nomeQueue)
    
def entrarEmQueue(nomefila):
    canal.basic_consume(queue=nomefila, on_message_callback=callback, auto_ack=True)
    canal.start_consuming()

def criacaoPrato(nomePrato, preco):
    mensagem = nomePrato + ": R$ " + preco
    canal.basic_publish(exchange= nomeRest, routing_key=nomeRest, body=mensagem)


#######################################################################################
nomeRest = input("Digite o Nome do Restaurante: ")
criacaoCardapio()

opcao = 0
while opcao == 0:
    opcao = input("Digite 1 para enviar novo prato "+"Digite 2 para entrar em uma fila: ")
    opcao = int(opcao)
    if opcao == 1:
        prato = input("Digite o Nome do Prato: ")
        if prato == "fechar":
            canal.close()
            exit
        preco = input("Digite o Preço: ")
        if preco == "fechar":
            canal.close()
            exit
        criacaoPrato(prato, preco)
        opcao = 0
    if opcao == 2:
        novaqueue = input("Digite o nome da nova fila: ")
        entrarEmQueue(novaqueue)
        opcao = 0
