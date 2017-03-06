import numpy as np
from economy import Economy
from graph import graph


def main():

    # random_seed = np.random.randint(4294967295)
    random_seed = 1684517814

    parameters = {
        "random_seed": random_seed,
        "n_generations": 10000,
        "n_periods_per_generation": 12,
        "n_goods": 4,
        "n_agents": 150,
        "p_mutation": 0.1,
        "mating_rate": 0.2
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
