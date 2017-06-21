from pylab import plt
from os import path, mkdir
import itertools as it
from datetime import datetime


def get_fig_name(root_folder=path.expanduser("~/Desktop/MoneyBootstrapping"), root_name="MB"):

    if not path.exists(root_folder):
        mkdir(root_folder)

    fig_name = "{}/{}_{}.pdf".format(root_folder, root_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

    return fig_name


def plot(results, parameters, fig_name):

    # What is common to all subplots
    fig = plt.figure(figsize=(25, 12))

    fig.patch.set_facecolor('white')

    line_width = 2

    n_lines = 3
    n_columns = 3

    counter = it.count(1)

    # ----- FOR EACH GENERATION ------ #

    # FITNESS

    x = range(len(results["fitness"]))
    y = results["fitness"]

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Fitness average\naccording to number of generations\n")
    ax.plot(x, y, linewidth=line_width)

    # PROPORTION OF EACH TYPE OF EXCHANGE

    x_max = len(results["exchanges"])
    x = range(x_max)

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Number of each type of exchange\naccording to number of generations\n")

    n_type_of_exchanges = len(results["exchanges_labels"])

    # ax.set_ylim([-0.02, 1.02])

    for exchange_idx in range(n_type_of_exchanges):

        ax.plot(x, results["exchanges"][:, exchange_idx],
                label="Exchange {}".format(results["exchanges_types"][exchange_idx]),
                linewidth=line_width)

    ax.legend(fontsize=8)

    # NUMBER OF EXCHANGES GENERATION

    x = range(len(results["n_exchanges"]))

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Total number of exchanges\naccording to number of generations\n")
    ax.plot(x, results["n_exchanges"], linewidth=line_width)

    # NUMBER OF INTERVENTION OF EACH GOOD

    n_goods = len(results["n_goods_intervention"][0, :])

    x_max = len(results["n_exchanges"])
    x = range(x_max)

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Number of interventions of each good\naccording to number of generations\n")

    for i in range(n_goods):

        ax.plot(x, results["n_goods_intervention"][:, i], label="Good {}".format(i), linewidth=line_width)

    ax.legend(fontsize=8)

    # DIVERSITY OF PRODUCTION

    x = range(len(results["production_diversity"]))

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Production diversity\naccording to number of generations\n")
    ax.plot(x, results["production_diversity"], linewidth=line_width)

    # N PRODUCERS

    n_goods = len(results["n_producers"][0])

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Number of producers for each good \n")

    for i in range(n_goods):
        y = [j[i] for j in results["n_producers"]]
        x = range(len(y))
        ax.plot(x, y, linewidth=line_width, label="Good {}".format(i))

    ax.legend(fontsize=8)

    # GLOBAL PRODUCTION

    n_goods = len(results["production"][0, :])

    x = range(len(results["production"][:]))

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Global production for each good \n")

    for i in range(n_goods):

        ax.plot(x, results["production"][:, i], linewidth=line_width, label="Good {}".format(i))

    ax.legend(fontsize=8)

    # ------ PARAMETERS ----- #

    # 5th subplot: PARAMETERS
    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Parameters")
    ax.axis('off')

    msg = ""
    for key in sorted(parameters.keys()):
        msg += "{}: {}; \n".format(key, parameters[key])

    ax.text(0.5, 0.5, msg, ha='center', va='center', size=12)

    plt.tight_layout()

    plt.savefig(fig_name)

    plt.close()


def graph(results, parameters, root_folder, root_name):

    fig_name = get_fig_name(root_folder=root_folder, root_name=root_name)
    plot(results, parameters, fig_name)
