import data.reading
import sys

config = data.reading.read_config(*sys.argv[1:2])
data.reading.config = config

import simulation

simulation.run_simulation(*sys.argv[2:])
