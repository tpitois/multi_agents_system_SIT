import numpy as np
import pandas as pd

class Control:
    """
    This class represents a control strategy for adding mosquitoes to the environment.

    :param N: Number of patches.
    :type N: int
    :param T: Total time period.
    :type T: int
    :param dt: Time step.
    :type dt: int
    """

    def __init__(self, N, T, dt):
        """
        Constructor.

        :param N: Number of patches.
        :type N: int
        :param T: Total time period.
        :type T: int
        :param dt: Time step.
        :type dt: int
        """
        self.__N = N
        self.__T = T
        self.__dt = dt
        self.__nt = int(T / dt) + 1
        self.__control = np.zeros((self.__nt, N))

    def read(self, filename):
        """
        Read the control strategy from a CSV file.

        :param filename: Path to the CSV file containing the control strategy.
        :type filename: str
        """
        self.__control = pd.read_csv(filename).set_index('Time').values

    def get_mosquitoes(self, time, mosquito_class):
        """
        Get the list of mosquitoes to be added at a specific time based on the control strategy.

        :param time: The current time step.
        :type time: int
        :param mosquito_class: The class of mosquitoes to be added.
        :type mosquito_class: class
        :return: List of mosquitoes to be added.
        :rtype: List[Mosquito]
        """
        mosquitoes = []
        for i in range(self.__N):
            mosquitoes += [mosquito_class(i, 0, True, False) for _ in range(int(self.__control[time, i]))]
        return mosquitoes
