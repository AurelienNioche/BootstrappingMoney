import numpy as np
from hyperopt import fmin, tpe, hp

from bootstrapmoney.economy import Economy


def fun(args):

    n_periods_per_generation = int(args[0])
    random_seed = np.random.randint(4294967295)
    # random_seed = 4043318547

    parameters = {
        "random_seed": random_seed,
        "n_generations": 50,
        "n_periods_per_generation": n_periods_per_generation,
        "n_goods": 3,
        "n_agents": 1000,
        "p_mutation": 0.05
    }

    e = Economy(**parameters)

    backup = e.run()

    return np.mean(backup["production_diversity"][-10:])


def main():

    space = [hp.quniform('x', 10, 15, 1)]

    best = fmin(
        fn=fun,
        space=space,
        algo=tpe.suggest,
        max_evals=50
    )
    print(best)


if __name__ == "__main__":

    main()
