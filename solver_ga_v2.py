import random
import numpy
from deap import base, creator, tools, algorithms

toolbox = base.Toolbox()

creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))
creator.create('Individual', list, fitness=creator.FitnessMax)


def solve_for_max_profit(graph, starting_node_id, distance_limit):
    toolbox.register(
        'attr_node_id',
        random.choice,
        list(graph.nodes())
    )

    def create_individual():
        length = random.randint(1, len(graph.nodes()))
        return [starting_node_id] + [toolbox.attr_node_id() for _ in range(length)]

    def evaluate(individual):
        total_distance = 0
        total_points = 0
        visited = set()
        for i in range(len(individual) - 1):
            current_ind, next_ind = (individual[i], individual[i + 1])
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

    def mutate_path_length(individual, available_nodes, add_prob=0.8):
        if random.random() < add_prob:
            new_node = random.choice(available_nodes)
            idx = random.randint(1, len(individual))
            individual.insert(idx, new_node)

        return individual,

    toolbox.register('individual', tools.initIterate, creator.Individual, create_individual)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_path_length, available_nodes=list(graph.nodes()), add_prob=0.5)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    population = toolbox.population(n=10_000)
    hof = tools.HallOfFame(10)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)

    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, halloffame=hof, verbose=True, stats=stats)

    print('\nHALL OF FAME:')
    print(f'with a distance limit of: {distance_limit}')
    for index, individual in enumerate(hof):
        print(
            f'{index + 1}.\t{individual} points: {individual.fitness.values[0]}, distance: {individual.fitness.values[1]}')
