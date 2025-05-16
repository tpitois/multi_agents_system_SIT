import sys

import numpy as np
import pandas as pd
import json

def control(N, T, control_value):
    mat = np.zeros((T, N))
    mat[25::7, :] = control_value
    df = pd.DataFrame(mat, columns=range(N))
    df["Time"] = range(T)
    return df

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        dico = json.load(f)

    control(dico["number_of_patches"], dico["period"], np.random.uniform(0, int(1e5))).to_csv(sys.argv[2], index=False)
