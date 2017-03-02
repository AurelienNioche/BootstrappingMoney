from economy import Economy
from graph import graph


def main():

    parameters = {
        "n_generations": 10,
        "n_periods_per_generation": 10,
        "n_goods": 10,
        "n_agents": 1000,
        "n_reproduction_pairs": 200,
        "p_mutation": 0.1
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(backup=backup, parameters=parameters)

if __name__ == "__main__":

    main()
