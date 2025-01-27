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


LAMBDAS = np.linspace(0.1, 1.0, num=100)
for op in range(1, 4):
    avgDelay = []
    for Lambda in LAMBDAS:
        total = 0
        for _ in range(5):
            delaysArr = []
            env = simpy.Environment()
            serverArr = [Server(env, str(i), delaysArr) for i in range(args.servercount)]
            interval = args.dispatchercount / (args.servercount * Lambda)
            dispatcherArr = [Dispatcher(env, serverArr, str(i), op) for i in range(args.dispatchercount)]
            for dispatch in dispatcherArr:
                env.process(dispatch.run(interval))

            if args.time:
                env.run(until=args.time)
            else:
                env.run(until=2500)
            total += np.mean(delaysArr)
        avgDelay.append(total / 5)
    results[dispatcherArr[0].getOperationName()] = avgDelay

x = LAMBDAS
fig, ax = plt.subplots()
for key in results:
    ax.plot(x, results[key], label=key)
# ax.plot(x, 1 / (1 - x), label="Theoretical")
ax.set(xlabel='Lambda', ylabel='Average Delay',
       title='Average Delay vs Lambda')
plt.legend(loc="upper left")
plt.show()
