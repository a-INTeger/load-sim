import simpy, argparse
import numpy as np
from server import Server
from dispatcher import Dispatcher
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(prog="load-sim",
                                 description="A short simulation for load balancing"
                                 )
parser.add_argument("servercount", help="The number of servers to use within the simulation", type=int)
parser.add_argument("-t","--time", help="Time to run the simulation", type=int)
parser.add_argument("dispatchercount", help="The number of dispatchers within the simulation", type=int)
args = parser.parse_args()

results = {}
intervals = [i for i in range(1, 75, 5)]
for op in range(1, 2):
    avgDelay = []
    for interval in intervals:
        delaysArr = []
        env = simpy.Environment()
        serverArr = [Server(env, str(i), delaysArr) for i in range(args.servercount)]
        dispatcherArr = [Dispatcher(env, serverArr, str(i), op) for i in range(args.dispatchercount)]
        for dispatch in dispatcherArr:
            env.process(dispatch.run(interval))

        if args.time:
            env.run(until=args.time)
        else:
            env.run(until=2500)

        avgDelay.append(np.mean(delaysArr))
    results[dispatcherArr[0].getOperationName()] = avgDelay

x = list(map(lambda x: args.dispatchercount / (args.servercount * x) , intervals))
fig, ax = plt.subplots()
for key in results:
    ax.plot(x, results[key], label=key)
plt.legend(loc="upper left")
plt.show()

print(np.mean(delaysArr))
