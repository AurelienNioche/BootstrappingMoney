from economy import Economy
from graph import graph

from os import path


random_seed = 460741801

parameters = {
    "random_seed": random_seed,
    "n_generations": 500,
    "n_periods_per_generation": 50,
    "n_goods": 3,
    "n_agents": 300,
    "p_mutation": 0.01,
    "mating_rate": 0.5,
    "production_costs": [2, 1.5, 1],
    "production_advantages": [1, 1 / 2, 1 / 100],
    "max_production": 50,
    "u": 1
}

e = Economy(**parameters)

backup = e.run()
graph(results=backup, parameters=parameters, root_name="MB",
      root_folder=path.expanduser("~Desktop/MoneyBootstrapping"))