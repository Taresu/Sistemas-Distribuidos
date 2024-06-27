import time

import Pyro5.api


def encaminhar_comando(comando):
    ns = Pyro5.api.locate_ns(host='localhost', port=9090)
    
    try:
        uri = ns.lookup("servidorLider")
        lider = Pyro5.api.Proxy(uri)
        lider.registrar_comando(comando)
    except Exception as e:
        print(f"Não há líder para encaminhar o comando. ERRO: {e}")

if __name__ == "__main__":
        while True:
            comando = input("Digite um comando para enviar ao líder: ")
            lista_comando = []
            lista_comando.extend(comando)
            encaminhar_comando(lista_comando)
            time.sleep(1)