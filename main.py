import numpy as np
from economy import Economy
from graph import graph


def main():

    random_seed = np.random.randint(4294967295)
    # random_seed = 1684517814

    parameters = {
        "random_seed": random_seed,
        "n_generations": 5000,
        "n_periods_per_generation": 15,
        "n_goods": 4,
        "n_agents": 40,
        "p_mutation": 0.1,
        "mating_rate": 0.3
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
