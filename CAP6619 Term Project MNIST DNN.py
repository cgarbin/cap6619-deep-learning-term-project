"""
CAP-6619 Deep Learning Fall 2018 term project
MNIST with standard deep neural network and dropout
"""

import time
import pandas as pd
import collections
from keras import models
from keras import layers
from keras import optimizers
from keras import backend
from keras.utils import to_categorical
from keras.constraints import max_norm
from keras.datasets import mnist

# Store data from the experiments
experiments = pd.DataFrame(columns=["Description", "DataSetName", "Optimizer",
                                    "TestLoss", "TestAccuracy",
                                    "HiddenLayers", "UnitsPerLayer", "Epochs",
                                    "BatchSize", "DropoutRateInput",
                                    "DropoutRateHidden", "LearningRate",
                                    "MaxNorm", "Momentum",
                                    "ModelParamCount", "TrainingCpuTime",
                                    "TestCpuTime"])


def run_experiment(description, model, parameters):
    """Run an experiment: train and test the network, save results"""
    # To make lines shorter
    p = parameters

    print(description)

    start = time.process_time()
    model.fit(train_images, train_labels,
              epochs=p.epochs, batch_size=p.batch_size)
    training_time = time.process_time() - start

    start = time.process_time()
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    test_time = time.process_time() - start

    optimizer = model.optimizer

    experiments.loc[len(experiments)] = [description, "MNIST",
                                         type(optimizer).__name__, test_loss,
                                         test_acc, p.hidden_layers,
                                         p.units_per_layer,
                                         p.epochs, p.batch_size,
                                         p.dropout_rate_input_layer,
                                         p.dropout_rate_hidden_layer,
                                         backend.eval(optimizer.lr),
                                         p.max_norm_max_value,
                                         p.dropout_momentum,
                                         model.count_params(),
                                         training_time, test_time]


def test_network_configurations(parameters,
                                standard_optimizer, dropout_optimizer,
                                end_experiment_callback):
    """Test all network configurations with the given parameters."""
    # To make lines shorter
    p = parameters

    # Standard network (no dropout)
    model = models.Sequential()
    model.add(layers.Dense(p.units_per_layer,
                           activation='relu', input_shape=(28 * 28,)))
    for _ in range(p.hidden_layers - 1):
        model.add(layers.Dense(p.units_per_layer, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer=standard_optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())
    run_experiment("Standard network", model, p)
    end_experiment_callback()

    # Adjust number of units in each layer: "...if an n-sized layer is optimal
    # for a standard neural net on any given task, a good dropout net should
    # have at least n/p units." [Keras is "drop", not "keep", hence the "1 -"]
    adjusted_units_hidden = int(
        p.units_per_layer / (1 - p.dropout_rate_hidden_layer))

    # Dropout without adjustment to number of units (for comparison)
    # Dropout is applied to all layers, as shown in figure 1.b in the paper
    model = models.Sequential()
    model.add(layers.Dropout(p.dropout_rate_input_layer,
                             input_shape=(28 * 28,)))
    for _ in range(p.hidden_layers):
        model.add(layers.Dense(p.units_per_layer, activation='relu',
                               kernel_constraint=max_norm(p.max_norm_max_value)))
        model.add(layers.Dropout(rate=p.dropout_rate_hidden_layer))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer=dropout_optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())
    run_experiment("Dropout, no unit adjustment", model, p)
    end_experiment_callback()

    # Dropout with adjustment to number of units
    # Dropout is applied to all layers, as shown in figure 1.b in the paper
    model = models.Sequential()
    model.add(layers.Dropout(p.dropout_rate_input_layer,
                             input_shape=(28 * 28,)))
    for _ in range(p.hidden_layers):
        model.add(layers.Dense(adjusted_units_hidden, activation='relu',
                               kernel_constraint=max_norm(p.max_norm_max_value)))
        model.add(layers.Dropout(rate=p.dropout_rate_hidden_layer))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer=dropout_optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())
    run_experiment("Dropout, units adjusted", model, p)
    end_experiment_callback()


