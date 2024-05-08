import random
<<<<<<< HEAD
import sys
import time

import Pyro5.api
=======
from threading import Thread
>>>>>>> refs/remotes/origin/main

FOLLOWER = 1
CANDIDATE = 2
LEADER = 3
<<<<<<< HEAD
PORTA_NODE1 = 40988

OBJECTID = "ObjetoNode2"
NODE1 = "PYRO:ObjetoNode1@localhost:" + str(PORTA_NODE1)

@Pyro5.api.expose
class MyPyro(object):
    def vote():
        return 1
    pass 
=======
PORTA = 40984

OBJECTID = "ObjetoNode2"
NODE1 = "PYRO:ObjetoNode1@localhost:40983"
RANDMIN = 10
RAMDMAX = 10
>>>>>>> refs/remotes/origin/main

class Node(object):
    @Pyro5.api.expose    
    class MyPyro(object):
        def vote(x):
            if node.votou:
                return 0
            else:
                node.votou = True
                return 1
        pass 
    
    class ThreadReqLoop(Thread):
        def __init__ (self, daemon): 
            Thread.__init__(self)
            self.daemon = daemon 
        def run(self):
            self.daemon.requestLoop()  
    
    def __init__(self, object):
        #status: Candidate, Leader, Follower
<<<<<<< HEAD
        daemon = Pyro5.server.Daemon(port = PORTA_NODE1)
        self.uriObject = daemon.register(MyPyro, object)
=======
        self.daemon = Pyro5.server.Daemon(port = PORTA)
        self.uriObject = self.daemon.register(self.MyPyro, object)
>>>>>>> refs/remotes/origin/main
        print(self.uriObject)
        self.status = FOLLOWER
        self.votou = False        
        
    
        
    def requestVote(self, uri):
        #Pede voto diretamente com URI pelo proxy
        objectDest = Pyro5.api.Proxy(uri)
        print(objectDest)
        return objectDest.vote()
            
    def election(self):
        if self.status == FOLLOWER:
            threadLoop = self.ThreadReqLoop(self.daemon)
            threadLoop.start()
            randTime = random.randint(RANDMIN, RAMDMAX)  
            print(str(randTime) + "segundos Sleeping...") 
            time.sleep(randTime)
            if (self.votou):
                self.votou = False
            else:
                self.status = CANDIDATE 
                
        elif self.status == CANDIDATE:
            votes = 0
            votes = votes + self.requestVote(NODE1)
            print("Quantidade de votos:" + votes)
            if (votes == 1):
                self.status = LEADER
        else:
            servidor_nomes = Pyro5.core.locate_ns(port=40982)
            print("node1 lider")
            servidor_nomes.register("Leader", self.uriObject)

<<<<<<< HEAD
node = Node(OBJECTID)
=======
node = Node(OBJECTID)         
while(True):
    node.election()   
>>>>>>> refs/remotes/origin/main
# def main(objectId):
#     server = Pyro5.server.Daemon(PORTA)
#     uriObject = server.register(MyPyro, objectId)
#     print(uriObject)
#     server.requestLoop()


# if __name__ == "__main__":
#     port, objectId = sys.argv[1]
#     main(objectId)

