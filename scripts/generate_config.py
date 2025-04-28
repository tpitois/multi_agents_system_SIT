import numpy as np
import pandas as pd
import json

from generate_control import control

def random_matrix(N):
    mat = np.random.uniform(0.7, 0.85, (N, N))
    filter = np.tile((1-np.diag(mat))/(np.sum(mat, axis=1)-np.diag(mat)), (N, 1)).transpose()
    np.fill_diagonal(filter, 1)
    res = np.multiply(mat, filter)
    return res.tolist()

def init_mosquitoes(simulation_folder):
    df = pd.DataFrame(0*np.ones((10, 2)), columns=["Male Egg", "Female Egg"])
    """
    df = pd.concat([pd.read_csv(f"{simulation_folder}{i}.csv").iloc[-1] for i in range(10)], axis=1).T
    df = df.drop("Time", axis=1)
    df["Sterile Male Adult"] = 0
    df["Sterile Female Adult"] = 0
    for type in ["Egg", "Larva", "Pupa"]:
        for gender in ["Male", "Female"]:
            df[f"{gender} {type}"] = df[type]/2
        df = df.drop(type, axis=1)
    """
    return df


if __name__ == '__main__':
    N = 10
    T = 80

    with open("config/config.json") as f:
        dico = json.load(f)

    dico["number_of_patches"] = N
    dico["period"] = T
    dico["mating_rates"] = list(np.random.uniform(0.1, 0.3, N))
    dico["capacity"] = list(np.random.uniform(1000, 2000, N))
    dico["migration_rates"] = random_matrix(N)

    with open("config/config.json", "w") as outfile:
        outfile.write(json.dumps(dico, indent=4))

    df_init = init_mosquitoes("initial_mosquitoes/")
    df_control = control(N, T, np.random.uniform(1500, 10000))
    df_init.to_csv("config/init_mosquitoes.csv", index=False)
    df_control.to_csv("config/control.csv", index=False)
