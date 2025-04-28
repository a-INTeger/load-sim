import simpy, argparse
import numpy as np
from server import Server
from dispatcher import Dispatcher
from queuehandler import QueueHandler
import matplotlib.pyplot as plt

# define command line arguments
# - servercount: number of servers to use within the simulation
# - time: time to run the simulation
# - dispatchercount: number of dispatchers within the simulation
# - constant: constant to change the fixed time delay by
# - file: file name to save results data under (NOT PATH)
# - runNumber: number of runs to do
parser = argparse.ArgumentParser(prog="load-sim",
                                 description="A short simulation for load balancing"
                                 )
parser.add_argument("servercount", help="The number of servers to use within the simulation", type=int)
parser.add_argument("-t","--time", help="Time to run the simulation", type=int)
parser.add_argument("dispatchercount", help="The number of dispatchers within the simulation", type=int)
parser.add_argument("constant", help="Constant to change the fixed time delay by", type=float)
parser.add_argument("file", help="file name to save results data under (NOT PATH)")
args = parser.parse_args()

# final dictionary to hold all result runtimes etc.
finalResults = {}

# run for 10 times to minimise the effect of randomisation
for runNumber in range(10):
    results = {}    # runtime results for current run
    LAMBDAS = np.linspace(0.0, 1.0, num=50)[1:] # range of lambda values to test
    for op in range(1, 8): # test across all operations
        # 1 = Random, 2 = JSQ, 3 = JIQ, 4 = JSQd, 5 = softminDistribute, 6 = softminDistributed, 7 = softminDistributedd
        avgDelay = []
        for Lambda in LAMBDAS:
            # initialise the environment
            delaysArr = []
            env = simpy.Environment()
            serverArr = [Server(env, str(i)) for i in range(args.servercount)]
            interval = args.dispatchercount / (args.servercount * Lambda)        
            queueHandler = QueueHandler(serverArr, env, args.constant , Lambda)
            dispatcherArr = [Dispatcher(env, queueHandler, str(i), op) for i in range(args.dispatchercount)]
            # start the queuehandler
            env.process(queueHandler.getCurrentQueueStatus())

            #start the dispatchers
            for dispatch in dispatcherArr:
                env.process(dispatch.run(interval))

            # if a runtime is declared, run for that amount of time
            if args.time:
                env.run(until=args.time)
            else:
                # run for 2500 units of time
                env.run(until=2500)

            # combine all server delay arrays into one
            for server in serverArr:
                delaysArr += server.getDelayArr()

            avgDelay.append(np.mean(delaysArr))
        results[dispatcherArr[0].getOperationName()] = avgDelay
    finalResults[runNumber] = results

# save all results to the npy file
np.save("c"+ str(args.constant) + "_" +'results_data_' + args.file + '.npy', finalResults)
