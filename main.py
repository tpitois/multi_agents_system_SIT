import data.reading
import sys

config = data.reading.read_config(*sys.argv[1:2])
data.reading.config = config

import simulation, time

tic = time.time()
simulation.run_simulation(*sys.argv[2:])
toc = time.time()
print(toc - tic)
