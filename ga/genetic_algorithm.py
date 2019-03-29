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
        for i in range(len(mother.input_to_hidden.weights)):
            for y in range(len(mother.input_to_hidden.weights[0])):
                new_gene = ""
                new_gene_size = min(
                    mother.input_to_hidden.weights[i][y],
                    father.input_to_hidden.weights[i][y],
                )
                for x in range(new_gene_size):
                    if random.random() < self.uniform_rate:
                        new_gene += mother.get_gene(i, y, x, True, False)
                    else:
                        new_gene += father.get_gene(i, y, x, True, False)
                baby.input_to_hidden.weights[i][y] = float(new_gene)
        for i in range(len(mother.hidden_to_output.weights)):
            for y in range(len(mother.hidden_to_output.weights[0])):
                new_gene = ""
                new_gene_size = min(
                    mother.hidden_to_output.weights[i][y],
                    father.hidden_to_output.weights[i][y],
                )
                for x in range(new_gene_size):
                    if random.random() < self.uniform_rate:
                        new_gene += mother.get_gene(i, y, x, False, True)
                    else:
                        new_gene += father.get_gene(i, y, x, False, True)
                baby.hidden_to_output.weights[i][y] = float(new_gene)
        return baby

    def mutate(self, ind):
        for i in range(len(ind.input_to_hidden.weights)):
            for y in range(len(ind.input_to_hidden.weights[0])):
                if random.random() <= self.mutation_rate:
                    ind.mutate_gene(i, y, True, False)
        for i in range(len(ind.hidden_to_output.weights)):
            for y in range(len(ind.hidden_to_output.weights[0])):
                if random.random() <= self.mutation_rate:
                    ind.mutate_gene(i, y, False, True)
