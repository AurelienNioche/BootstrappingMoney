from os import path

import numpy as np

from bootstrapmoney import model
from graph import graph

random_seed = np.random.randint(460741801)

parameters = {
    "mating_rate": 0.3,
    "max_production": 10,
    "n_agents": 300,
    "n_generations": 5000,
    "n_periods_per_generation": 5,
    "p_mutation": 0.1,
    "production_difficulty": [4, 4, 4, 4, 0.5],
    "production_costs": [4, 2, 2, 2, 2],
    "random_seed": random_seed,
    "utility": 20,
    "exchange_cost": 2,
    "p_direct": 0.4
}

e = model.Model(parameters)

backup = e.run()
graph(results=backup, parameters=parameters, root_name="MB",
      root_folder=path.expanduser("~/Desktop/MoneyBootstrapping"))
