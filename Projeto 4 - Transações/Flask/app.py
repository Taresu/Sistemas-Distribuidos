import json
import socket

from db import SistemaComercioEletronico as banco_comercio
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'segredo'

def chamar_servico(port, endpoint, dados):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        mensagem = f"POST {endpoint} {json.dumps(dados)}"
        s.sendall(mensagem.encode('utf-8'))
        response = s.recv(1024)
    return json.loads(response.decode('utf-8'))

def orquestrar_pedido(pedido):
    try:
        print("Chamando serviço de pedidos...")
        resposta_pedidos = chamar_servico(5001, '/pedido', pedido) 
        pedido['id_pedido'] = resposta_pedidos['id_pedido']

        print("Chamando serviço de estoque...")
        resposta_estoque = chamar_servico(5002, '/estoque', pedido) 

        print("Chamando serviço de pagamentos...")
        resposta_pagamento = chamar_servico(5003, '/pagamento', pedido) 

        print("Chamando serviço de envio...")
        resposta_envio = chamar_servico(5004, '/envio', pedido) 

        flash("Pedido processado com sucesso!")
    except Exception as e:
        flash(f"Erro durante o processamento do pedido: {e}")
        print("Iniciando rollback...")
        rollback(pedido)

def rollback(pedido):
    try:
        print("Revertendo envio...")
        chamar_servico(5004, '/rollback_envio', pedido)
    except Exception as e:
        print(f"Erro ao reverter envio: {e}")

    try:
        print("Revertendo pagamento...")
        chamar_servico(5003, '/rollback_pagamento', pedido)
    except Exception as e:
        print(f"Erro ao reverter pagamento: {e}")

    try:
        print("Revertendo estoque...")
        chamar_servico(5002, '/rollback_estoque', pedido)
    except Exception as e:
        print(f"Erro ao reverter estoque: {e}")

    try:
        print("Revertendo pedido...")
        chamar_servico(5001, '/rollback_pedido', pedido)
    except Exception as e:
        print(f"Erro ao reverter pedido: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar_pedido', methods=['POST'])
def processar_pedido():
    nome_produto = request.form['nome_produto']
    quantidade = int(request.form['quantidade'])
    valor = float(request.form['valor'])

    pedido = {
        'nome_produto': nome_produto,
        'quantidade': quantidade,
        'valor': valor
    }

    orquestrar_pedido(pedido)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000)
    banco_comercio.criar_tabelas()
