from random_variable.random_variable import simulate

# List of mosquito types based on stage, sex, fertility, and mating status.
MOSQUITO_TYPE = ([(stage, male, 1, 0) for stage in ["Egg", "Larva", "Pupa"] for male in [1, 0]] +
                 [("Adult", 1, 1, 0), ("Adult", 0, 1, 0), ("Adult", 1, 0, 0), ("Adult", 0, 0, 0), ("Adult", 0, 0, 1)])

# List of names corresponding to each type in MOSQUITO_TYPE.
MOSQUITO_NAME = ["Male Egg", "Female Egg", "Male Larva", "Female Larva", "Male Pupa", "Female Pupa",
                 "Fertile Male Adult", "Fertile Female Adult", "Sterile Male Adult", "Sterile Female Adult",
                 "Mated Female Adult"]

def type_to_name(mosquito_type):
    """
    Convert a mosquito type tuple to its corresponding name.

    :param mosquito_type: Tuple representing the mosquito type.
    :type mosquito_type: tuple
    :return: The name corresponding to the mosquito type.
    :rtype: str
    """
    return MOSQUITO_NAME[MOSQUITO_TYPE.index(mosquito_type)]

def name_to_type(name):
    """
    Convert a mosquito name to its corresponding type tuple.

    :param name: The name of the mosquito.
    :type name: str
    :return: Tuple representing the mosquito type.
    :rtype: tuple
    """
    return MOSQUITO_TYPE[MOSQUITO_NAME.index(name)]

class Mosquito:
    """
    Base class representing a mosquito with various attributes.

    :param patch: The patch (location) where the mosquito is situated.
    :type patch: Patch
    :param age: The age of the mosquito.
    :type age: int
    :param male: Boolean indicating if the mosquito is male.
    :type male: bool
    :param lifespan_dist: Distribution parameters for the mosquito's lifespan.
    :type lifespan_dist: dict
    :param maturing_age_dist: Distribution parameters for the mosquito's maturing age.
    :type maturing_age_dist: dict
    :param fertile: Boolean indicating if the mosquito is fertile, defaults to True.
    :type fertile: bool, optional
    :param mated: Boolean indicating if the mosquito is mated, defaults to False.
    :type mated: bool, optional
    """
    def __init__(self, patch, age, male, duration_dist, survival_rate, fertile=True, mated=False):
        self.__patch = patch
        self.__age = age
        self.__male = male
        self.__duration = simulate(duration_dist["dist"], duration_dist["params"])
        self.__survive = simulate("bernoulli", [survival_rate])
        self.__fertile = fertile
        self.__mated = mated
        self.__nb_eggs = 0

    @property
    def nb_eggs(self):
        return self.__nb_eggs
    
    @nb_eggs.setter
    def nb_eggs(self, value):
        self.__nb_eggs = value

    @property
    def patch(self):
        """
        Get the patch (location) where the mosquito is situated.

        :return: The patch.
        :rtype: Patch
        """
        return self.__patch

    @patch.setter
    def patch(self, value):
        """
        Set the patch (location) where the mosquito is situated.

        :param value: The new patch.
        :type value: Patch
        """
        self.__patch = value

    @property
    def age(self):
        """
        Get the age of the mosquito.

        :return: The age.
        :rtype: int
        """
        return self.__age

    @property
    def male(self):
        """
        Check if the mosquito is male.

        :return: True if male, False otherwise.
        :rtype: bool
        """
        return self.__male

    @property
    def female(self):
        """
        Check if the mosquito is female.

        :return: True if female, False otherwise.
        :rtype: bool
        """
        return not self.__male

    @property
    def fertile(self):
        """
        Check if the mosquito is fertile.

        :return: True if fertile, False otherwise.
        :rtype: bool
        """
        return self.__fertile

    @property
    def mated(self):
        """
        Check if the mosquito is mated.

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
    Class representing the egg stage of a mosquito.

    :param patch: The patch where the egg is located.
    :type patch: Patch
    :param male: Boolean indicating if the egg will hatch into a male mosquito.
    :type male: bool
    """
    def __init__(self, patch, male, config):
        super().__init__(patch=patch, age=0, male=male, duration_dist=config["egg"]["duration"], survival_rate=config["egg"]["survival_rate"])
        self.__config = config

    def grow_old(self, dt):
        """
        Age the egg by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if not self._Mosquito__survive:
            return self, False
        if self._Mosquito__age > self._Mosquito__duration:
            return Larva(patch=self._Mosquito__patch, male=self._Mosquito__male, config=self.__config), True
        return self, True

class Larva(Mosquito):
    """
    Class representing the larva stage of a mosquito.

    :param patch: The patch where the larva is located.
    :type patch: Patch
    :param age: The age of the larva.
    :type age: int
    :param male: Boolean indicating if the larva is male.
    :type male: bool
    """
    def __init__(self, patch, male, config):
        super().__init__(patch=patch, age=0, male=male, duration_dist=config["larva"]["duration"], survival_rate=config["larva"]["survival_rate"])
        self.__config = config

    def grow_old(self, dt):
        """
        Age the larva by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if not self._Mosquito__survive: 
            return self, False
        if self._Mosquito__age > self._Mosquito__duration:
            return Pupa(patch=self._Mosquito__patch,  male=self._Mosquito__male, config=self.__config), True
        return self, True

