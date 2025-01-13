import simpy
import numpy as np
from server import Server
from dispatcher import Dispatcher
import argparse


parser = argparse.ArgumentParser(prog="load-sim",
                                 description="A short simulation for load balancing"
                                 
                                 )


delaysArr = []
env = simpy.Environment()
serverArr = [Server(env, str(i), delaysArr) for i in range(10)]
dispatcher = Dispatcher(env, serverArr)
env.process(dispatcher.run(1))

env.run(until=500)
print(np.mean(delaysArr))