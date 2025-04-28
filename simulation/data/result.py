import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Result:
    """
    This class represents the result of a multi-agent system simulation.

    :param N: Number of patches.
    :type N: int
    :param T: Period.
    :type T: int
    :param dt: Time step.
    :type dt: int
    :param folder_name: Name of the folder where results are saved.
    :type folder_name: str
    """

    def __init__(self, N, T, dt, folder_name):
        """
        Constructor.

        :param N: Number of patches.
        :type N: int
        :param T: Period.
        :type T: int
        :param dt: Time step.
        :type dt: int
        :param folder_name: Name of the folder where results are saved.
        :type folder_name: str
        """
        self.__N = N
        self.__T = T
        self.__dt = dt
        self.__column_names = ["Egg", "Larva", "Pupa", "Fertile Male Adult", "Fertile Female Adult",
                               "Sterile Male Adult", "Sterile Female Adult", "Mated Female Adult"]
        self.__nt = int(T / dt) + 1
        self.__result = np.zeros((N, self.__nt, len(self.__column_names)))
        self.__t = 0
        self.__folder_name = folder_name
        os.makedirs(folder_name, exist_ok=True)

    def add_populations(self, populations):
        """
        Add populations at the end to this result.

        :param populations: List of population in a patch.
        :type populations: list of list of float
        :return: None
        """
        for i in range(self.__N):
            population = populations[i]
            for j in [0, 2, 4]:
                population[j] = population[j] + population[j + 1]
            self.__result[i, self.__t, :] = [population[j] for j in range(len(population)) if j not in [1, 3, 5]]
        self.__t += 1

    def write(self):
        """
        Save each patch result to a CSV file.

        :return: None
        """
        #os.makedirs(f"{self.__folder_name}/tables/", exist_ok=True)
        for i in range(self.__N):
            df = pd.DataFrame(self.__result[i], columns=self.__column_names)
            df["Time"] = pd.Series([self.__dt * k for k in range(self.__nt)])
            df.to_csv(f"{self.__folder_name}/{i:0{len(str(self.__N-1))}}.csv", index=False)

    def read(self, folder_name):
        """
        Read the results from CSV files in the specified folder.

        :param folder_name: The path of the folder where the results are saved.
        :type folder_name: str
        :return: None
        """
        with os.scandir(folder_name) as it:
            for entry in it:
                if entry.name.endswith(".csv") and entry.is_file():
                    self.__result[int(entry.name[:-4]), :, :] = pd.read_csv(entry.path).set_index("Time").values

    def draw(self):
        """
        Draw the results as a plot and save it as a PDF file.

        :return: None
        """
        rows = math.isqrt(self.__N)
        cols = math.ceil(self.__N / rows)
        fig, axs = plt.subplots(rows, cols, figsize=(15, 10), constrained_layout=False)
        axs = axs.flatten()
        time_interval = [self.__dt * k for k in range(self.__nt)]
        y_max = np.max(self.__result)
        for i in range(self.__N):
            for j in range(len(self.__column_names)):
                ax = axs[i]
                ax.plot(time_interval, self.__result[i, :, j], label=self.__column_names[j])
                ax.set_title(f"{i:0{len(str(self.__N))}}")
                ax.set_xlim(time_interval[0], time_interval[-1])
                ax.set_ylim(0, y_max)
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        handles, labels = axs[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=4)
        fig.savefig(f"{self.__folder_name}/graphs.pdf")
