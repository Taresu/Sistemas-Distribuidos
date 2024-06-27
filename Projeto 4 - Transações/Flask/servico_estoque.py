import json
import socket

from db import SistemaComercioEletronico as banco_comercio


def atualizar_estoque(data):
    pedido = json.loads(data)
    produto = pedido['nome_produto']
    if produto in estoque:
        estoque[produto] -= pedido['quantidade']
    else:
        estoque[produto] = -pedido['quantidade']
    return json.dumps({'status': 'Estoque atualizado'})

def rollback_estoque(data):
    pedido = json.loads(data)
    produto = pedido['nome_produto']
    estoque[produto] += pedido['quantidade']
    return json.dumps({'status': 'Rolled back'})

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5002))
    server_socket.listen(5)
    print("Serviço de Estoque escutando na porta 5002...")
    
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("POST /estoque"):
            response = atualizar_estoque(data[len("POST /estoque "):])
        elif data.startswith("POST /rollback_estoque"):
            response = rollback_estoque(data[len("POST /rollback_estoque "):])
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    estoque = {}
    start_server()
