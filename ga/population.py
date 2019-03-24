from ga.individual import Individual


class Population:

    def __init__(self, pop_size, initialise):
        self.individuals = []
        if initialise:
            for i in range(pop_size):
                ind = Individual()
                ind.generate()
                self.individuals.append(ind)

    # def get_individual(self, index):
    #     return self.individuals[index]

    def set_individual(self, index, ind):
        self.individuals[index] = ind

    def get_fittest(self):
        fittest = None
        for ind in self.individuals:
            if fittest is None:
                fittest = ind
                continue
            if ind.fitness > fittest.fitness:
                fittest = ind
        return fittest
