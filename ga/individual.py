class Individual:

    def __init__(self):
        self.fitness = 0
        self.genes = []

    def generate(self):
        pass

    def get_gene(self, index):
        return self.genes[index]

    def set_gene(self, index, new_gene):
        self.genes[index] = new_gene
        self.fitness = 0

    def mutate_gene(self, index):
        pass
