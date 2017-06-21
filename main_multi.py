import numpy as np
from multiprocessing import cpu_count, Pool
from os import path

from bootstrapmoney import Model
from graph import graph


def compute(random_seed):

    parameters = {
        "mating_rate": 0.3,
        "max_production": 10,
        "n_agents": 300,
        "n_generations": 10**4,
        "n_goods": 3,
        "n_periods_per_generation": 5,
        "p_mutation": 0.1,
        "production_difficulty": [4, 2, 0.5],
        "production_costs": [4, 2, 2],
        "random_seed": random_seed,
        "utility": 10
    }

    model = Model(parameters)

    model.run()
    return parameters, model.history.history


def main():

    random_seeds = np.random.randint(2320602665, size=cpu_count())

    pool = Pool(processes=cpu_count())

    results = pool.map(compute, random_seeds)

    for parameters, backup in results:
        print("Do graph.")
        graph(results=backup, parameters=parameters,
              root_folder=path.expanduser("~/Desktop/MoneyBootstrapping"), root_name="MB")


if __name__ == "__main__":

    main()
