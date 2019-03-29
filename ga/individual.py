import random

from nn.neural_network import *


class Individual:

    def __init__(self):
        self.input_to_hidden = Neuron(20, 15)
        self.hidden_to_output = Neuron(3, 20)
        self.brain = NeuralNetwork(self.input_to_hidden, self.hidden_to_output)
        self.fitness = 0
        self.gene_size = 2
        self.genes = [[self.input_to_hidden.weights], [self.hidden_to_output.weights]]

    def generate(self):
        for i in range(self.gene_size):
            self.genes.append(random.random())

    def get_gene(self, gene_index, gene_code):
        return str(self.genes[gene_index])[gene_code]

    def mutate_gene(self, index):
        self.genes[index] = random.random()
