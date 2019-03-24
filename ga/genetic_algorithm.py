import random

from ga.individual import Individual
from ga.population import Population


class GeneticAlgoritthm:

    def __init__(self):
        self.uniform_rate = 0.5
        self.mutation_rate = 0.015
        self.tournament_size = 5
        self.elitism_offset = 1

    def evolve(self, population):
        new_population = Population(len(population), False)

        new_population.individuals.append(population.get_fittest())

        for i in range(len(population) - self.elitism_offset):
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
            random.choice(population.individuals)
        return tournament_population.get_fittest()

    def reproduce(self, mother, father):
        baby  = Individual()
        for i in range(len(mother.genes)):
            if random.random() < self.uniform_rate:
                baby.set_gene(i, mother.get_gene(i))
            else:
                baby.set_gene(i, father.get_gene(i))
        return baby

    def mutate(self, ind):
        for i in range(len(ind.genes)):
            if random.random() <= self.mutation_rate:
                ind.mutate_gene(i)