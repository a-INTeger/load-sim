import simpy
from job import Job
from server import Server

def jobCreator(env, interval, server):
    count = 0
    while 1:
        count += 1
        job = Job(env, str(count))
        server.submitJob(job)
        yield env.timeout(interval)


if __name__ == "__main__":
    env = simpy.Environment()
    server = Server(env)
    env.process(jobCreator(env, 3, server))

    env.run(until=20)