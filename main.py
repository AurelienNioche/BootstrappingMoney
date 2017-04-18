import numpy as np
from economy import Economy
from graph import graph
from multiprocessing import Pool, cpu_count


def compute(random_seed):

    parameters = {
        "random_seed": random_seed,
        "n_generations": 300,
        "n_periods_per_generation": 50,
        "n_goods": 3,
        "n_agents": 300,
        "p_mutation": 0.01,
        "mating_rate": 0.5,
        "production_costs": [0.9, 0.6, 0.3],
        "production_advantages": [1, 1/2, 1/4],
        "max_production": 50,
        "u": 1
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters, root_name="MoneyBootstrappingProductionCost")


def main():

    random_seeds = np.random.randint(2320602665, size=cpu_count())

    pool = Pool(processes=cpu_count())
    pool.map(compute, random_seeds)


if __name__ == "__main__":

    main()
