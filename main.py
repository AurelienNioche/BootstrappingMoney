from economy import Economy
from graph import graph


def main():

    parameters = {
        "n_generations": 200,
        "n_periods_per_generation": 100,
        "n_goods": 3,
        "n_agents": 200,
        "reproduction_proportion": 0.01,
        "p_mutation": 0.01
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
