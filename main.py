import numpy as np
from economy import Economy
from graph import graph


def main():

    random_seed = np.random.randint(4294967295)
    # random_seed = 4043318547

    parameters = {
        "random_seed": random_seed,
        "n_generations": 200,
        "n_periods_per_generation": 50,
        "n_goods": 3,
        "n_agents": 500,
        "p_mutation": 0.01
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
