import numpy as np

from bootstrapmoney import model


def main():
    random_seed = np.random.randint(460741801)

    parameters = {
        "mating_rate": 0.3,
        "max_production": 10,
        "n_agents": 300,
        "n_generations": 20,
        "n_goods": 3,
        "n_periods_per_generation": 5,
        "p_mutation": 0.1,
        "production_difficulty": [4, 2, 0.5],
        "production_costs": [4, 2, 2],
        "random_seed": random_seed,
        "utility": 20
    }

    e = model.Model(parameters)

    e.run()

if __name__ == "__main__":

    main()
