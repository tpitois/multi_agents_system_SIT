import queue
import random
from typing import List, Optional, Tuple

from random_variable.random_variable import simulate
from agents.mosquito import MOSQUITO_TYPE, Mosquito, Egg, Adult, name_to_type
from environment.patch import Patch

class Environment:
    """
    This class represents the environment for a multi-agent system simulation.

    :param mosquitoes: List of mosquitoes in the environment.
    :type mosquitoes: List[Mosquito]
    :param patches: List of patches in the environment.
    :type patches: List[Patch]
    :param dt: Time step.
    :type dt: int
    """

    def __init__(self, mosquitoes: List[Mosquito], patches: List[Patch], dt: int):
        """
        Constructor.

        :param mosquitoes: List of mosquitoes in the environment.
        :type mosquitoes: List[Mosquito]
        :param patches: List of patches in the environment.
        :type patches: List[Patch]
        :param dt: Time step.
        :type dt: int
        """
        self.__time = 0
        self.__dt = dt
        self.__current_queue = 0
        self.__patches = patches
        self.__mosquitoes = [queue.Queue(), queue.Queue()]
        self.add_mosquitoes(mosquitoes)

    @property
    def time(self) -> int:
        """
        Get the current time in the environment.

        :return: Current time.
        :rtype: int
        """
        return self.__time

    def __add_mosquito(self, mosquito: Mosquito):
        """
        Add a mosquito to the environment.

        :param mosquito: Mosquito to add.
        :type mosquito: Mosquito
        """
        self.__mosquitoes[(self.__current_queue + 1) % 2].put(mosquito)
        self.__patches[mosquito.patch].add_mosquito(mosquito)

    def add_mosquitoes(self, mosquitoes: Optional[List[Mosquito]] = None):
        """
        Add a list of mosquitoes to the environment.

        :param mosquitoes: List of mosquitoes to add.
        :type mosquitoes: List[Mosquito], optional
        """
        if mosquitoes is None:
            mosquitoes = []
        for mosquito in mosquitoes:
            self.__add_mosquito(mosquito)

    def get_mosquito(self) -> Mosquito:
        """
        Get the next mosquito from the queue.

        :return: Next mosquito.
        :rtype: Mosquito
        """
        return self.__mosquitoes[self.__current_queue].get_nowait()

    def next_time(self):
        """
        Advance the environment time by one time step.
        """
        self.__time += self.__dt
        self.__current_queue = (self.__current_queue + 1) % 2

    def grow_old(self, mosquito: Mosquito, config: dict) -> Tuple[Optional[Mosquito], bool]:
        """
        Age the mosquito by one time step and make it lay eggs or not.

        :param mosquito: Mosquito to age.
        :type mosquito: Mosquito
        :param config: Configuration dictionary containing parameters for the simulation.
        :type config: dict
        :return: Tuple containing the new mosquito and a boolean indicating if it is alive.
        :rtype: Tuple[Optional[Mosquito], bool]
        """
        if mosquito.stage() == "Adult":
            new_mosquito, alive, lay_eggs = mosquito.grow_old(self.__dt)
        else:
            new_mosquito, alive = mosquito.grow_old(self.__dt)
            lay_eggs = False

        if not alive:
            self.__patches[mosquito.patch].remove_mosquito(mosquito)
            return None, False

        if lay_eggs:
            self.__lay_eggs(mosquito.patch, config)

        if new_mosquito.stage() != mosquito.stage():
            self.__patches[mosquito.patch].remove_mosquito(mosquito)
            self.__patches[new_mosquito.patch].add_mosquito(new_mosquito)
        return new_mosquito, True

    def mate(self, mosquito: Mosquito, config: dict):
        """
        Attempt to mate the mosquito.

        :param mosquito: Mosquito to mate.
        :type mosquito: Mosquito
        :param config: Configuration dictionary containing parameters for the simulation.
        :type config: dict
        """
        patch = self.__patches[mosquito.patch]
        if not (mosquito.stage() == "Adult" and mosquito.female and mosquito.fertile
                and random.random() < patch.mating_rate):
            return
        mosquito.become_sterile(patch)
        if patch.is_fertile_partner(config["sterile male adult"]["competitiveness"]):
            mosquito.become_mated(patch)

    def migrate(self, mosquito: Mosquito):
        """
        Attempt to migrate the mosquito to another patch.

        :param mosquito: Mosquito to migrate.
        :type mosquito: Mosquito
        """
        if mosquito.stage() != "Adult":
            self.__mosquitoes[(self.__current_queue + 1) % 2].put(mosquito)
            return

        id_destination = self.__patches[mosquito.patch].random_destination()
        if id_destination != mosquito.patch:
            self.__patches[mosquito.patch].remove_mosquito(mosquito)
            mosquito.patch = id_destination
            self.__patches[id_destination].add_mosquito(mosquito)
        self.__mosquitoes[(self.__current_queue + 1) % 2].put(mosquito)

    def get_populations(self) -> List[List[int]]:
        """
        Get the populations of mosquitoes in each patch.

        :return: List of populations in each patch.
        :rtype: List[List[int]]
        """
        return [[patch.get_mosquitoes_number(type) for type in MOSQUITO_TYPE] for patch in self.__patches]

    def __lay_eggs(self, patch: int, config: dict):
        """
        Lay eggs in the specified patch.

        :param patch: The patch where eggs will be laid.
        :type patch: int
        :param number_of_eggs_dist: Distribution parameters for the number of eggs.
        :type number_of_eggs_dist: dict
        """

        max_eggs = max(
            0,
            (self.__patches[patch].capacity -
             sum(self.__patches[patch].get_mosquitoes_number(name_to_type(name))
                 for name in ["Male Egg", "Female Egg"]))
        )

        number_of_eggs_dist = config["female adult"]["mate"]["number of eggs"]

        number_of_female_eggs = simulate(number_of_eggs_dist["female"]["dist"], number_of_eggs_dist["female"]["params"])
        number_of_male_eggs = simulate(number_of_eggs_dist["male"]["dist"], number_of_eggs_dist["male"]["params"])
        K = min(max_eggs / (number_of_female_eggs + number_of_male_eggs), 1)
        number_of_female_eggs *= K
        number_of_male_eggs *= K
        self.add_mosquitoes(
            [Egg(patch, False, config) for _ in range(int(number_of_female_eggs))]
            + [Egg(patch, True, config) for _ in range(int(number_of_male_eggs))]
        )

    def add_sterile_mosquitoes(self, control, config):
        """
        Add sterile mosquitoes to the environment based on the control strategy.

        :param control: Control strategy for adding sterile mosquitoes.
        :type control: Control
        """
        self.add_mosquitoes(control.get_mosquitoes(self.time, Adult, config))

    def empty_queue(self) -> bool:
        """
        Check if the current mosquito queue is empty.

        :return: True if the queue is empty, False otherwise.
        :rtype: bool
        """
        return self.__mosquitoes[self.__current_queue].empty()
