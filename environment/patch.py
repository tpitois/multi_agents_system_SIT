import random

import numpy as np


class Patch(object):
    """
    This class represents a patch in the environment where mosquitoes reside.

    :param mating_rate: The rate at which mosquitoes mate in this patch.
    :type mating_rate: float
    :param migration_rates: The rates at which mosquitoes migrate to other patches.
    :type migration_rates: list of float
    """

    def __init__(self, mating_rate, migration_rates, capacity):
        """
        Constructor.

        :param mating_rate: The rate at which mosquitoes mate in this patch.
        :type mating_rate: float
        :param migration_rates: The rates at which mosquitoes migrate to other patches.
        :type migration_rates: list of float
        """
        self.__mating_rate = mating_rate
        self.__migration_rates = migration_rates
        self.__capacity = capacity
        self.__cum_migration_rates = np.cumsum(self.__migration_rates)
        self.__mosquitoes = {}

    def add_mosquito(self, mosquito):
        """
        Add a mosquito to the patch.

        :param mosquito: Mosquito to add.
        :type mosquito: Mosquito
        """
        mosquito_type = (mosquito.stage(), mosquito.male, mosquito.fertile, mosquito.mated)
        if mosquito_type not in self.__mosquitoes:
            self.__mosquitoes[mosquito_type] = 0
        self.__mosquitoes[mosquito_type] += 1

    def remove_mosquito(self, mosquito):
        """
        Remove a mosquito from the patch.

        :param mosquito: Mosquito to remove.
        :type mosquito: Mosquito
        """
        mosquito_type = (mosquito.stage(), mosquito.male, mosquito.fertile, mosquito.mated)
        self.__mosquitoes[mosquito_type] -= 1

    def get_mosquitoes_number(self, mosquito_type):
        """
        Get the number of mosquitoes of a specific type in the patch.

        :param mosquito_type: Type of mosquito to count.
        :type mosquito_type: tuple
        :return: Number of mosquitoes of the specified type.
        :rtype: int
        """
        if mosquito_type in self.__mosquitoes:
            return self.__mosquitoes[mosquito_type]
        return 0

    def is_fertile_partner(self):
        """
        Check if there is a fertile partner available in the patch.

        :return: True if a fertile partner is available, False otherwise.
        :rtype: bool
        """
        male_number = (self.get_mosquitoes_number(("Adult", True, True, False))
                       + self.get_mosquitoes_number(("Adult", True, False, False)))

        return random.uniform(0, male_number) < self.get_mosquitoes_number(("Adult", True, True, False))

    @property
    def migration_rates(self):
        """
        Get the migration rates for this patch.

        :return: Migration rates.
        :rtype: list of float
        """
        return self.__migration_rates

    @property
    def mating_rate(self):
        """
        Get the mating rate for this patch.

        :return: Mating rate.
        :rtype: float
        """
        return self.__mating_rate

    @property
    def capacity(self):
        return self.__capacity

    def random_destination(self):
        """
        Get a random destination patch based on migration rates.

        :return: Index of the destination patch.
        :rtype: int
        """
        id_destination = 0
        r = random.random()
        while self.__cum_migration_rates[id_destination] < r:
            id_destination += 1
        return id_destination