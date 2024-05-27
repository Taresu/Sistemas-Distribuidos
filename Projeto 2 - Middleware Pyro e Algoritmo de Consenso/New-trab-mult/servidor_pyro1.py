import random
import threading

import Pyro5.api


class ServidorRaft:
    def __init__(self, id, port):
        self.id = id
        self.status = "SEGUIDOR"
        self.termo_atual = 0
        self.votou_no_termo = None
        self.votos_recebidos = 0
        self.log = []
        self.conexoes = {}
        self.daemon = Pyro5.server.Daemon(port=port)
        self.uri = self.daemon.register(self)
        self.ns = Pyro5.api.locate_ns()
        self.ns.register(f"raft.servidor.{self.id}", self.uri)
        print(f"Servidor {self.id} iniciado na porta {port}.")
        threading.Thread(target=self.daemon.requestLoop).start()
        self.iniciar_eleicao()

    @Pyro5.api.expose
    def iniciar_eleicao(self):
        if self.status == "SEGUIDOR":
            self.status = "CANDIDATO"
            self.termo_atual += 1
            self.votou_no_termo = self.termo_atual
            self.votos_recebidos = 1
            print(f"Servidor {self.id} iniciou uma eleição no termo {self.termo_atual}.")
            for conexao in self.conexoes.values():
                threading.Thread(target=conexao.votar, args=(self.termo_atual,)).start()

    @Pyro5.api.expose
    def votar(self, termo):
        if termo >= self.termo_atual:
            self.status = "SEGUIDOR"
            self.termo_atual = termo
            self.votou_no_termo = None
            if hasattr(self, "temporizador_eleicao"):
                self.temporizador_eleicao.cancel()
            self.temporizador_eleicao = threading.Timer(self.tempo_limite_eleicao(), self.iniciar_eleicao)
            self.temporizador_eleicao.start()
            print(f"Servidor {self.id} votou no termo {termo}.")
            return True
        return False

    @Pyro5.api.expose
    def registrar_comando(self, comando):
        if self.status == "LÍDER":
            self.log.append(comando)
            for conexao in self.conexoes.values():
                threading.Thread(target=conexao.replicar_log, args=(self.termo_atual, self.log.copy())).start()
            print(f"Servidor {self.id} registrou um comando: {comando}")

    @Pyro5.api.expose
    def replicar_log(self, termo, log):
        if termo >= self.termo_atual:
            self.termo_atual = termo
            self.log = log
            print(f"Servidor {self.id} replicou o log do termo {termo}.")

    def tempo_limite_eleicao(self):
        return random.uniform(1, 2)

    def heartbeat(self):
        pass

if __name__ == "__main__":
    try:
        PORTA = 4246  # Defina a porta desejada
        servidor = ServidorRaft(1, PORTA)
        threading.Event().wait()
    except Exception as e:
        print(f"Erro: {e}")
