import sys
import Pyro5.api
import time
import random

FOLLOWER = 1
CANDIDATE = 2
LEADER = 3
PORTA = 40984

OBJECTID = "ObjetoNode2"
NODE1 = "PYRO:ObjetoNode1@localhost:40983"

@Pyro5.api.expose    
class MyPyro(object):
    def vote(x):
        return 1
    pass 

class Node(object):
    def __init__(self, object):
        #status: Candidate, Leader, Follower
        self.daemon = Pyro5.server.Daemon(port = PORTA)
        self.uriObject = self.daemon.register(MyPyro, object)
        print(self.uriObject)
        self.status = FOLLOWER
        
        
    def requestVote(self, uri):
        #Pede voto diretamente com URI pelo proxy
        objectDest = Pyro5.api.Proxy(uri)
        print(objectDest)
        return objectDest.vote()
            
    def election(self):
        if self.status == FOLLOWER:
            randTime = random.randint(5, 10)  
            print(str(randTime) + " segundos Sleeping...") 
            time.sleep(randTime)
            noAns = False
            if (noAns):
                self.status = CANDIDATE
            else:
                self.daemon.requestLoop()
                
        elif self.status == CANDIDATE:
            votes = 0
            votes = votes + self.requestVote(NODE1)
            print("Quantidade de votos:" + votes)
            if (votes == 1):
                self.status = LEADER
        else:
            servidor_nomes = Pyro5.core.locate_ns()
            print("node1 lider")
            servidor_nomes.register("Leader", self.uriObject)

node = Node(OBJECTID)         
while(True):
    node.election()   
# def main(objectId):
#     server = Pyro5.server.Daemon(PORTA)
#     uriObject = server.register(MyPyro, objectId)
#     print(uriObject)
#     server.requestLoop()


# if __name__ == "__main__":
#     port, objectId = sys.argv[1]
#     main(objectId)

