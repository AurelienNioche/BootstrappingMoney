import numpy as np
from pylab import plt
from os import path


class GraphicDesigner(object):

    def __init__(self, backup, parameters):

        self.exchanges_list = backup["exchanges"]
        self.fitness_list = backup["fitness"]
        self.n_exchanges_list = backup["n_exchanges"]

        self.parameters = parameters

        self.main_figure_name = self.get_fig_name(name="MoneyBootstrapping_main_fig")

    @staticmethod
    def get_fig_name(name, folder="~/Desktop/"):

        fig_name = path.expanduser("{}{}.pdf".format(folder, name))

        init_fig_name = fig_name.split(".")[0]
        i = 2
        while path.exists(fig_name):
            fig_name = "{}{}.pdf".format(init_fig_name, i)
            i += 1

        return fig_name

    def plot_main_fig(self):

        # What is common to all subplots
        fig = plt.figure(figsize=(25, 12))
        fig.patch.set_facecolor('white')

        n_lines = 1
        n_columns = 4

        # 1rst subplot

        x_max = len(self.exchanges_list)
        x = range(x_max)

        ax = plt.subplot(n_lines, n_columns, 1)
        ax.set_title("Proportion of each type of exchange according to time \n")

        type_of_exchanges = sorted([i for i in self.exchanges_list[0].keys()])
        y = []
        for i in range(len(type_of_exchanges)):
            y.append([])

        for i in range(x_max):

            for exchange_idx in range(len(type_of_exchanges)):

                y[exchange_idx].append(self.exchanges_list[i][type_of_exchanges[exchange_idx]])

        ax.set_ylim([-0.02, 1.02])

        for exchange_idx in range(len(type_of_exchanges)):

            ax.plot(x, y[exchange_idx], label="Exchange {}".format(type_of_exchanges[exchange_idx]), linewidth=2)

        ax.legend()

        # 2nd subplot: FITNESS TLNNJZLJKNTZLJKNVZ
        x = range(len(self.fitness_list))
        y = self.fitness_list

        ax = plt.subplot(n_lines, n_columns, 2)
        ax.set_title("Fitness average according to time \n")
        ax.plot(x, y, linewidth=2)

        # 3rd subplot: NUMBER OF EXCHANGES
        x = range(len(self.n_exchanges_list))
        y = self.n_exchanges_list

        ax = plt.subplot(n_lines, n_columns, 3)
        ax.set_title("Total number of exchanges according to time \n")
        ax.plot(x, y, linewidth=2)

        # 4th subplot: PARAMETERS
        ax = plt.subplot(n_lines, n_columns, 4)
        ax.set_title("Parameters")
        ax.axis('off')

        msg = ""
        for key in sorted(self.parameters.keys()):
            msg += "{}: {}; \n\n".format(key, self.parameters[key])

        ax.text(0.5, 0.5, msg, ha='center', va='center', size=12)

        plt.savefig(self.main_figure_name)

        plt.close()


def graph(backup, parameters):

    g = GraphicDesigner(backup=backup, parameters=parameters)
    g.plot_main_fig()
