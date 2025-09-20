import random
import numpy as np
from job import Job

class Dispatcher:
    def __init__(self, env, queueHandler, opName):
        self.opName = opName
        self.env = env
        self.queueHandler = queueHandler
    
    def dispatch(self, job):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def getOperationName(self):
        return self.opName

    def run(self, pause):
        while True:
            job = Job(self.env)
            self.dispatch(job)
            interval = np.random.exponential(pause)
            yield self.env.timeout(interval)


class RandomDispatcher(Dispatcher):
    def __init__(self, env, queueHandler):
        super().__init__(env, queueHandler, "Random")
    
    def dispatch(self, job):
        chosen = random.choice(self.queueHandler.getQueueLengths())
        chosen[0].submitJob(job)
    
class JSQDispatcher(Dispatcher):
    def __init__(self, env, queueHandler):
        super().__init__(env, queueHandler, "JSQ")
    
    def dispatch(self, job):
        bestServer = self.queueHandler.getMinQueueServer()
        bestServer.submitJob(job)

class JIQDispatcher(Dispatcher):
    def __init__(self, env, queueHandler):
        super().__init__(env, queueHandler, "JIQ")
    
    def dispatch(self, job):
        bestServer = None
        for (server, length) in self.queueHandler.getQueueLengths():
            if length == 0:
                bestServer = server
        
        if bestServer is None:
            chosen = random.choice(self.queueHandler.getQueueLengths())
            chosen[0].submitJob(job)
        else:
            bestServer.submitJob(job)

class JSQdDispatcher(Dispatcher):
    def __init__(self, env, queueHandler, d=2):
        super().__init__(env, queueHandler, f"JSQ({d})")
        self.d = d
    
    def dispatch(self, job):
        subsetServers = random.sample(self.queueHandler.getQueueLengths(), self.d)
        minQueueLength = float('inf')
        bestServer = None

        for (server, length) in subsetServers:
            if length < minQueueLength:
                minQueueLength = length
                bestServer = server
        
        bestServer.submitJob(job)

class SoftminJSQDispatcher(Dispatcher):
    def __init__(self, env, queueHandler):
        super().__init__(env, queueHandler, "Softmin-JSQ")
    
    def dispatch(self, job):
        chosen = self.queueHandler.softmaxGetServer()
        chosen.submitJob(job)

class SoftminJSQdDispatcher(Dispatcher):
    def __init__(self, env, queueHandler, d=2):
        super().__init__(env, queueHandler, f"Softmin-JSQ({d})")
        self.d = d
    
    def dispatch(self, job):
        subsetServers = random.sample(self.queueHandler.getQueueLengths(), self.d)
        serverList = list(map(lambda x: x[0], subsetServers))
        total = np.sum(np.exp(list(map(lambda x: -x[1] / self.queueHandler.getUpdateDelay(), subsetServers))))
        probs = list()
        for (server, length) in subsetServers:
            prob = np.exp(-length / self.queueHandler.getUpdateDelay()) / total
            probs.append(prob)

        chosen = np.random.choice(serverList, p=probs)
        chosen.submitJob(job)


class TWFDispatcher(Dispatcher):
    def __init__(self, env, queueHandler):
        super().__init__(env, queueHandler, "TWF")
    
    def dispatch(self, job):
        chosen = self.queueHandler.stochasticGetServer()
        chosen.submitJob(job)

