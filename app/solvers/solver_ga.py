import random
import networkx as nx
import numpy
from deap import base, creator, tools, algorithms

toolbox = base.Toolbox()

creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))
creator.create('Individual', list, fitness=creator.FitnessMax)


def solve_for_max_profit(graph, starting_node_id, distance_limit):
    is_tournament = nx.tournament.hamiltonian_path(graph)
    print(is_tournament)
    toolbox.register(
        'attr_node_id',
        random.choice,
        list(graph.nodes())
    )

    def create_individual():
        length = random.randint(1, len(graph.nodes()) + 2)
        return [starting_node_id] + [toolbox.attr_node_id() for _ in range(length)]

    def evaluate(individual):
        total_distance = 0
        total_points = 0
        visited = set()
        for i in range(len(individual) - 1):
            [current_ind, next_ind] = (individual[i], individual[i + 1])
            try:
                total_distance += graph[current_ind][next_ind]['cost']
                if next_ind not in visited:
                    total_points += graph.nodes[next_ind]['profit']
                    visited.add(next_ind)
            except KeyError:
                return 0, 0
        if total_distance > distance_limit:
            return 0, 0
        return total_points, total_distance

    toolbox.register('individual', tools.initIterate, creator.Individual, create_individual)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    population = toolbox.population(n=100)
    hof = tools.HallOfFame(10)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, halloffame=hof, verbose=True, stats=stats)
    print('\nHALL OF FAME:')
    print(f'with distance limit of: {distance_limit} steps')
    for index, individual in enumerate(hof):
        print(
            f'{index + 1}.\t{individual} points: {individual.fitness.values[0]}, distance: {individual.fitness.values[1]}')
