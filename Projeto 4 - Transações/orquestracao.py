import subprocess
import time


def iniciar_servico(nome_arquivo):
    return subprocess.Popen(['python', nome_arquivo])

# Iniciar todos os serviços
servico_pedidos = iniciar_servico('servico_pedidos.py')
time.sleep(1)  # Aguardar um pouco para garantir que o serviço de pedidos esteja pronto
servico_estoque = iniciar_servico('servico_estoque.py')
time.sleep(1)
servico_pagamentos = iniciar_servico('servico_pagamentos.py')
time.sleep(1)
servico_envio = iniciar_servico('servico_envio.py')

# Manter a orquestração ativa
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Parar todos os serviços ao receber uma interrupção (Ctrl+C)
    servico_pedidos.terminate()
    servico_estoque.terminate()
    servico_pagamentos.terminate()
    servico_envio.terminate()