import numpy as np

class Job:
    def __init__(self, env):
        # attach simpy environment
        self.__env = env
        # NOTE: change this line to change the distribution of the process time
        self.__processTime = np.random.exponential(1)
        # time the job was created
        self.__created = self.__env.now
        # time the job was processed
        self.__processed = None
    
    def process(self):
        # set the process time to the current time
        self.__processed = self.__env.now
        # add the current delay time to the main delay array
        return self.__processed - self.__created


    def getProcessTime(self):
        return self.__processTime
    
