import numpy as np
from bootstrapmoney import Model
from graph import graph


def main():

    random_seed = np.random.randint(2320602665)

    parameters = {
        "random_seed": random_seed,
        "n_generations": 300,
        "n_periods_per_generation": 50,
        "n_goods": 3,
        "n_agents": 300,
        "p_mutation": 0.01,
        "mating_rate": 0.5,
        "production_costs": [0.9, 0.6, 0.3],
        "production_difficulty": [1, 1/2, 1/4],
        "max_production": 50,
        "utility": 1
        # "random_seed"  : random_seed,
        # "n_generations": 5000,
        # "n_periods_per_generation": 10,
        # "n_goods"      : 3,
        # "n_agents"     : 50,
        # "p_mutation"   : 0.4,
        # "mating_rate"  : 0.2,
        # "production_costs": [0.9, 0.6, 0.3],
        # "production_difficulty": [1, 1/2, 1/4],
        # "max_production": 10,
        # "utility"       : 1
    }

    model = Model(parameters)

    model.run()
    graph(results=model.history.history, parameters=parameters)

if __name__ == "__main__":

    main()
