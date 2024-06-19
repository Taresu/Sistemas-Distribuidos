import random
import threading
from time import sleep

import Pyro5.api
import Pyro5.server
import Pyro5.core

@Pyro5.api.expose
class ServidorRaft:
    def __init__(self, id):
        self.id = id
        self.status = "SEGUIDOR"
        self.termo_atual = 0
        self.votou_no_serv = None
        self.votos_recebidos = 0
        self.conexoes = [f"PYRO:servidor{n}@localhost:500{n}" for n in range(1, 5) if n != id]
        self.losg = []
        self.tempo_eleicao = None
        self.ind_commit = 0
        self.commitado = False
        self.contador_confrimacao = 0
        self.uri = None
        self.ns = Pyro5.core.locate_ns(host='localhost', port=40982)

    def iniciar_servidor(self, uri, port):
        self.uri = uri
        self.ns.register(f"servidor{self.id}", self.uri)
        sleep(10)
        print(f"Servidor {self.id} iniciado na porta {port}.")
        self.eleicao_threads(False)

    def eleicao_threads(self, heartbeat):
        if self.tempo_eleicao:
            self.tempo_eleicao.cancel()
        timeout = random.uniform(10.0, 20.0)
        if heartbeat:
            pass
        else:
            print(f"SErvidor {self.id} Novo Timeout: {timeout} segundos")
        self.tempo_eleicao = threading.Timer(timeout, self.iniciar_eleicao)
        self.tempo_eleicao.start()

    def iniciar_eleicao(self):
        if self.status == "SEGUIDOR":
            self.status = "CANDIDATO"
            self.termo_atual += 1
            self.votou_no_serv = self.id
            self.votos_recebidos = 1
            print(f"Servidor {self.id} Virei Candidato! Termo: {self.termo_atual}.")
            print(f"Servidor {self.id} iniciou uma eleição! Termo {self.termo_atual}.")
            print(self.conexoes)
            for conexao in self.conexoes:
               # threading.Thread(target=self.pedir_voto(conexao), args=(conexao,)).start()
               self.pedir_voto(conexao)
                
        elif self.status == "CANDIDATO":
            self.status = "SEGUIDOR"
            self.votou_no_serv = None
            self.votos_recebidos = 0
            print(f"Servidor {self.id} falha na eleição! Termo {self.termo_atual}.")
            self.eleicao_threads(False)

    def virar_lider(self):
        if self.status == "CANDIDATO":
            self.status = "LIDER"
            self.lider = self.id
            self.votou_no_serv = None
            self.votos_recebidos = 0
            print(f"Servidor {self.id} virou lider! Termo: {self.termo_atual}.")
            #.enviar_heartbeat()
            threading.Timer(8, self.enviar_heartbeat).start()
            

    def enviar_heartbeat(self):
        for conexao in self.conexoes:
                try:
                    proxy = Pyro5.api.Proxy(conexao)
                    proxy._pyroTimeout = 8
                    proxy.eleicao_threads(True)
                except Exception as e:
                    print(f"Erro de envio de heartbeat: {e}.")
                    pass


    def receber_entradas_log(self, termo, id_lider, entrada_log, indice_commit):
        self.eleicao_threads(True)
        if indice_commit > self.ind_commit:
            self.ind_commit = indice_commit
            print(f"Servidor {self.id} comitou log com indice {indice_commit}!")
        if termo >= self.termo_atual:
            self.termo_atual = termo
            self.status = "SEGUIDOR"
            self.lider = id_lider
            self.votou_no_serv = None
            self.votos_recebidos = 0
            for log in entrada_log:
                if len(self.losg) < log['index'] or self.losg[log['index'] - 1]['term']:
                    self.losg = self.losg[:log['index'] - 1] + [log]
                    print(f"Servidor {self.id}: Atualizados logs! Índice {log['index']}! Termo: {log['term']}, comando: {log['command']}.")
            return True
        return False

    def pedir_voto(self, uri):
        try:
            proxy = Pyro5.api.Proxy(uri)
            proxy._pyroTimeout = 10
            print(f"Servidor {self.id} pediu voto para {uri}")
            votado = proxy.votar(self.termo_atual, self.id)
            if votado:
                print (f"Servidor {self.id} Voto recebido de {uri}")
                self.votos_recebidos = self.votos_recebidos + 1
                if self.votos_recebidos > len(self.conexoes) + 1 / 2 and self.status == "CANDIDATO":
                    self.virar_lider()
        except Exception as e:
            print(f"Servidor {self.id}] Erro no voto de {uri}: {e}")
            pass
        

    @Pyro5.api.expose
    def votar(self, termo, candidato):
        self.eleicao_threads(False)
        if termo > self.termo_atual:
            self.termo_atual = termo
            self.lider = None
            self.votou_no_serv = None
        if (self.votou_no_serv is None) or self.votou_no_serv == candidato:
            self.termo_atual = termo
            self.votou_no_serv = candidato
            print(f"Servidor {self.id} votou no {self.votou_no_serv}! Termo: {termo}.")
            return True
        return False



    @Pyro5.api.expose
    def registrar_comando(self, comando):
        if self.status == "LIDER":
            if comando:
                self.comitou = False
                comando[0]['term'] = self.termo_atual
                self.losg.extend(comando)
                self.contador_confrimacao = 1
                for conexao in self.conexoes.values():
                    threading.Thread(target=self.replicar_log, args=(self.losg, conexao)).start()
                print(f"Servidor {self.id} registrou um comando: {comando[0]['command']} ")

    @Pyro5.api.expose
    def replicar_log(self, log, conexao):
        try:
            proxy = Pyro5.api.Proxy(conexao)
            proxy._pyroTimeout = 10
            print(f"Servidor {self.id} Enviou log para {conexao}")
            confirmacao = proxy.append_entries(self.termo_atual, self.lider, log, self.ind_commit)
            if confirmacao:
                print(f"Servidor {self.id} Recebeu confirmacao de {conexao}")
                self.contador_confrimacao = self.contador_confrimacao + 1
                if self.contador_confrimacao > (((len(self.conexoes) + 1) / 2) and not self.comitou) :
                    self.ind_commit = log[len(log) - 1]['index']
                    print(f"Servidor {self.id} Log índice {self.ind_commit} comitado")
                    self.comitado = True
        except Exception as e:
            print(f"Servidor {self.id} Falha no envio dos logspara {conexao}")

    def tempo_limite_eleicao(self):
        return random.uniform(1, 2)

if __name__ == "__main__":
    try:
        PORTA = 5004  # Defina a porta desejada
        daemon = Pyro5.server.Daemon(host="localhost", port=PORTA)
        servidor = ServidorRaft(4)
        uri = daemon.register(servidor, objectId=f"servidor4")
        servidor.iniciar_servidor(uri, PORTA)
        daemon.requestLoop()
        # threading.Event().wait()
    except Exception as e:
        print(f"Erro: {e}")