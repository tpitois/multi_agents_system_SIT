# Mosquito Life Cycle Simulation with Sterile Insect Technique (SIT)

This project simulates the life cycle of mosquitoes in a multi-agent system, focusing on the Sterile Insect Technique (SIT) as a method for controlling mosquito populations. The simulation models the behavior and development of mosquitoes over time, considering interactions between patches and the biological characteristics specific to each life stage.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)

## Installation

To run the simulation, you need to have Python installed on your system. You can download Python from [python.org](https://www.python.org/).


```bash
git clone https://github.com/your-username/mosquito-simulation.git
cd mosquito-simulation
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the simulation, use the following command:

```bash
python main.py <config_file> <init_mosquito_file> <control_file> <folder_name>
```

- `<config_file>`: Path to the JSON configuration file  
  _(Default: `example/config.json`)_
- `<init_mosquito_file>`: Path to the CSV file containing the initial mosquitoes  
  _(Default: `example/init_mosquitoes.csv`)_
- `<control_file>`: Path to the CSV file containing the control strategy  
  _(Default: `example/control.csv`)_
- `<folder_name>`: Name of the folder where results are saved  
  _(Default: `results`)_

## Project Structure

The project is structured as follows:


```
mosquito-simulation/
│
├── agents/
│   ├── mosquito.py
│
├── data/
│   ├── reading.py
│   ├── result.py
│   ├── control.py
│
├── environment/
│   ├── environment.py
│   ├── patch.py
│
├── example/
│   ├── config.json
│   ├── init_mosquitoes.csv
│   ├── control.csv
│
│
├── main.py
├── simulation.py
├── requirements.txt
├── README.md
```

- `agents/`: Contains the mosquito class and its life stages.
- `data/`: Contains modules for reading configuration files, initial mosquito data, and control strategies.
- `environment/`: Contains the environment and patch classes for the simulation.
- `example/`: Example files for initial mosquito data and control strategies, including the default configuration file.
- `main.py`: The main script to run the simulation.
- `simulation.py`: Contains the core simulation logic.
- `requirements.txt`: Lists the required dependencies for the project.
- `README.md`: Project documentation.
