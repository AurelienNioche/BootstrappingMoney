import numpy as np
from economy import Economy


def main():

    random_seed = np.random.randint(4294967295)

    parameters = {
        "random_seed": random_seed,
        "n_generations": 100,
        "n_periods_per_generation": 30,
        "n_goods": 5,
        "n_agents": 100,
        "p_mutation": 0.1,
        "mating_rate": 0.3
    }

    e = Economy(**parameters)

    e.run()

if __name__ == "__main__":

    main()
