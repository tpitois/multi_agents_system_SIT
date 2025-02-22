from environment.environment import Environment
from environment.patch import Patch
from data.result import Result
from data.control import Control
from data.reading import get_config, read_init_mosquitoes

import random

def run_simulation(init_mosquito_file="example/init_mosquitoes.csv", control_file="example/control.csv", folder_name="results"):
    """
    Run the multi-agent system simulation.

    This function initializes the environment, reads the initial mosquitoes and control strategy,
    and runs the simulation until the specified period is reached.

    :param init_mosquito_file: Path to the CSV file containing the initial mosquitoes, defaults to "example/init_mosquitoes.csv".
    :type init_mosquito_file: str, optional
    :param control_file: Path to the CSV file containing the control strategy, defaults to "example/control.csv".
    :type control_file: str, optional
    :param folder_name: Name of the folder where results are saved, defaults to "results".
    :type folder_name: str, optional
    """
    config = get_config()

    T = config["period"]
    dt = config["dt"]
    N = config["number_of_patches"]

    patches = [Patch(config["mating_rates"][i], config["migration_rates"][i]) for i in range(N)]
    mosquitoes = read_init_mosquitoes(init_mosquito_file)
    mosquitoes = random.sample(mosquitoes, len(mosquitoes))

    environment = Environment(mosquitoes, patches, dt)
    result = Result(N, T, dt, folder_name=folder_name)
    control = Control(N, T, dt)

    control.read(control_file)
    result.add_populations(environment.get_populations())

    while environment.time < T:
        mosquito = environment.get_mosquito()

        if mosquito is None:
            result.add_populations(environment.get_populations())
            environment.add_sterile_mosquitoes(control)
            environment.next_time()
            environment.add_sentinel()
            mosquito = environment.get_mosquito()
            if mosquito is None:
                break

        mosquito, alive = environment.grow_old(mosquito, config)

        if not alive:
            continue

        environment.mate(mosquito)
        environment.migrate(mosquito)

    result.write()
    result.draw()
