"""Parameters to control the experiments.

These parameters drive the code. Modify them to test different configurations.
"""
import collections

# Parameters to control the experiments.
Parameters = collections.namedtuple('Parameters', [
    # A brief description of the experiment. Will be used as part of file names
    # to prevent collisions with other experiments. Cannot contain spaces to
    # work correctly as a command line parameter.
    'experiment_name',
    # Type of network to test: only valid choice is 'batch_normalization'. The
    # standard network type (no batch normalization) can be tested with the
    # dropout code, to avoid duplication.
    'network',
    # Type of optimizer to use: 'sgd' or 'rmsprop'.
    'optimizer',
    # Number of hidden layers in the network. When a batch normalization
    # network is used, each hidden layer will be followed by a batch
    # normalization layer.
    'hidden_layers',
    # Number of units in each layer.
    'units_per_layer',
    # Number of epochs to train.
    'epochs',
    # Number of samples in each batch.
    'batch_size',
    # Learning rate - can be increased for batch normalization ('In a batch-
    # normalized model, we have been able to achieve a training speedup from
    # higher learning rates, with no ill side effects').
    # The default Keras values are SGD: 0.01, RMSProp: 0.001 (see
    # https://keras.io/optimizers/).
    'learning_rate',
    # Weight decay (L2).
    'decay',
    # Momentum for the SGD optimizer (not used in RMSProp). The paper mentions
    # as a side noe ('SGD variants such as momentum... have been used to
    # achieve state of the art performance.)' and it has proven to benefitial
    # in the dropout tests.
    'sgd_momentum',
])
