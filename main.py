import numpy as np
from bootstrapmoney import Economy
from graph import graph


def main():

    random_seed = np.random.randint(2320602665)

    parameters = {
        "random_seed": random_seed,
        "n_generations": 5000,
        "n_periods_per_generation": 10,
        "n_goods": 3,
        "n_agents": 50,
        "p_mutation": 0.4,
        "mating_rate": 0.2
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
