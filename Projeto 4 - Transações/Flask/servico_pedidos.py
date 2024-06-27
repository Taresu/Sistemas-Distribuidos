import json
import socket

from db import SistemaComercioEletronico as banco_comercio


def criar_pedido(data):
    pedido = json.loads(data)
    pedido['id_pedido'] = len(pedidos) + 1
    pedidos.append(pedido)
    return json.dumps(pedido)

def rollback_pedido(data):
    pedido = json.loads(data)
    pedidos.remove(next(p for p in pedidos if p['id_pedido'] == pedido['id_pedido']))
    return json.dumps({'status': 'Rolled back'})

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(5)
    print("Serviço de Pedidos escutando na porta 5001...")
    
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("POST /pedido"):
            response = criar_pedido(data[len("POST /pedido "):])
        elif data.startswith("POST /rollback_pedido"):
            response = rollback_pedido(data[len("POST /rollback_pedido "):])
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    pedidos = []
    start_server()

