from scipy import stats
from data.reading import get_config

MOSQUITO_TYPE = ([(stage, male, 1, 0) for stage in ["Egg", "Larva", "Pupa"] for male in [1, 0]] +
                 [("Adult", 1, 1, 0), ("Adult", 0, 1, 0), ("Adult", 1, 0, 0), ("Adult", 0, 0, 0), ("Adult", 0, 0, 1)])
MOSQUITO_NAME = ["Male Egg", "Female Egg", "Male Larva", "Female Larva", "Male Pupa", "Female Pupa",
                 "Fertile Male Adult", "Fertile Female Adult", "Sterile Male Adult", "Sterile Female Adult",
                 "Mated Female Adult"]

def type_to_name(type):
    """
    Convert a mosquito type to its corresponding name.

    :param type: Mosquito type.
    :type type: tuple
    :return: Mosquito name.
    :rtype: str
    """
    return MOSQUITO_NAME[MOSQUITO_TYPE.index(type)]

def name_to_type(name):
    """
    Convert a mosquito name to its corresponding type.

    :param name: Mosquito name.
    :type name: str
    :return: Mosquito type.
    :rtype: tuple
    """
    return MOSQUITO_TYPE[MOSQUITO_NAME.index(name)]

config = get_config()

class Mosquito(object):
    """
    Base class for representing a mosquito.

    :param patch: The patch where the mosquito is located.
    :type patch: Patch
    :param age: The age of the mosquito.
    :type age: int
    :param male: Whether the mosquito is male.
    :type male: bool
    :param lifetime_dist: Distribution parameters for the mosquito's lifetime.
    :type lifetime_dist: dict
    :param maturing_age_dist: Distribution parameters for the mosquito's maturing age.
    :type maturing_age_dist: dict
    :param fertile: Whether the mosquito is fertile, defaults to True.
    :type fertile: bool, optional
    :param mated: Whether the mosquito is mated, defaults to False.
    :type mated: bool, optional
    """
    def __init__(self, patch, age, male, lifetime_dist, maturing_age_dist=config["egg"]["maturing_age"],
                 fertile=True, mated=False):
        self.__patch = patch
        self.__age = age
        self.__male = male
        self.__lifetime = getattr(stats, lifetime_dist["dist"]).rvs(*lifetime_dist["params"])
        self.__maturing_age = getattr(stats, maturing_age_dist["dist"]).rvs(*maturing_age_dist["params"])
        self.__fertile = fertile
        self.__mated = mated

    @property
    def patch(self):
        """
        The patch where the mosquito is located.

        :return: The patch.
        :rtype: Patch
        """
        return self.__patch

    @patch.setter
    def patch(self, value):
        """
        Set the patch where the mosquito is located.

        :param value: The new patch.
        :type value: Patch
        """
        self.__patch = value

    @property
    def age(self):
        """
        The age of the mosquito.

        :return: The age.
        :rtype: int
        """
        return self.__age

    @property
    def male(self):
        """
        Whether the mosquito is male.

        :return: True if male, False otherwise.
        :rtype: bool
        """
        return self.__male

    @property
    def female(self):
        """
        Whether the mosquito is female.

        :return: True if female, False otherwise.
        :rtype: bool
        """
        return not self.__male

    @property
    def fertile(self):
        """
        Whether the mosquito is fertile.

        :return: True if fertile, False otherwise.
        :rtype: bool
        """
        return self.__fertile

    @property
    def mated(self):
        """
        Whether the mosquito is mated.

        :return: True if mated, False otherwise.
        :rtype: bool
        """
        return self.__mated

    def stage(self):
        """
        Get the current stage of the mosquito.

        :return: The stage name.
        :rtype: str
        """
        return self.__class__.__name__

