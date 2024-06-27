import requests


def chamar_servico(url, dados):
    response = requests.post(url, json=dados)
    if response.status_code != 200:
        raise Exception(f"Erro ao chamar serviço: {url}")
    return response.json()

def orquestrar_pedido(pedido):
    try:
        # Chama o serviço de pedidos
        print("Chamando serviço de pedidos...")
        resposta_pedidos = chamar_servico('http://localhost:5001/pedido', pedido)
        pedido['id_pedido'] = resposta_pedidos['id_pedido']

        # Chama o serviço de estoque
        print("Chamando serviço de estoque...")
        resposta_estoque = chamar_servico('http://localhost:5002/estoque', pedido)

        # Chama o serviço de pagamentos
        print("Chamando serviço de pagamentos...")
        resposta_pagamento = chamar_servico('http://localhost:5003/pagamento', pedido)

        # Chama o serviço de envio
        print("Chamando serviço de envio...")
        resposta_envio = chamar_servico('http://localhost:5004/envio', pedido)

        print("Pedido processado com sucesso!")
    except Exception as e:
        print(f"Erro durante o processamento do pedido: {e}")
        print("Iniciando rollback...")
        rollback(pedido)

def rollback(pedido):
    # Chama os serviços de rollback em ordem inversa
    try:
        print("Revertendo envio...")
        chamar_servico('http://localhost:5004/rollback_envio', pedido)
    except Exception as e:
        print(f"Erro ao reverter envio: {e}")

    try:
        print("Revertendo pagamento...")
        chamar_servico('http://localhost:5003/rollback_pagamento', pedido)
    except Exception as e:
        print(f"Erro ao reverter pagamento: {e}")

    try:
        print("Revertendo estoque...")
        chamar_servico('http://localhost:5002/rollback_estoque', pedido)
    except Exception as e:
        print(f"Erro ao reverter estoque: {e}")

    try:
        print("Revertendo pedido...")
        chamar_servico('http://localhost:5001/rollback_pedido', pedido)
    except Exception as e:
        print(f"Erro ao reverter pedido: {e}")

# Simulação de uma requisição de pedido
pedido = {
    'nome_produto': 'produto1',
    'quantidade': 2,
    'valor': 100.0
}

orquestrar_pedido(pedido)