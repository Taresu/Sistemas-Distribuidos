import json
import socket

from db import SistemaComercioEletronico as banco_comercio


def processar_pagamento(data):
    pedido = json.loads(data)
    pagamentos.append(pedido)
    return json.dumps({'status': 'Pagamento processado'})

def rollback_pagamento(data):
    pedido = json.loads(data)
    pagamentos.remove(next(p for p in pagamentos if p['id_pedido'] == pedido['id_pedido']))
    return json.dumps({'status': 'Rolled back'})

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5003))
    server_socket.listen(5)
    print("Serviço de Pagamentos escutando na porta 5003...")
    
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("POST /pagamento"):
            response = processar_pagamento(data[len("POST /pagamento "):])
        elif data.startswith("POST /rollback_pagamento"):
            response = rollback_pagamento(data[len("POST /rollback_pagamento "):])
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    pagamentos = []
    start_server()
