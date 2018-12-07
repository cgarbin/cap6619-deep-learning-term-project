"""
Plot accuracy and loss data generated by Keras models fit() function.

Data is read from a JSON file, crated with json.dump(history)
"""
import json
import os
import glob
import re
from argparse import ArgumentParser
from matplotlib import pyplot as plt
import seaborn as sns


def parse_command_line():
    """Parse command line parameters and return them."""
    ap = ArgumentParser(description='Plot Keras history from a JSON file.')
    ap.add_argument("--directory", type=str)
    ap.add_argument("--pattern", type=str)
    args = ap.parse_args()

    return args.directory, args.pattern


def plot_history(history, file, show):
    """Plot the loss history created from druing the execution of Keras fit().

    Arguments:
      history {[dataframe]} -- The history data from the call to fit()
      file {[string]} -- Name of the input file (the one with the history)
      show {[Boolean]} -- True to also show on screen, False to just save it
    """

    # Style with default seaborn, then change background (easier to read)
    sns.set()
    sns.set_style('white')

    # Fix the y axis scale for all graphs so we can compare graphs
    plt.ylim(0, 0.8)

    # Create a data source for the epochs - need this for the x axis
    epochs = range(1, len(history['loss'])+1)

    # Plot loss data
    sns.lineplot(x=epochs, y=history['loss'], label='Training loss')
    sns.lineplot(x=epochs, y=history['val_loss'], label='Test loss')

    # Change x-axis tick labels (epoch) from float to integers
    plt.xticks(epochs)

    plt.legend()

    # Add a title from the pieces embedded in the file name
    network = re.search(r"nw=(.*?)_", file).group(1)
    optimizer = re.search(r"opt=(.*?)_", file).group(1)
    hidden_layers = re.search(r"hl=(.*?)_", file).group(1)
    units_per_layer = re.search(r"uhl=(.*?)_", file).group(1)
    epochs = re.search(r"e=(.*?)_", file).group(1)
    learning_rate = re.search(r"lr=(.*?)_", file).group(1)

    title = ("{} network \n epochs={} optimizer={} \n"
             "hidden layers={} units in hidden layer={} \n"
             "lr={}").format(
        network, epochs, optimizer, hidden_layers, units_per_layer,
        learning_rate)
    plt.title(title)

    # Save to disk as a .png file
    png_file = file.replace(".json", ".png")
    plt.savefig(png_file)

    if show:
        plt.show()


def plot_all_files(directory, pattern, show):
    full_path = os.path.join(directory, "*" + pattern + "*.json")
    all_files = glob.glob(full_path)

    for file in all_files:
        with open(file) as f:
            print("plotting " + f.name)  # show progress to the user
            history = json.load(f)
            plot_history(history, file, show)


# Change this to "False" when testing from the command line. Leave set to True
# when launching from the IDE and change the parameters below (it's faster
# than dealing with launch.json).
ide_test = True
if ide_test:
    # Show a warning to let user now we are ignoring command line parameters
    print("\n\n  --- Running from IDE - ignoring command line\n\n")
    # Get all history files from a directory...
    directory = "./mnist/dropout/"
    # ...and a specific pattern to select files
    pattern = "quick_test"
    plot_all_files(directory, pattern, show=True)
else:
    directory, pattern = parse_command_line()
    plot_all_files(directory, pattern, show=False)
