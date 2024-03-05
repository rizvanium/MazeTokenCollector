import random
import numpy
from deap import base, creator, tools, algorithms
from deap.tools import HallOfFame

toolbox = base.Toolbox()

creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create('Individual', list, fitness=creator.FitnessMulti)


def solve_for_max_profit(
        graph,
        starting_node_id,
        distance_limit,
        population_size=10_000,
        generation_size=30
) -> tuple[HallOfFame | None, bool]:
    toolbox.register(
        'attr_node_id',
        random.choice,
        list(graph.nodes())
    )

    if graph is None:
        return None, False

    if not isinstance(starting_node_id, int) or not isinstance(distance_limit, int):
        return None, False

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
    toolbox.register("mutate", mutate_path_length, available_nodes=list(graph.nodes()), add_prob=1.0)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)

    population = toolbox.population(n=population_size)
    hof = tools.HallOfFame(10)

    algorithms.eaSimple(
        population,
        toolbox,
        cxpb=0.5,
        mutpb=0.5,
        ngen=generation_size,
        halloffame=hof,
        verbose=True,
        stats=stats
    )

    return hof, True
