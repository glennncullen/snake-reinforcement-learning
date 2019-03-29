import numpy as np


class Neuron():
    def __init__(self, num_neurons, num_inputs_per_neuron):
        self.weights = np.random.random((num_neurons, num_inputs_per_neuron))


class NeuralNetwork:

    def __init__(self, layer_1, layer_2):
        self.layer_1 = layer_1
        self.layer_2 = layer_2

    def __sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def make_decision(self, inputs):
        # inputs should be in the form: ([[], [], [], []])
        input_to_hidden = self.__sigmoid(np.dot(inputs, self.layer_1.weights))
        hidden_to_output = self.__sigmoid(np.dot(input_to_hidden, self.layer_2.weights))
        return hidden_to_output
