import errno
import random
import threading
import time

import Pyro5.api

PORTA_INICIAL = 4002

class ServidorRaft3:
    def __init__(self, id, port):
        self.id = id
        self.status = "SEGUIDOR" # status: Seguidor, Líder, Candidato
        self.termo_atual = 0
        self.votou_no_termo = None
        self.votos_recebidos = 0
        self.log = []
        self.conexoes = {}
        self.daemon = None
        self.ns = Pyro5.api.locate_ns()
        self.inicializar_servidor(port)

    def inicializar_servidor(self, port):
        try:
            self.daemon = Pyro5.server.Daemon(port=port)
            self.uri = self.daemon.register(self)
            self.ns.register(f"raft.servidor.{self.id}", self.uri)
            print(f"Servidor {self.id} iniciado na porta {port}.")
        except OSError as e:
            if e.errno == errno.EADDRINUSE:  
                print(f"Porta {port} já está em uso. Tentando outra porta...")
                nova_porta = random.randint(4000, 4999)
                time.sleep(random.uniform(1, 3))
                self.inicializar_servidor(nova_porta)
            else:
                print("Não foi possível encontrar uma porta disponível após várias tentativas.")
                raise e
    
    def tempo_limite_eleicao(self):
        return random.uniform(1, 2)  

    def iniciar_eleicao(self):
        if self.status == "SEGUIDOR":
            self.status = "CANDIDATO"
            self.termo_atual += 1
            self.votou_no_termo = self.termo_atual
            self.votos_recebidos = 1  
            for conexao in self.conexoes.values():
                threading.Thread(target=conexao.votar, args=(self.termo_atual,)).start()  
            self.temporizador_eleicao = threading.Timer(self.tempo_limite_eleicao(), self.iniciar_eleicao)
            self.temporizador_eleicao.start()

    def votar(self, termo):
        if termo > self.termo_atual:
            self.status = "SEGUIDOR"
            self.termo_atual = termo
            self.votou_no_termo = None
            self.temporizador_eleicao.cancel()
            self.temporizador_eleicao = threading.Timer(self.tempo_limite_eleicao(), self.iniciar_eleicao)
            self.temporizador_eleicao.start()
            return True
        return False

    def registrar_comando(self, comando):
        if self.status == "LÍDER":
            self.log.append(comando)
            for conexao in self.conexoes.values():
                threading.Thread(target=conexao.replicar_log, args=(self.termo_atual, self.log)).start()  

    def replicar_log(self, termo, log):
        if termo >= self.termo_atual:
            self.termo_atual = termo
            self.log = log

    def heartbeat(self):
        pass

if __name__ == "__main__":
    # Inicialize o servidor de nomes Pyro
    Pyro5.api.locate_ns()

    # Inicialize a instância do servidor Raft
    instancia = ServidorRaft3(3, PORTA_INICIAL)

    # Estabeleça conexões entre os servidores
    servidores = [ServidorRaft3(i, PORTA_INICIAL + i) for i in range(1, 5)]
    for servidor in servidores:
        for outro_servidor in servidores:
            if outro_servidor != servidor:
                servidor.conexoes[outro_servidor.id] = Pyro5.api.Proxy(outro_servidor.uri)

    # Aguarde perpetuamente
    threading.Event().wait()
