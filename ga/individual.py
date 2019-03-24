import random


class Individual:

    def __init__(self):
        self.fitness = 0
        self.gene_size = 3
        self.genes = []

    def generate(self):
        for i in self.gene_size:
            self.genes.append(random.random())

    def get_gene(self, gene_index, gene_code):
        return str(self.genes[gene_index])[gene_code]

    # def set_gene(self, index, new_gene):
    #     self.genes[index] = new_gene
    #     self.fitness = 0

    def mutate_gene(self, index):
        pass
