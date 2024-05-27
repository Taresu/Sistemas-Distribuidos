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
PORTA_NODE2 = 40987

OBJECTID = "ObjetoNode1"
<<<<<<< HEAD
NODE2 = "PYRO:ObjetoNode2@localhost:" + str(PORTA_NODE2)

@Pyro5.api.expose
class MyPyro(object):
    def vote(x):
        return 1
    pass
=======
NODE2 = "PYRO:ObjetoNode2@localhost:40984"
RANDMIN = 3
RAMDMAX = 3
>>>>>>> refs/remotes/origin/main

class Node(object):
    @Pyro5.api.expose    
    class MyPyro(object):
        def vote(self):
            if self.votou:
                return 0
            else:
                self.votou = True
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
        daemon = Pyro5.server.Daemon(port = PORTA_NODE2)
        self.uriObject = daemon.register(MyPyro, object)
=======
        self.daemon = Pyro5.server.Daemon(port = PORTA)
        self.uriObject = self.daemon.register(self.MyPyro, object)
>>>>>>> refs/remotes/origin/main
        print(self.uriObject)
        self.status = FOLLOWER
        self.votou = False
            # daemon.requestLoop()
        
    def requestVote(self, uri):
        #Pede voto diretamente com URI pelo proxy
        objectDest = Pyro5.api.Proxy(uri)
        print(objectDest)
        return objectDest.vote()
    pass
            
    def election(self):
        if self.status == FOLLOWER:
            randTime = random.randint(5, 10)
            print(str(randTime) + "segundos Sleeping...")
            threadLoop = self.ThreadReqLoop(self.daemon)
            threadLoop.start()
            randTime = random.randint(RANDMIN, RAMDMAX)  
            print(str(randTime) + "segundos Sleeping...") 
            time.sleep(randTime)
            # threadLoop.join()
            if (self.votou == False):
                self.status = CANDIDATE  
                
        elif self.status == CANDIDATE:
            votes = 0
            votes = votes + self.requestVote(NODE2)
            print("Quantidade de votos:" + str(votes))
            if (votes == 1):
                self.status = LEADER
        else:
            servidor_nomes = Pyro5.core.locate_ns(port=40982)
            print("node1 lider")
<<<<<<< HEAD
            servidor_nomes.register("Leader", self.uriObject)
=======
            servidor_nomes.register("Leader", self.uriObject)      
>>>>>>> refs/remotes/origin/main
            
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