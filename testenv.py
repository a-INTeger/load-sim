import simpy
import numpy as np
from server import Server
from dispatcher import Dispatcher
import argparse


parser = argparse.ArgumentParser(prog="load-sim",
                                 description="A short simulation for load balancing"
                                 )
parser.add_argument("servercount", help="The number of servers to use within the simulation", type=int)
parser.add_argument("-t","--time", help="Time to run the simulation", type=int)
args = parser.parse_args()
delaysArr = []
env = simpy.Environment()
serverArr = [Server(env, str(i), delaysArr) for i in range(args.servercount)]
dispatcherArr = [Dispatcher(env, serverArr, str(i)) for i in range(10)]
for dispatch in dispatcherArr:
    env.process(dispatch.run())

if args.time:
    env.run(until=args.time)
else:
    env.run(until=500)
print(np.mean(delaysArr))
