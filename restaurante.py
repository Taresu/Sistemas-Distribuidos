import pika
import sys

#def main():
# def fechar_janela():
    #janela.destroy()
canal = None;
    
def criacaoCardapio():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    canal = connection.channel()

    canal.exchange_declare(exchange=nomeMercado, exchange_type='fanout')

    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    canal.basic_publish(exchange=nomeMercado, routing_key='', body=message)
    print(f" [x] Sent {message}")
    #connection.close()

def criacaoPrato(nomePrato, preco):
    mensagem = nomePrato + ": R$ " + preco
    canal.basic_publish(exchange=nomeMercado, routing_key='', body=nomePrato)


#######################################################################################
nomeMercado = input("Digite o Nome do Mercado: ")
criacaoCardapio()

while True:
    prato = input("Digite o Nome do Prato: ")
    if prato == "fechar":
        exit
    preco = input("Digite o Preço: ")
    if preco == "fechar":
        exit
    criacaoPrato(prato, preco)
    
