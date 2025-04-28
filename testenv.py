import simpy, argparse, os, sys
import numpy as np
from server import Server
from dispatcher import Dispatcher
from queuehandler import QueueHandler
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(prog="load-sim-short",
                                 description="A short simulation for load balancing designed to run a single test"
                                 )
parser.add_argument("servercount", help="The number of servers to use within the simulation", type=int)
parser.add_argument("dispatchercount", help="The number of dispatchers within the simulation", type=int)
parser.add_argument("constant", help="Constant to change the fixed time delay by", type=float)
parser.add_argument("runname", help="run name to save results data under (NOT PATH)")
parser.add_argument("-t","--time", help="Time to run the simulation", type=int)
args = parser.parse_args()

if os.path.exists(f'./csvs/{args.runname}'):
    sys.exit("Folder already exists, please delete the file or change the run name")
else:
    os.makedirs(f'./csvs/{args.runname}')

LAMBDA = 0.95
for op in range(1, 8):
    env = simpy.Environment()
    serverArr = [Server(env, str(i)) for i in range(args.servercount)]
    interval = args.dispatchercount / (args.servercount * LAMBDA)        
    queueHandler = QueueHandler(serverArr, env, args.constant, LAMBDA)
    dispatcherArr = [Dispatcher(env, queueHandler, str(i), op) for i in range(args.dispatchercount)]
    env.process(queueHandler.getCurrentQueueStatus())
    for dispatch in dispatcherArr:
        env.process(dispatch.run(interval))

    if args.time:
        env.run(until=args.time)
    else:
        env.run(until=2500)

    # combine all server delay arrays into one
    total = []
    for server in serverArr:
        total += server.getDelayArr()
        

    # save all results to a csv file
    with open(f'./csvs/{args.runname}/{dispatcherArr[0].getOperationName()}.csv', 'a') as f:
        np.savetxt(f, total, delimiter=",")
