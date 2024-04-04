import pika
import requests
import subprocess

conexao = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
canal = conexao.channel()

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())

filaConectada = input("Digite o Nome do Restaurante, que quer receber o cardapio:")

canal.queue_declare(queue=filaConectada)
canal.basic_consume(queue=filaConectada, on_message_callback=callback ,auto_ack=True)
print("Aguardando mensagens. Pressione Ctrl+C para sair.")

# Começar a consumir mensagens
canal.start_consuming()

# def listar_filas():
#     # Chamar o comando rabbitmqctl list_queues usando subprocess
#     resultado = subprocess.run(['rabbitmqctl', 'list_queues'], capture_output=True, text=True)

#     # Verificar se o comando foi bem-sucedido
#     if resultado.returncode == 0:
#         # Imprimir o resultado
#         print("Filas disponíveis:")
#         print(resultado.stdout)
#     else:
#         # Imprimir uma mensagem de erro se o comando falhou
#         print("Erro ao listar as filas:", resultado.stderr)

# # Chame a função para listar as filas
# listar_filas()



# def EntraFila():
    