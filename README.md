# load-sim
Simulation environment for different load-balancing algorithms.
Requires Python 3.12.5

# Installation
Clone the repository and intialize a virtual environment and load the necessary files
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Adding modules
Enter virtual environment and use `pip install [package name]` to install a package.
Make sure after installing a package to run `pip freeze > requirements.txt`

# Running the loadsim
For the generic runs to gather average delay data:
```
python loadsimtestenv.py servers dispatchers constant run_name -t TIME
```
servers - Number of servers within system
dispatchers - Number of dispatchers within system
constant - ratio between incoming rate of jobs and time between update
run_name - name to save data under

Example:
```
python loadsimtestenv.py 10 5 1.0 "testrun" -t 6000
```
For an environment that contains 10 servers, 5 dispatchers with c = 1.0 which runs for 6000 units of sim time, saved under c1.0_results_data_testrun.npy

For running a specific run with a specific value of $\lambda$ with all data being saved to csvs
```
python specifictestenv.py servers dispatchers constant run_name -t TIME
```
make sure to change the value for $\lambda$ within the python file, the csvs will be saved under `csvs/run_name/`

# Generating the graphs
To generate the average delay vs $\lambda$ graphs from a `.npy` file simply run the command
```
python dataloader.py file_name
```
the graph will be saved under the `file_name.png`.


To generate the CCDF graphs from the csvs files run:
```
python csvdataloader.py folder_name
```

the graph will be saved within the csvs folder under `CCDF_folder_name.png`