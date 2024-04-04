import pika

conexao = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

canal = conexao.channel()

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())
    
def criacaoPromocoes():
    canal.exchange_declare(exchange=nomeMercado, exchange_type='fanout')
    message = "Bem vindo as promoções do " + nomeMercado + "!"
    canal.basic_publish(exchange=nomeMercado, routing_key=nomeMercado, body=message)
    print(f" [x] Sent {message}")

    nomeQueue = "Mercado " + nomeMercado
    canal.queue_declare(queue=nomeQueue)
    canal.queue_bind(exchange=nomeMercado, queue=nomeQueue)
    

def criaPromo(nomePrato, preco):
    mensagem = nomePrato + ": R$ " + preco
    canal.basic_publish(exchange= nomeMercado, routing_key=nomeMercado, body=mensagem)    
############################################################ 

nomeMercado = input("Digite o Nome do Restaurante: ")
criacaoPromocoes()

while True:    
    produto = input("Digite o Nome do Produto: ")
    if produto == "fechar":
        canal.close()
        exit()
    preco = input("Digite o Preço: ")
    if preco == "fechar":
        canal.close()
        exit()   
    criaPromo(produto, preco)

