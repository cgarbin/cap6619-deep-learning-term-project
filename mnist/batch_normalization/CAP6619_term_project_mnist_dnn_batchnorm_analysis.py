"""
CAP-6619 Deep Learning Fall 2018 term project
MNIST with standard deep neural network and batch normalization

Read test result files and generate graphs for analysis.
"""
import pandas as pd
import glob

# Get all result files from current directory
all_files = glob.glob("MNIST_DNN_BatchNorm_*.txt")
# Create a generator to get data from one file at a time
file_generator = (pd.read_csv(f, delim_whitespace=True) for f in all_files)
# Read all files using the generator and concatenates them (ignore_index=True
# creates a unique index across all files)
results = pd.concat(file_generator, ignore_index=True)

# Save combined results into files
with open("mnist_batchnorm_results_all.txt", "w") as f:
    results.to_string(f)
with open("mnist_batchnorm_results_top10_accuracy_overall.txt", "w") as f:
    results.nlargest(10, "TestAccuracy").to_string(f)
with open("mnist_batchnorm_results_top10_accuracy_batchnorm.txt", "w") as f:
    results.loc[results["Description"] != "standard_network"]. \
        nlargest(10, "TestAccuracy").to_string(f)
with open("mnist_batchnorm_results_top10_accuracy_no_batchnorm.txt", "w") as f:
    results.loc[results["Description"] == "standard_network"]. \
        nlargest(10, "TestAccuracy").to_string(f)
