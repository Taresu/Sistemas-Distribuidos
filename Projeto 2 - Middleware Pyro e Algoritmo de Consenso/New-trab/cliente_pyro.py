import time

import Pyro5.api


# Processo de Replicação: seguidores replicam o log recebido do líder.
def replicar_log(self, log):
# Verifique se o líder ainda está ativo
    if self.papel == "LÍDER":
        # Adicione o log recebido ao próprio log
        self.log.extend(log)
        print(f"[Processo {self.id}] recebeu log para replicar.")
        time.sleep(1)  # Adiciona um atraso na exibição para maior clareza
        print(f"[Processo {self.id}] Log replicado: {log}")

# Função para inicializar o cliente Pyro
def inicializar_cliente():
    # Encontre os servidores Pyro disponíveis
    ns = Pyro5.api.locate_ns()
    servidores_uris = ns.list(prefix="raft.servidor.")

    if not servidores_uris:
        print("Nenhum servidor disponível.")
        return None

    # Conecte-se a um servidor Pyro
    uri = servidores_uris.popitem()[1]
    servidor = Pyro5.api.Proxy(uri)
    #self = Pyro5.api.Proxy()
    print(f"Cliente conectado ao servidor: {uri}")
    print(servidor.replicar_log())

    return servidor

if __name__ == "__main__":
    # Inicialize o cliente
    cliente = inicializar_cliente()

    if cliente:
        # Encaminhe um comando para o servidor
        comando = "Comando de teste"
        cliente.registrar_comando(comando)

