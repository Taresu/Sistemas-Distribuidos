import Pyro5.api


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
    print(f"Cliente conectado ao servidor: {uri}")

    return servidor

if __name__ == "__main__":
    # Inicialize o cliente
    cliente = inicializar_cliente()

    if cliente:
        # Encaminhe um comando para o servidor
        comando = "Comando de teste"
        cliente.registrar_comando(comando)
