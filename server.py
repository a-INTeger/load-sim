import simpy

class Server:
    def __init__(self, env, name):
        self.__name = name
        self.__env = env
        self.__queue = simpy.Store(env)
        self.__serverResource = simpy.Resource(env, capacity=1)
        self.__delayArr = []
        # start the process of consuming jobs on server creation instead of starting it in main file
        self.__env.process(self.__consumeJobs())

    # continuously consume jobs from the queue
    def __consumeJobs(self):
        while 1:
            job = yield self.__queue.get() # await job from queue if it exists
            with self.__serverResource.request() as req: # attempt to request job from the queue
                # await until there is a job that is available
                yield req 
                yield self.__env.timeout(job.getProcessTime()) # delay the method for the job's process time
                # record the delay for the current job
                delay = job.process()
                self.__delayArr.append(delay)

    # add a job to the server queue when dispatching
    # public method to be called by the dispatcher
    def submitJob(self, job):
        self.__queue.put(job)


    # get server name if you need to identify it
    def getName(self):
        return self.__name
    
    # get the delay array for this server
    # this is for when data needs to be collected at the end of the simulation
    def getDelayArr(self):
        return self.__delayArr
    
    # get the current queue status (mainly for queue handler)
    def getQueue(self):
        return self.__queue


    
