from flask import Flask, jsonify, request

app = Flask(__name__)
envios = {}

@app.route('/envio', methods=['POST'])
def processar_envio():
    dados = request.json
    id_pedido = dados['id_pedido']
    envios[id_pedido] = dados
    print(f"Envio processado para o pedido: {id_pedido}")
    return '', 200

@app.route('/rollback_envio', methods=['POST'])
def rollback_envio():
    dados = request.json
    id_pedido = dados.get('id_pedido')
    if id_pedido in envios:
        del envios[id_pedido]
        print(f"Rollback realizado para o envio do pedido: {id_pedido}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5004)