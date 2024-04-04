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

opcao = input("Digite 1 para enviar cardapio ou 2 para receber promoções de mercado, ou 'fechar' para sair: ")

if opcao == '1':
    nomeRest = input("Digite o Nome do Restaurante: ")
    criacaoCardapio()
    while True:    
        prato = input("Digite o Nome do Prato: ")
        if prato == "fechar":
            canal.close()
            exit()
        preco = input("Digite o Preço: ")
        if preco == "fechar":
            canal.close()
            exit()   
        criacaoPrato(prato, preco)
elif opcao == '2':
        novaqueue = input("Digite o nome do mercado: ")
        entrarEmQueue(novaqueue)
else:
    canal.close()
    exit()
    
