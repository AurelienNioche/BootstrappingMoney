import numpy as np
from economy import Economy
from graph import graph


def main():

    random_seed = np.random.randint(4294967295)

    parameters = {
        "random_seed": random_seed,
        "n_generations": 10000,
        "n_periods_per_generation": 100,
        "n_goods": 3,
        "n_agents": 200,
        "reproduction_proportion": 0.01,
        "p_mutation": 0.01
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
