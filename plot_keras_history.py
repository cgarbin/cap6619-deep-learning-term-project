"""
Plot accuracy and loss data generated by Keras models fit() function.

Data is read from a JSON file, crated with json.dump(history)
"""
import json
import os
import glob
from argparse import ArgumentParser
from matplotlib import pyplot as plt
import seaborn as sns


def parse_command_line():
    """Parse command line parameters and return it."""
    ap = ArgumentParser(description='Plot Keras history from a JSON file.')
    ap.add_argument("--directory", type=str)
    ap.add_argument("--pattern", type=str)
    args = ap.parse_args()

    return args.directory, args.pattern


def plot_history(history, file, show):
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
    plt.savefig(file)

    if show:
        plt.show()


def plot_all_files(directory, pattern, show):
    full_path = os.path.join(directory, "*" + pattern + "*.json")
    all_files = glob.glob(full_path)

    for file in all_files:
        with open(file) as f:
            print("plotting " + f.name)  # show progress to the user
            history = json.load(f)
            plot_history(history, file + ".png", show)


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
