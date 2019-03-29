import random

from ga.individual import Individual
from ga.population import Population


class GeneticAlgorithm:

    def __init__(self):
        self.uniform_rate = 0.5
        self.mutation_rate = 0.015
        self.tournament_size = 5
        self.elitism_offset = 1

    def evolve(self, population):
        new_population = Population(len(population.individuals), False)

        new_population.individuals.append(population.get_fittest())

        for i in range(len(population.individuals) - self.elitism_offset):
            if i <= self.elitism_offset:
                continue
            mother = self.tournament(population)
            father = self.tournament(population)
            baby = self.reproduce(mother, father)
            new_population.individuals.append(baby)

        for i in range(len(new_population.individuals)):
            if i <= self.elitism_offset:
                continue
            self.mutate(new_population.individuals[i])

        return new_population

    def tournament(self, population):
        tournament_population = Population(self.tournament_size, False)
        for i in range(self.tournament_size):
            tournament_population.individuals.append(random.choice(population.individuals))
        return tournament_population.get_fittest()

    def reproduce(self, mother, father):
        baby = Individual()
        for i in range(mother.gene_size):
            new_gene = ""
            new_gene_size = min(len(str(mother.genes[i])), len(str(father.genes[i])))
            for y in range(new_gene_size):
                if random.random() < self.uniform_rate:
                    new_gene += mother.get_gene(i, y)
                else:
                    new_gene += father.get_gene(i, y)
            baby.genes.append(float(new_gene))
        return baby

    def mutate(self, ind):
        for i in range(len(ind.genes)):
            if i < 3:
                continue
            if random.random() <= self.mutation_rate:
                ind.mutate_gene(i)
