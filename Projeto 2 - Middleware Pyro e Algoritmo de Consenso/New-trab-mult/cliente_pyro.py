import time

import Pyro5.api


def encaminhar_comando(self, comando):
    ns = Pyro5.api.locate_ns(host='localhost', port=40982)
    
    try:
        uri = ns.lookup("servidorLider")
        lider = Pyro5.api.Proxy(uri)
        lider.registrar_comando(comando)
    except Exception as e:
        print(f"Não há líder para encaminhar o comando. ERRO: {e}")

if __name__ == "__main__":
    try:
        while True:
            comando = input("Digite um comando para enviar ao líder: ")
            encaminhar_comando(comando)
            time.sleep(1)
    except Exception as e:
        print(f"Erro: {e}")