import operator
import random

# group players into species based on how similar their brains are
class Species:
    def __init__(self, player):
        self.players = []
        self.average_fitness = 0
        self.threshold = 1.5 # maximum difference between networks to be considered similar
        self.players.append(player)

        # the "representative" brain of the species
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()

        # species always keep their best player
        self.champion = player.clone()
        # how many generations passed with no improvement
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(b1, b2):
        total = 0
        count = min(len(b1.connections), len(b2.connections))
        for i in range(count):
            total += abs(b1.connections[i].weight - b2.connections[i].weight)
        return total / count

    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        # see if the species produced a better player
        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        # if multiple players exist choose a parent randomly
        if len(self.players) > 1:
            baby = self.players[random.randint(1, len(self.players)) - 1].clone()
        else:
            baby = self.players[0].clone()
        baby.brain.mutate()
        return baby