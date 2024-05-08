import random
import threading
import time

import Pyro5.api


# Classe para criar o servidor
class ServidorRaft:
    def __init__(self, id, porta):
        #status: CANDIDATO, LÍDER, SEGUIDOR
        self.id = id
        self.id_lider = None
        self.log = []
        self.indice_commitado = 0
        self.ultimo_aplicado = 0
        self.papel = "SEGUIDOR"
        self.tempo_limite_eleicao = random.randint(150, 300) / 1000  # timeout entre 150ms e 300ms
        self.intervalo_heartbeat = 0.1  # intervalo de envio de heartbeat
        self.conexoes = []
        
        # Inicializa o servidor Pyro
        self.daemon = Pyro5.server.Daemon(port=porta)
        self.uri = self.daemon.register(self)
        self.ns = Pyro5.api.locate_ns()
        self.ns.register(f"raft.servidor.{self.id}", self.uri)

        # Cria os temporizadores
        self.temporizador_eleicao = threading.Timer(self.tempo_limite_eleicao, self.iniciar_eleicao)
        self.temporizador_lider = threading.Timer(self.intervalo_heartbeat, self.enviar_heartbeat)

    def iniciar_eleicao(self):
        if self.papel == "SEGUIDOR":
            print(f"Processo {self.id} está iniciando eleição.")
            self.papel = "CANDIDATO"
            self.id_lider = None
            # Inicia a votação
            votos = 1  # O próprio servidor vota em si mesmo
            for servidor in self.conexoes:
                try:
                    if servidor.votar():
                        votos += 1
                except Pyro5.errors.CommunicationError:
                    pass  # Ignora erros de comunicação
            if votos > len(self.conexoes) / 2:  # Verifica se recebeu maioria dos votos
                self.tornar_lider()
            else:
                self.papel = "SEGUIDOR"
                self.temporizador_eleicao = threading.Timer(self.tempo_limite_eleicao, self.iniciar_eleicao)
                self.temporizador_eleicao.start()

    def votar(self):
        return self.papel == "SEGUIDOR"  # Um SEGUIDOR vota em um CANDIDATO

    def tornar_lider(self):
        print(f"Processo {self.id} se tornou líder.")
        self.papel = "LÍDER"
        self.id_lider = self.id
        for servidor in self.conexoes:
            servidor.definir_lider(self.id)

        # Envie os comandos do log para os seguidores
        for seguidor in self.conexoes:
            seguidor.replicar_log(self.log)

    def definir_lider(self, id_lider):
        self.id_lider = id_lider
        if self.papel == "CANDIDATO":
            self.temporizador_eleicao.cancel()
            self.papel = "SEGUIDOR"

    def enviar_heartbeat(self):
        if self.papel == "LÍDER":
            print(f"Processo {self.id} está enviando heartbeat.")
            for servidor in self.conexoes:
                try:
                    servidor.heartbeat(self.id_lider)
                except Pyro5.errors.CommunicationError:
                    pass  # Ignora erros de comunicação
            self.temporizador_lider = threading.Timer(self.intervalo_heartbeat, self.enviar_heartbeat)
            self.temporizador_lider.start()

    def replicar_log(self, log):
        # Verifique se o líder ainda está ativo
        if self.papel == "LÍDER":
            # Adicione o log recebido ao próprio log
            self.log.extend(log)
            print(f"[Processo {self.id}] recebeu log para replicar.")
            time.sleep(1)  # Adiciona um atraso na exibição para maior clareza
            print(f"[Processo {self.id}] Log replicado: {log}")

# Função para inicializar os servidores
def inicializar_servidores():
    servidores = []
    portas = [40020, 40021, 40032, 40043]  # Portas diferentes para cada servidor
    for i, porta in enumerate(portas):
        servidor = ServidorRaft(i, porta)
        servidores.append(servidor)
    return servidores

if __name__ == "__main__":
    # Inicialize o servidor de nomes Pyro
    Pyro5.api.locate_ns()
    
    # Inicialize os servidores
    servidores = inicializar_servidores()

    # Inicie os temporizadores
    for servidor in servidores:
        servidor.temporizador_eleicao.start()
        servidor.temporizador_lider.start()
    
    # Aguarde para sempre
    threading.Event().wait()
