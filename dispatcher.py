import simpy, random
from job import Job

class Dispatcher:
    def __init__(self, env, serverList):
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
                
    
    def run(self, interval):
        count = 0
        while 1:
            count += 1
            job = Job(self.env, str(count))
            self.dispatchRandom(job)
            yield self.env.timeout(interval)
