import random
import numpy as np
import math
from job import Job

class Dispatcher:
    def __init__(self, env, serverList, name):
        self.name = name
        self.env = env
        self.serverList = serverList

    def dispatchRandom(self, job):
        chosen = random.choice(self.serverList)
        chosen.submitJob(job)

    def JSQ(self, job):
        # iterate over all the servers
        minQueueLength = float('inf')
        bestServer = None

        for server in self.serverList:
            if len(server.queue.items) < minQueueLength:
                minQueueLength = len(server.queue.items)
                bestServer = server
        
        bestServer.submitJob(job)

    def JIQ(self, job):
        bestServer = None
        for server in self.serverList:
            if len(server.queue.items) == 0:
                bestServer = server
        
        if bestServer is None:
            self.JSQ(job)
        else:
            bestServer.submitJob(job)

    def JSQd(self, d, job):
        if d > len(self.serverList):
            raise Exception("cant select a subset that is larger than the main set")
        
        subsetServers = random.sample(self.serverList, d)
        minQueueLength = float('inf')
        bestServer = None

        for server in subsetServers:
            if len(server.queue.items) < minQueueLength:
                minQueueLength = len(server.queue.items)
                bestServer = server
        
        bestServer.submitJob(job)
                
    
    def run(self):
        count = 0
        while 1:
            count += 1
            job = Job(self.env, str(count))
            print(f"job {count} was sent from {self.name}")
            self.dispatchRandom(job)
            interval = math.floor(np.random.normal(10, 1))
            yield self.env.timeout(interval)