class Egg(Mosquito):
    """
    Class representing an egg stage of a mosquito.

    :param patch: The patch where the egg is located.
    :type patch: Patch
    :param male: Whether the egg will hatch into a male mosquito.
    :type male: bool
    """
    def __init__(self, patch, male):
        super().__init__(patch, 0, male, config["egg"]["lifetime"], config["egg"]["maturing_age"])

    def grow_old(self, dt):
        """
        Age the egg by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if self._Mosquito__age > self._Mosquito__lifetime:
            return self, False
        if self._Mosquito__age > self._Mosquito__maturing_age:
            return Larva(self._Mosquito__patch, self._Mosquito__age, self._Mosquito__male), True
        return self, True

class Larva(Mosquito):
    """
    Class representing a larva stage of a mosquito.

    :param patch: The patch where the larva is located.
    :type patch: Patch
    :param age: The age of the larva.
    :type age: int
    :param male: Whether the larva is male.
    :type male: bool
    """
    def __init__(self, patch, age, male):
        super().__init__(patch, age, male, config["larva"]["lifetime"], config["larva"]["maturing_age"])

    def grow_old(self, dt):
        """
        Age the larva by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if self._Mosquito__age > self._Mosquito__lifetime:
            return self, False
        if self._Mosquito__age > self._Mosquito__maturing_age:
            return Pupa(self._Mosquito__patch, self._Mosquito__age, self._Mosquito__male), True
        return self, True

class Pupa(Mosquito):
    """
    Class representing a pupa stage of a mosquito.

    :param patch: The patch where the pupa is located.
    :type patch: Patch
    :param age: The age of the pupa.
    :type age: int
    :param male: Whether the pupa is male.
    :type male: bool
    """
    def __init__(self, patch, age, male):
        super().__init__(patch, age, male, config["pupa"]["lifetime"], config["pupa"]["maturing_age"])

    def grow_old(self, dt):
        """
        Age the pupa by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if self._Mosquito__age > self._Mosquito__lifetime:
            return self, False
        if self._Mosquito__age > self._Mosquito__maturing_age:
            return Adult(self._Mosquito__patch, self._Mosquito__age, self._Mosquito__male, True), True
        return self, True

class Adult(Mosquito):
    """
    Class representing an adult stage of a mosquito.

    :param patch: The patch where the adult is located.
    :type patch: Patch
    :param age: The age of the adult.
    :type age: int
    :param male: Whether the adult is male.
    :type male: bool
    :param fertile: Whether the adult is fertile.
    :type fertile: bool
    """
    def __init__(self, patch, age, male, fertile):
        super().__init__(patch, age, male, config[["female adult", "male adult"][male]]["lifetime"], fertile=fertile)
        self.__cycle_number = 0
        self.__next_cycle = 0

    def grow_old(self, dt):
        """
        Age the adult by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current stage of the mosquito, a boolean indicating if it is alive and
        a boolean indicating if it lays eggs.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if self._Mosquito__age > self._Mosquito__lifetime:
            return self, False, False
        if (not self._Mosquito__male and self.__cycle_number < config["female adult"]["mate"]["max cycle"]
                and self.__next_cycle - dt < self._Mosquito__age < self.__next_cycle + dt):
            self.__new_cycle()
            return self, True, True
        return self, True, False

    def become_sterile(self, patch):
        """
        Make the adult mosquito sterile.

        :param patch: The patch where the mosquito is located.
        :type patch: Patch
        """
        patch.remove_mosquito(self)
        self._Mosquito__fertile = False
        patch.add_mosquito(self)

    def become_mated(self, patch):
        """
        Mark the adult mosquito as mated.

        :param patch: The patch where the mosquito is located.
        :type patch: Patch
        """
        patch.remove_mosquito(self)
        self.__new_cycle()
        self._Mosquito__mated = True
        patch.add_mosquito(self)

    def __new_cycle(self):
        """
        Start a new cycle for the adult mosquito.
        """
        self.__cycle_number += 1
        dist = config["female adult"]["mate"]["next cycle"]
        self.__next_cycle = self._Mosquito__age + getattr(stats, dist["dist"]).rvs(*dist["params"])
