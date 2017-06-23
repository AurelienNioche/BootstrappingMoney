from os import path, mkdir
import itertools as it
from datetime import datetime

# remove LAPACK/scipy harmless warning (see https://github.com/scipy/scipy/issues/5998)
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

from pylab import plt
import scipy.signal



def get_fig_name(root_folder=path.expanduser("~/Desktop/MoneyBootstrapping"), root_name="MB"):

    if not path.exists(root_folder):
        mkdir(root_folder)

    fig_name = "{}/{}_{}.pdf".format(root_folder, root_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

    return fig_name


def moving_average(ys, window=9, polyorder=1, mode='mirror'):
    return scipy.signal.savgol_filter(ys, window, polyorder, mode=mode)


def plot(results, parameters, fig_name):

    # What is common to all subplots
    fig = plt.figure(figsize=(25, 12))

    fig.patch.set_facecolor('white')

    line_width = 1

    n_lines = 3
    n_columns = 3

    counter = it.count(1)

    # ----- FOR EACH GENERATION ------ #

    # FITNESS

    x = range(len(results["fitness"]))
    y = results["fitness"]

    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Fitness average\naccording to number of generations\n")
    ax.plot(x, y, linewidth=line_width, alpha=0.25)
    #ax.plot(x, moving_average(y), linewidth=2*line_width, alpha=0.5)

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

    # ------ STRATEGIES ------ #

    # 6th subplot: STRATEGIES
    ax = plt.subplot(n_lines, n_columns, next(counter))
    ax.set_title("Strategies")

    # FIXME: move me somewhere else
    direct   = [sum([n_s for s_path, n_s in strategies_t.items() if len(s_path) == 1]) for strategies_t in results['n_strategies']]
    indirect0 = [sum([n_s for s_path, n_s in strategies_t.items() if len(s_path) == 2 and s_path[0][1] == 0]) for strategies_t in results['n_strategies']]
    indirect = [sum([n_s for s_path, n_s in strategies_t.items() if len(s_path) == 2 and s_path[0][1] != 0]) for strategies_t in results['n_strategies']]

    ax.plot(range(len(direct)),       direct, linewidth=line_width, label="Direct")
    ax.plot(range(len(indirect)),   indirect, linewidth=line_width, label="Indirect (no 0)")
    ax.plot(range(len(indirect0)), indirect0, linewidth=line_width, label="Indirect (zero)")
    ax.legend(fontsize=8)

    plt.tight_layout()

    plt.savefig(fig_name)

    plt.close()


def graph(results, parameters, root_folder, root_name):

    fig_name = get_fig_name(root_folder=root_folder, root_name=root_name)
    plot(results, parameters, fig_name)
