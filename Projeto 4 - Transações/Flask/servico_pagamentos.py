from flask import Flask, jsonify, request

app = Flask(__name__)
pagamentos = {}

@app.route('/pagamento', methods=['POST'])
def processar_pagamento():
    dados = request.json
    id_pedido = dados['id_pedido']
    valor = dados['valor']
    pagamentos[id_pedido] = valor
    print(f"Pagamento processado para o pedido: {id_pedido}, valor: {valor}")
    return '', 200

@app.route('/rollback_pagamento', methods=['POST'])
def rollback_pagamento():
    dados = request.json
    id_pedido = dados.get('id_pedido')
    if id_pedido in pagamentos:
        del pagamentos[id_pedido]
        print(f"Rollback realizado para o pagamento do pedido: {id_pedido}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5003)