# Load and prepare data
start = time.process_time()
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
end = time.process_time()
print("Timing: load and prepare data: {0:.5f}s".format(end - start))

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

# Parameters to control the experiments.
Parameters = collections.namedtuple("Parameters", [
    # Number of hidden layers in the network. When a dropout network is used,
    # each hidden layer will be followed by a dropout layer.
    "hidden_layers",
    # Number of units in each layer (note that dropout layers are adjusted,
    # increasing the number of units used in the network).
    "units_per_layer",
    # Number of epochs to train.
    "epochs",
    # Number of samples in each batch.
    "batch_size",
    # Dropout rate for the input layer ("For input layers, the choice depends
    # on the kind of input. For real-valued inputs (image patches or speech
    # frames), a typical value is 0.8.)" [Note: keras uses "drop", not "keep"]
    "dropout_rate_input_layer",
    # Dropout rate for the input layer ("Typical values of p for hidden units
    # are in the range 0.5 to 0.8.)" [Note: keras uses "drop", not "keep" rate]
    "dropout_rate_hidden_layer",
    # Dropout learning rate multiplier, as recommended in the dropout paper
    # ("... dropout net should typically use 10-100 times the learning rate
    # that was optimal for a standard neural net.")
    "dropout_lr_multiplier",
    # Momentum, as recommended in the dropout paper ("While momentum values of
    # 0.9 are common for standard nets, with dropout we found that values
    # around 0.95 to 0.99 work quite a lot better.")
    "dropout_momentum",
    # Max norm max value. The paper recommends its usage ("Although dropout
    # alone gives significant improvements, using dropout along with
    # max-norm... Typical values of c range from 3 to 4.")
    "max_norm_max_value",
])

p = Parameters(
    hidden_layers=2,
    units_per_layer=1024,
    epochs=5,
    batch_size=128,
    dropout_rate_input_layer=0.2,
    dropout_rate_hidden_layer=0.5,
    dropout_lr_multiplier=10.0,
    dropout_momentum=0.95,
    max_norm_max_value=3
)

# The SGD optimizer to use in standard networks (no dropout).
optimizer_sgd_standard = optimizers.SGD()
# The SGD optimizer to use in dropout networks.
optimizer_sgd_dropout = optimizers.SGD(
    lr=backend.eval(optimizer_sgd_standard.lr) * p.dropout_lr_multiplier,
    momentum=p.dropout_momentum)

# The RMSProp optimizer to use in standard networks (no dropout).
# The paper doesn't mention what optimizer was used in the tests. It looks
# like those tests were done with SGD. I tried RMSProp here because it's a
# popular one nowadays and the one used in the Deep Learning With Python
# book. It results in good accuracy with the default learning rate.
optimizer_rmsprop_standard = optimizers.RMSprop()
# The RMSProp optimizer to use in dropout networks.
# Increasing the learn rate for the RMSProp optimizer resulted in much worse
# accuracy. To prevent that we use the default optimizer for dropout.
optimizer_rmsprop_dropout = optimizer_rmsprop_standard

# File where the results will be saved (the name encodes the parameters used
# in the experiments)
file_name = "MNIST DNN hl={:03d} uhl={:04d} dri={:0.2f} drh={:0.2f} e={:02d} dlrm={:03.1f} dm={:0.2f} mn={} bs={:04d}.txt" \
    .format(p.hidden_layers, p.units_per_layer, p.dropout_rate_input_layer,
            p.dropout_rate_hidden_layer, p.epochs,
            p.dropout_lr_multiplier, p.dropout_momentum, p.max_norm_max_value,
            p.batch_size)


def save_step():
    """Show results as we get them, to let us monitor progress"""
    print(experiments)
    with open(file_name, "w") as outfile:
        experiments.to_string(outfile)


test_network_configurations(p, standard_optimizer=optimizer_sgd_standard,
                            dropout_optimizer=optimizer_sgd_dropout,
                            end_experiment_callback=save_step)

test_network_configurations(p, standard_optimizer=optimizer_rmsprop_standard,
                            dropout_optimizer=optimizer_rmsprop_dropout,
                            end_experiment_callback=save_step)
