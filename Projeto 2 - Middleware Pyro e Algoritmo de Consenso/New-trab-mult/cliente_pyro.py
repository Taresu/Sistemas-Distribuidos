import time

import Pyro5.api


class Cliente:
    def __init__(self):
        self.uri_lider = None
        self.ns = Pyro5.api.locate_ns()

    def encaminhar_comando(self, comando):
        if self.uri_lider:
            lider = Pyro5.api.Proxy(self.uri_lider)
            lider.registrar_comando(comando)
        else:
            print("Não há líder para encaminhar o comando.")

    def atualizar_lider(self):
        try:
            servidores_uris = self.ns.list(prefix="raft.servidor.")
            if servidores_uris:
                self.uri_lider = servidores_uris.popitem()[1]
            else:
                self.uri_lider = None
        except Exception as e:
            print(f"Erro ao atualizar líder: {e}")

if __name__ == "__main__":
    try:
        cliente = Cliente()
        while True:
            cliente.atualizar_lider()
            if cliente.uri_lider:
                comando = input("Digite um comando para enviar ao líder: ")
                cliente.encaminhar_comando(comando)
            else:
                print("Nenhum líder encontrado. Tentando novamente...")
            time.sleep(1)
    except Exception as e:
        print(f"Erro: {e}")