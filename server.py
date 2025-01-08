import simpy

class Server:
    def __init__(self, env):
        self.env = env
        self.queue = simpy.Store(env)
        self.serverResource = simpy.Resource(env, capacity=1)
        env.process(self.consumeJobs())

    def submitJob(self, job):
        print(f"Added Job {job.jobName} at time {self.env.now} with processing time {job.processTime}")
        self.queue.put(job)

    def consumeJobs(self):
        while 1:
            job = yield self.queue.get()
            with self.serverResource.request() as req:
                yield req
                print("Processing")
                yield self.env.timeout(job.processTime)
                job.process()
