from multiprocessing import Pool, cpu_count
from os import path

import numpy as np

from bootstrapmoney.model import Model
from graph import graph


def compute(random_seed):

    parameters = {
        "mating_rate": 0.3,
        "max_production": 30,
        "n_agents": 300,
        "n_generations": 5000,
        "n_periods_per_generation": 100,
        "p_mutation": 0.1,
        "production_difficulty": [8, 8, 0.1],
        "production_costs": [5, 5, 5],
        "random_seed": random_seed,
        "utility": 200,
        "exchange_cost": 0,
        "p_direct": 0.4
    }

    m = Model(parameters)

    return parameters, m.run()


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
