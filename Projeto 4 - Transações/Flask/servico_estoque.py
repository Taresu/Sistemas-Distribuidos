from flask import Flask, jsonify, request

app = Flask(__name__)
estoque = {}

@app.route('/estoque', methods=['POST'])
def atualizar_estoque():
    dados = request.json
    produto = dados['nome_produto']
    quantidade = dados['quantidade']
    if produto not in estoque:
        estoque[produto] = 0
    estoque[produto] += quantidade
    print(f"Estoque atualizado para o produto: {produto}, quantidade: {quantidade}")
    return '', 200

@app.route('/rollback_estoque', methods=['POST'])
def rollback_estoque():
    dados = request.json
    produto = dados['nome_produto']
    quantidade = dados['quantidade']
    if produto in estoque:
        estoque[produto] -= quantidade
        if estoque[produto] <= 0:
            del estoque[produto]
        print(f"Rollback realizado para o estoque do produto: {produto}, quantidade: {quantidade}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5002)