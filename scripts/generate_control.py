import sys

import numpy as np
import pandas as pd
import json

def control(N, T, control_value):
    mat = np.zeros((T, N))
    for i, val in enumerate(control_value):
        mat[20::7, i] = val
    df = pd.DataFrame(mat, columns=range(N))
    df["Time"] = range(T)
    return df

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        dico = json.load(f)

    control(dico["number_of_patches"], dico["period"], 125000*np.random.random(dico["number_of_patches"])).to_csv(sys.argv[2], index=False)
    