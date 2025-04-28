import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, argparse, sys


parser = argparse.ArgumentParser(prog="npy-average-delay-generator",
                                 description="convert a series of csv files to a CCDF plot"
                                 )
parser.add_argument("filename",
                     help="the .npy file name where the results are stored must be in the same directory as this script",
                     type=str)
args = parser.parse_args()


if not os.path.exists(f"./{args.filename}"):
    sys.exit(f"file {args.filename} does not exist, please run loadsimtestenv.py first to generate results")

# load the data
data = dict(enumerate(np.load(args.filename, allow_pickle=True).flatten(), 1))[1]
# pick which algorithms to plot 
# MUST BE THE SAME AS IN THE DISPATCHER CLASSS
opNames = ["Random", "JSQ", "JIQ", "Softmin-JSQ", "JSQ(2)", "Softmin-JSQ(2)", "TWF"]
# opNames = ["Softmin-JSQ", "Softmin-JSQ(2)", "TWF"]
res = {}
# convert npys to arrays for plotting
for opName in opNames:
    arr = []
    for runNumber, runResults in data.items():
        for dispatch, results in runResults.items():
            if dispatch == opName:
                arr.append(results)
    res[opName] = arr


# set large figure size
plt.figure(figsize=(12.8, 9.6))

# plot each line 
for key, arr in res.items():
    df = pd.DataFrame(arr)
    df.columns = np.linspace(0.0, 1.0, num=50)[1:]
    df = df.T
    df.index.name="Average Incoming Job Rate Per server (\u03BB)"
    df_melted = df.reset_index().melt(id_vars="Average Incoming Job Rate Per server (\u03BB)", var_name="run", value_name="Average Delay")


    sns.lineplot(data=df_melted, x="Average Incoming Job Rate Per server (\u03BB)", y="Average Delay", label=key)

# title and save the graph
plt.title("Average Delay vs. Average Incoming Job Rate Per server (\u03BB)")
plt.legend(loc="upper left")

plt.savefig(f"{args.filename[:-4]}.png", dpi=180)
