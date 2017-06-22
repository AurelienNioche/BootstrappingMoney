import numpy as np
from bootstrapmoney import Model
from graph import graph

from os import path


def main():

    random_seed = np.random.randint(2320602665)

    parameters = {
        "mating_rate": 0.3,
        "max_production": 10,
        "n_agents": 300,
        "n_generations": 100,
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
    graph(results=model.history.history, parameters=parameters,
          root_folder=path.expanduser("~/Desktop/MoneyBootstrapping"), root_name="MB")

if __name__ == "__main__":

    main()
