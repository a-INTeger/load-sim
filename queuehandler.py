import numpy as np
from operator import itemgetter

class QueueHandler:
    def __init__(self, serverArr, env, constant, rate):
        # attach list of servers to the queue handler
        self.serverArr = serverArr
        # main server queue length list
        self.serverQueueLengths = list()
        # attach environment
        self.env = env
        # keep track of the server with the minimum queue length
        self.minQueueServer = None
        #  list of different dispatching method probabilities
        self.softminProbs = list()
        self.stochasticProbs = list()
        # Update rate of server queue length
        self.updateDelay = constant / rate
        self.rate = rate

    # constantly get the current queue status of all servers
    # and update the queue length list
    def getCurrentQueueStatus(self):
        while 1:
            # empty and refill the server queue length list
            self.serverQueueLengths.clear()
            for server in self.serverArr:
                self.serverQueueLengths.append([server, len(server.getQueue().items)])

            # find the server with the minimum queue length
            self.findMinQueueServer()

            # generate softmin-JSQ probabilities
            self.generateQueueProbabilities()

            # generate TWF probabilities
            waterLev = self.genWaterLevel()
            self.computeprobs(waterLev)

            # pause for the update delay
            yield self.env.timeout(self.updateDelay)
    
    # public getter to access queue lengths
    def getQueueLengths(self):
        return self.serverQueueLengths
    

    # iterate through the server queue lengths
    # and find the server with the minimum queue length
    def findMinQueueServer(self):
        minQueueLength = float('inf')
        for (server, length) in self.serverQueueLengths:
            if length < minQueueLength:
                minQueueLength = length
                self.minQueueServer = server
        
    # public getter to access the server with the minimum queue length
    def getMinQueueServer(self):
        return self.minQueueServer
    
    # public getter to access the update delay
    def getUpdateDelay(self):
        return self.updateDelay
    
    # generate softmin-JSQ probabilities
    def generateQueueProbabilities(self):
        total = np.sum(np.exp(list(map(lambda x: -x[1] / self.updateDelay, self.serverQueueLengths))))
        self.softminProbs.clear()
        for (server, length) in self.serverQueueLengths:
            prob = np.exp(-length / self.updateDelay) / total
            self.softminProbs.append(prob)

    # select a server based on the softmin-JSQ probabilities
    def softmaxGetServer(self):
        return np.random.choice(self.serverArr, p=self.softminProbs)
    
    # calculate the water level for the server queue lengths
    def genWaterLevel(self):
        # calculate the number of jobs to be added
        a = len(self.serverQueueLengths) * self.rate * self.updateDelay + 1 
        # make list of queue lengths without the server objects
        tmp = list(map(lambda x: x[1], self.serverQueueLengths))
        # algorithm 1 of TWF paper
        while (a > 0):
            tmp = sorted(tmp)
            minSet = [v for v in tmp if v == tmp[0]]
            if len(minSet) == len(tmp):
                return tmp[0] + (a / len(tmp))            
            nextMin = sorted(list(set(tmp)))[1]
            delta = nextMin - tmp[0]

            if delta * len(minSet) < a:
                a = a - delta * len(minSet)
                for i in range(len(minSet)):
                    tmp[i] += delta

            else:
                return tmp[0] + (a / len(minSet))
            
    #  compute the probabilities for TWF 
    #  given by equation 3.2
    def computeprobs(self, waterLevel):
        a = len(self.serverQueueLengths) * self.rate * self.updateDelay + 1
        diffWLQ = [waterLevel - x[1] for x in self.serverQueueLengths]
        gPlus = sum(1 for x in diffWLQ if x > 0)

        if gPlus == 0:
            # If gPlus is zero, assign equal probability to all
            self.stochasticProbs = [1 / len(self.serverQueueLengths)] * len(self.serverQueueLengths)
            return

        p = [(max(0, (diffWLQ[idx] - 1 / gPlus) / (a - 1))) for idx in range(len(self.serverQueueLengths))]

        total = sum(p)
        if total == 0:
            # If total probability is 0, assign equal probability to avoid division errors
            self.stochasticProbs = [1 / len(self.serverQueueLengths)] * len(self.serverQueueLengths)
        else:
            # Normalize p to sum to 1
            self.stochasticProbs = [x / total for x in p]

    # select a server based on the TWF probabilities
    def stochasticGetServer(self):
        return np.random.choice(self.serverArr, p=self.stochasticProbs)