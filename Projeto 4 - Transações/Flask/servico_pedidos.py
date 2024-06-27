import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)
pedidos = {}

@app.route('/pedido', methods=['POST'])
def criar_pedido():
    dados = request.json
    id_pedido = str(uuid.uuid4())
    pedidos[id_pedido] = dados
    print(f"Pedido criado: {id_pedido}")
    return jsonify({'id_pedido': id_pedido})

@app.route('/rollback_pedido', methods=['POST'])
def rollback_pedido():
    dados = request.json
    id_pedido = dados.get('id_pedido')
    if id_pedido in pedidos:
        del pedidos[id_pedido]
        print(f"Rollback realizado para o pedido: {id_pedido}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5001)