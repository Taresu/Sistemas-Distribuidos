import json
import socket

from db import SistemaComercioEletronico as banco_comercio


def processar_envio(data):
    pedido = json.loads(data)
    envios.append(pedido)
    return json.dumps({'status': 'Envio processado'})

def rollback_envio(data):
    pedido = json.loads(data)
    envios.remove(next(e for e in envios if e['id_pedido'] == pedido['id_pedido']))
    return json.dumps({'status': 'Rolled back'})

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5004))
    server_socket.listen(5)
    print("Serviço de Envio escutando na porta 5004...")
    
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("POST /envio"):
            response = processar_envio(data[len("POST /envio "):])
        elif data.startswith("POST /rollback_envio"):
            response = rollback_envio(data[len("POST /rollback_envio "):])
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    envios = []
    start_server()
