import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, argparse, errno
from json import load


parser = argparse.ArgumentParser(prog="load-sim-graph-generator",
                                 description="convert results generated into graphs"
                                 )
parser.add_argument("filename",
                     help="the .json file name where the results are stored must be in the same directory as this script",
                     type=str)
args = parser.parse_args()


if not os.path.exists(f"./results/{args.filename}"):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"./results/{args.filename}")

# load the data
with open(f"./results/{args.filename}", "r") as f:
    data = load(f)

df = pd.DataFrame.from_dict(data)
x_name = "Average Incoming Job Rate Per server (\u03BB)"
df.index.name=x_name
df.index = df.index.astype('float64')


long_df = (
    df.reset_index()
      .melt(id_vars=x_name, var_name="line", value_name="delay")
      .explode("delay")
)

long_df[x_name] = long_df[x_name].astype('float64')
long_df["delay"] = long_df["delay"].astype('float64')

# print(long_df.query("line == 'Random'"))

# set large figure size
plt.figure(figsize=(12.8, 9.6))


# plot each line
sns.lineplot(data=long_df, x=x_name, y="delay", errorbar=("pi", 25), estimator="mean", hue="line")

plt.show()
# # title and save the graph
# plt.title("Average Delay vs. Average Incoming Job Rate Per server (\u03BB)")
# plt.legend(loc="upper left")

# plt.savefig(f"a.png", dpi=180)