class Pupa(Mosquito):
    """
    Class representing the pupa stage of a mosquito.

    :param patch: The patch where the pupa is located.
    :type patch: Patch
    :param age: The age of the pupa.
    :type age: int
    :param male: Boolean indicating if the pupa is male.
    :type male: bool
    """
    def __init__(self, patch, male, config):
        super().__init__(patch=patch, age=0, male=male, duration_dist=config["pupa"]["duration"], survival_rate=config["pupa"]["survival_rate"])
        self.__config = config

    def grow_old(self, dt):
        """
        Age the pupa by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current or new stage of the mosquito and a boolean indicating if it is alive.
        :rtype: tuple
        """
        self._Mosquito__age += dt
        if not self._Mosquito__survive:
            return self, False
        if self._Mosquito__age > self._Mosquito__duration:
            return Adult(patch=self._Mosquito__patch, age=0, male=self._Mosquito__male, fertile=True, config=self.__config), True
        return self, True

class Adult(Mosquito):
    """
    Class representing the adult stage of a mosquito.

    :param patch: The patch where the adult is located.
    :type patch: Patch
    :param age: The age of the adult.
    :type age: int
    :param male: Boolean indicating if the adult is male.
    :type male: bool
    :param fertile: Boolean indicating if the adult is fertile.
    :type fertile: bool
    """
    def __init__(self, patch, age, male, fertile, config):
        lifespan_key = ["female adult", "male adult", "sterile male adult"][male + (not fertile)]
        super().__init__(patch, age, male, config[lifespan_key]["lifespan"], config["egg"]["survival_rate"], fertile=fertile)
        self.__cycle_number = 0
        self.__next_cycle = simulate(config["female adult"]["first blood"]["dist"], config["female adult"]["first blood"]["params"])
        self.__config = config

    def grow_old(self, dt):
        """
        Age the adult by a given time increment.

        :param dt: The time increment.
        :type dt: int
        :return: A tuple containing the current stage of the mosquito, a boolean indicating if it is alive,
                 and a boolean indicating if it lays eggs.
        :rtype: tuple
        """

        self._Mosquito__age += dt
        if self._Mosquito__age > self._Mosquito__duration:
            return self, False, False
        if (not self._Mosquito__male and self.__cycle_number < self.__config["female adult"]["mate"]["max cycle"]
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
        dist = self.__config["female adult"]["mate"]["next cycle"]
        self.__next_cycle = self._Mosquito__age + simulate(dist["dist"], dist["params"])
