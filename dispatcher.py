import random
import numpy as np
from job import Job

class Dispatcher:
    def __init__(self, env, queueHandler, name, op):
        self.name = name
        self.env = env
        self.queueHandler = queueHandler
        # define the dispatching algorithm to use
        self.op = op

    def dispatchRandom(self, job):
        chosen = random.choice(self.queueHandler.getQueueLengths())
        chosen[0].submitJob(job)

    def JSQ(self, job):
        bestServer = self.queueHandler.getMinQueueServer()
        bestServer.submitJob(job)

    def JIQ(self, job):
        bestServer = None
        for (server, length) in self.queueHandler.getQueueLengths():
            if length == 0:
                bestServer = server
        
        if bestServer is None:
            self.dispatchRandom(job)
        else:
            bestServer.submitJob(job)

    def JSQd(self, d, job):
        
        subsetServers = random.sample(self.queueHandler.getQueueLengths(), d)
        minQueueLength = float('inf')
        bestServer = None

        for (server, length) in subsetServers:
            if length < minQueueLength:
                minQueueLength = length
                bestServer = server
        
        bestServer.submitJob(job)

    def softminjsq(self, job):
        chosen = self.queueHandler.softmaxGetServer()
        chosen.submitJob(job)
    
    def softminjsqd(self, d, job):
        subsetServers = random.sample(self.queueHandler.getQueueLengths(), d)
        serverList = list(map(lambda x: x[0], subsetServers))
        total = np.sum(np.exp(list(map(lambda x: -x[1] / self.queueHandler.getUpdateDelay(), subsetServers))))
        probs = list()
        for (server, length) in subsetServers:
            prob = np.exp(-length / self.queueHandler.getUpdateDelay()) / total
            probs.append(prob)

        chosen = np.random.choice(serverList, p=probs)
        chosen.submitJob(job)
    
    def tidalWaterFilling(self, job):
        chosen = self.queueHandler.stochasticGetServer()
        chosen.submitJob(job)

    # public getter to access the dispatching algorithm name
    # used for saving results
    def getOperationName(self):
        if (self.op == 1):
            return "Random"
        elif (self.op == 2):
            return "JSQ"
        elif (self.op == 3):
            return "JIQ"
        elif (self.op == 4):
            return "Softmin-JSQ"
        elif (self.op == 5):
            return "JSQ(2)"
        elif (self.op == 6):
            return "Softmin-JSQ(2)"
        elif(self.op == 7):
            return "TWF"
        
    
    # continuously run the dispatcher for the entire simulation
    # and dispatch jobs to the servers
    def run(self, pause):
        count = 0
        while 1:
            count += 1
            # initialise a new job instance
            job = Job(self.env)
            # choose the dispatching operation
            # 1 = Random, 2 = JSQ, 3 = JIQ, 4 = JSQd, 
            # 5 = softminjsq, 6 = softminjsqd, 7 = tidalWaterFilling
            if (self.op == 1):
                self.dispatchRandom(job)
            elif (self.op == 2):
                self.JSQ(job)
            elif (self.op == 3):
                self.JIQ(job)
            elif (self.op == 4):
                self.softminjsq(job)
            elif (self.op == 5):
                self.JSQd(2, job)
            elif (self.op == 6):
                self.softminjsqd(2, job)
            elif (self.op == 7):
                self.tidalWaterFilling(job)
            # pause for a random time given by m / n * l 
            interval = np.random.exponential(pause)
            yield self.env.timeout(interval)
