import sqlite3
from sistema_estoque import SistemaEstoque
from sistema_pedido import SistemaPedido
from sistema_pagamento import SistemaPagamento
from sistema_envio import Sistemaenvio

class SistemaComercioMonolitico:
    def realizar_pedido(self, nome_produto, quantidade, dinheiro, pedido, estoque, pagamento, envio):
        try:
            # self.iniciar_transacao()
            id_pedido = pedido.criar_pedido()
            flag_estoque, valorInd = estoque.reservar_estoque(nome_produto, quantidade)
            flag_pagamento = pagamento.verificar_dindin(quantidade, dinheiro, valorInd, id_pedido)
            flag_envio = envio.registrar_id(id_pedido)
            if id_pedido == 0 or (not flag_estoque) or (not flag_pagamento) or (not flag_envio):
                pedido.rollback_pedido()
                estoque.rollback_estoque()
                pagamento.rollback_pagamento()
                envio.rollback_envio()
                print("Falha ao realizar pedido")
            pedido.commit_pedido()
            estoque.atualizar_estoque()
            pagamento.processar_pagamento()
            envio.enviar_pedido()
            print("Pedido realizado com sucesso")
        except Exception as e:
            print(f"Falha ao realizar pedido: {e}")

# Uso
sistema = SistemaComercioMonolitico()
caminho_bd = 'comercio_monolitico.db'
pedido = SistemaPedido(caminho_bd)
estoque = SistemaEstoque(caminho_bd)
pagamento = SistemaPagamento(caminho_bd)
envio = Sistemaenvio(caminho_bd)
while(True):
    estoque.imprimir_produtos()
    produto_desejado = input("Digite o produto desejado: ")
    quantidade_desejada = input("Digite a quantidade desejada: ")
    dinheiro = input("Digite quanto dinheiro tem disponível: ")
    sistema.realizar_pedido(produto_desejado, quantidade_desejada, dinheiro, pedido, estoque, pagamento, envio)