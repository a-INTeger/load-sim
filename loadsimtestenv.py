import simpy, argparse, concurrent.futures
from json import dump
from collections import defaultdict
import numpy as np
from server import Server
from dispatcher import *
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

# get all subclasses of dispatcher (saves calling them per run)
allDispatchers = [cls for cls in Dispatcher.__subclasses__()]

# final dictionary to hold all result runtimes etc.
finalResults = {}


def single_run(runNumber, args, allDispatchers):
    results = {}
    LAMBDAS = np.linspace(0.0, 1.0, num=50)[1:] # range of lambda values to test

    for cls in allDispatchers: # test across all operations
        opName = cls(None, None).getOperationName()
        results[opName] = {}
        for Lambda in LAMBDAS:
            # initialise the environment
            delaysArr = []
            env = simpy.Environment()
            serverArr = [Server(env, str(i)) for i in range(args.servercount)]
            interval = args.dispatchercount / (args.servercount * Lambda)        
            queueHandler = QueueHandler(serverArr, env, args.constant , Lambda)
            dispatcherArr = [cls(env, queueHandler) for i in range(args.dispatchercount)]
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

            results[opName][Lambda] = delaysArr

    return runNumber, results
    

def merge_results(finalResults, LAMBDAS):
    mergedResults = defaultdict(lambda: defaultdict(list))
    
    for runNumber, results in finalResults.items():
        for opName, lambdaDict in results.items():
            for Lambda, delays in lambdaDict.items():
                mergedResults[opName][Lambda].extend(delays)  # merge delay arrays
    
    # convert back to normal dict for saving
    return {op: dict(lambdas) for op, lambdas in mergedResults.items()}

# run for 10 times to minimise the effect of randomisation
def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(single_run, runNumber, args, allDispatchers) for runNumber in range(10)]
        for future in concurrent.futures.as_completed(futures):
            runNumber, results = future.result()
            finalResults[runNumber] = results

    mergedResults = merge_results(finalResults, np.linspace(0.0, 1.0, num=50)[1:])

    with open(f"results/{args.file}.json", "w") as f:
        dump(mergedResults, f, indent=4)

if __name__ == "__main__":
    main()
    

