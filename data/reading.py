import json
import pandas as pd

config = {}

def read_config(filename="example/config.json"):
    """
    Read the configuration from a JSON file.

    This function reads the configuration from a specified JSON file and stores it in the global `config` variable.

    :param filename: Path to the JSON configuration file, defaults to "example/config.json".
    :type filename: str, optional
    :return: Dictionary containing the configuration.
    :rtype: dict
    """
    with open(filename) as f:
        global config
        config = json.load(f)
        return config

def get_config():
    """
    Get the current configuration.

    This function returns the current configuration stored in the global `config` variable.

    :return: Dictionary containing the configuration.
    :rtype: dict
    """
    return config

def read_init_mosquitoes(filename):
    """
    Read the initial mosquitoes from a CSV file and create mosquito objects.

    This function reads the initial mosquitoes from a specified CSV file and creates mosquito objects based on the data.

    :param filename: Path to the CSV file containing the initial mosquitoes.
    :type filename: str
    :return: List of mosquito objects.
    :rtype: List[Mosquito]
    """
    import agents.mosquito
    mosquitoes = []
    df = pd.read_csv(filename)
    for mosquito_name, numbers in df.items():
        type = agents.mosquito.name_to_type(mosquito_name)
        mosquito_class = getattr(agents.mosquito, type[0])
        params = list(type[1:mosquito_class.__init__.__code__.co_argcount-1])
        for patch, number in enumerate(numbers):
            mosquitoes += [mosquito_class(*([patch]+params)) for _ in range(int(number))]
    return mosquitoes
