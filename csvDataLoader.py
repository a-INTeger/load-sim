import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob, os, sys, argparse

# define command line arguments
parser = argparse.ArgumentParser(prog="csv-data-loader",
                                 description="convert a series of csv files to a CCDF plot"
                                 )
parser.add_argument("foldername", help="the folder name where the results are stored within ./csvs", type=str)
args = parser.parse_args()

# check if the folder exists
if not os.path.exists(f"./csvs/{args.foldername}"):
    sys.exit("Folder does not exist, please run testenv.py first to generate results")

# convert csvs to dataframes
dataframes = {}
files = [f for f in glob.glob(f"./csvs/{args.foldername}/*") if not f.endswith(".png") and not f.endswith(".py")]
for file in files:
    tmp = pd.read_csv(file)
    tmp.columns = ["delay"]
    name = os.path.basename(file)[:-4]
    dataframes[name] =  tmp

plt.figure(figsize=(12.8, 9.6))

output = []
# plot each dataframe
for key, df in dataframes.items():
    xs = np.linspace(0, 20, num=200)[1:]
    ys = []
    for x in xs:
        ys.append(len(list(filter(lambda z: z > x, df["delay"]))) / len(df["delay"]))
    # NOTE: feel free to change or add percentiles to save in the csv file
    row = [np.round(np.percentile(df["delay"], 25), 3), np.round(np.percentile(df["delay"], 50), 3), np.round(np.percentile(df["delay"], 75), 3)]
    output.append(row)
    
    sns.lineplot(x=xs, y=ys, label=key)


# save quartile performance to csv
np.savetxt(f"./csvs/quartile_results/quartiles_{args.foldername}.csv", output, delimiter=",")

# label and save the CCDF graph
plt.title("Proportion of jobs with a certain delay")
plt.xlabel("Delay")
plt.ylabel("Proportion of jobs")
plt.savefig(f"CCDF_{args.foldername}.png", dpi=180)


