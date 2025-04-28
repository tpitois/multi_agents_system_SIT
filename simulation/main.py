import sys
import os
import time
import random

from data.reading import read_config, read_init_mosquitoes
from environment.patch import Patch
from environment.environment import Environment
from data.result import Result
from data.control import Control

os.environ["OPENBLAS_MAIN_FREE"] = "1"


config = read_config(*sys.argv[1:2])
init_mosquito_file, control_file, folder_name = sys.argv[2:]

T = config["period"]
dt = config["dt"]
N = config["number_of_patches"]

patches = [Patch(config["mating_rates"][i], config["migration_rates"][i], config["capacity"][i]) for i in range(N)]
mosquitoes = read_init_mosquitoes(init_mosquito_file, config)
mosquitoes = random.sample(mosquitoes, len(mosquitoes))

environment = Environment(mosquitoes, patches, dt)
result = Result(N, T, dt, folder_name=folder_name)
control = Control(N, T, dt)

control.read(control_file)
result.add_populations(environment.get_populations())

tic = time.time()

while environment.time < T:

    if environment.empty_queue():
        #print(environment.time)
        result.add_populations(environment.get_populations())
        environment.add_sterile_mosquitoes(control, config)
        environment.next_time()

    mosquito = environment.get_mosquito()

    mosquito, alive = environment.grow_old(mosquito, config)

    if not alive:
        continue

    environment.mate(mosquito, config)
    environment.migrate(mosquito)

result.write()
result.draw()

toc = time.time()
print(toc - tic)
