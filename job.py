import simpy, random

class Job:
    def __init__(self, env, jobName):
        self.env = env
        self.jobName = jobName
        self.processTime = random.randint(1, 10)
        self.created = self.env.now
        self.processed = None
    
    def process(self):
        self.process = self.env.now
        print(f"Job {self.jobName} processed at {self.process}")

