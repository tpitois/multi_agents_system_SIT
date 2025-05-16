import sys
import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path


def read_patch(patch_file):
    df = pd.read_csv(patch_file)
    df = df.drop("Time", axis=1)
    sterile_male_col = df.pop("Sterile Male Adult")
    return df.values, sterile_male_col.values.reshape(-1, 1)

def read_simulation(simulation_folder):
    path2csv = Path(simulation_folder)
    nb_csvfile = len(list(path2csv.glob("*.csv")))
    csvlist = [f"{simulation_folder}/{i:0{len(str(nb_csvfile-1))}}.csv" for i in range(nb_csvfile)]
    wild_pop_list, sterile_male_list = zip(*[read_patch(patch_file) for patch_file in csvlist])
    wild_pop = np.concatenate(wild_pop_list, axis=1)
    sterile_male = np.concatenate(sterile_male_list, axis=1)
    return np.concatenate((wild_pop, sterile_male), axis=1), sterile_male.shape[1]

def process_seq2seq(data, window_len, forecast_len, nb_patches):
    return data[:window_len, :], data[window_len:window_len+forecast_len, -nb_patches:], data[window_len:window_len+forecast_len, :-nb_patches]

def read_dataset_seq2seq(dataset, window_len, forecast_len, nb_patches):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = [read_simulation(folder.path)[0] for folder in os.scandir(dataset)]
    scaler.fit(np.concatenate(data))
    past_list, deterministic_future_list, future_list =  zip(*[process_seq2seq(scaler.transform(simu), window_len, forecast_len, nb_patches) for simu in data])
    return np.array(past_list), np.array(deterministic_future_list), np.array(future_list)

def simu_to_lookback(simulation_folder, lookback):
    data, nb_sterile = read_simulation(simulation_folder)
    X_list, Y_list  = [], []
    for i in range(data.shape[0]-lookback-1):
        X_list.append(data[i:i+lookback])
        Y_list.append(data[i+lookback, :data.shape[1]-nb_sterile])
    return np.array(X_list), np.array(Y_list)

def read_dataset(dataset, lookback=1):
    X_list, Y_list = zip(*[simu_to_lookback(folder.path, lookback) for folder in os.scandir(dataset)])
    return np.concatenate(X_list), np.concatenate(Y_list)

if __name__ == "__main__":
    dataset_path = sys.argv[1]
    processed_dataset_path = sys.argv[2]
    X, Y = read_dataset(dataset_path)

