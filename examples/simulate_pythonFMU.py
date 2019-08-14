import os
import sys
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2

root = os.path.dirname(os.path.realpath(__file__))

# Add path to wrapper here
sys.path.append(os.path.join(root, '..', 'SimulatorToFMU', 'utilities'))

# Load the FMU
fmu = load_fmu(os.path.join(root, 'simulator.fmu'), log_level=7)

# Setup coupled network
master = CoupledFMUModelME2([['FMU1', fmu]], [])

# Run the FMU
result = master.simulate(start_time=0, final_time=1)

# Print results
print('Timesteps:', result['time'])