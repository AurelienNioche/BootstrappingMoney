import numpy as np
from pylab import plt
from os import path


def get_fig_name(name, folder="~/Desktop/"):

    fig_name = path.expanduser("{}{}.pdf".format(folder, name))

    init_fig_name = fig_name.split(".")[0]
    i = 2
    while path.exists(fig_name):
        fig_name = "{}{}.pdf".format(init_fig_name, i)
        i += 1

    return fig_name


def plot(results, parameters, fig_name):

    # What is common to all subplots
    fig = plt.figure(figsize=(25, 12))
    fig.patch.set_facecolor('white')

    n_lines = 2
    n_columns = 3

    # 1rst subplot

    x_max = len(results["exchanges"])
    x = range(x_max)

    ax = plt.subplot(n_lines, n_columns, 1)
    ax.set_title("Proportion of each type of exchange\naccording to time \n")

    type_of_exchanges = sorted([i for i in results["exchanges"][0].keys()])
    y = []
    for i in range(len(type_of_exchanges)):
        y.append([])

    for i in range(x_max):

        for exchange_idx in range(len(type_of_exchanges)):

            y[exchange_idx].append(results["exchanges"][i][type_of_exchanges[exchange_idx]])

    ax.set_ylim([-0.02, 1.02])

    for exchange_idx in range(len(type_of_exchanges)):

        ax.plot(x, y[exchange_idx], label="Exchange {}".format(type_of_exchanges[exchange_idx]), linewidth=2)

    ax.legend()

    # 2nd subplot: FITNESS TLNNJZLJKNTZLJKNVZ
    x = range(len(results["fitness"]))
    y = results["fitness"]

    ax = plt.subplot(n_lines, n_columns, 2)
    ax.set_title("Fitness average according to time \n")
    ax.plot(x, y, linewidth=2)

    # 3rd subplot: NUMBER OF EXCHANGES
    x = range(len(results["n_exchanges"]))
    y = results["n_exchanges"]

    ax = plt.subplot(n_lines, n_columns, 3)
    ax.set_title("Total number of exchanges according to time \n")
    ax.plot(x, y, linewidth=2)

    # 4rd subplot: NUMBER OF EXCHANGES
    x = range(len(results["n_market_agents"]))
    y = results["n_market_agents"]

    ax = plt.subplot(n_lines, n_columns, 4)
    ax.set_title("Total number of agents frequenting market \n")
    ax.plot(x, y, linewidth=2)

    # 5th subplot: DIVERSITY OF PRODUCTION
    x = range(len(results["production_diversity"]))
    y = results["production_diversity"]

    ax = plt.subplot(n_lines, n_columns, 5)
    ax.set_title("Production diversity according to time \n")
    ax.plot(x, y, linewidth=2)

    # 5th subplot: PARAMETERS
    ax = plt.subplot(n_lines, n_columns, 6)
    ax.set_title("Parameters")
    ax.axis('off')

    msg = ""
    for key in sorted(parameters.keys()):
        msg += "{}: {}; \n\n".format(key, parameters[key])

    ax.text(0.5, 0.5, msg, ha='center', va='center', size=12)

    plt.savefig(fig_name)

    plt.close()


def graph(results, parameters):

    fig_name = get_fig_name(name="MoneyBootstrapping_main_fig")
    plot(results, parameters, fig_name)
