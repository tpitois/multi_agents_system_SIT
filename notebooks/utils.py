import matplotlib.pyplot as plt
import numpy as np

def draw_prediction(real, pred, patch):
    names = ["Egg", "Larva", "Pupa", "Fertile Male Adult", "Fertile Female Adult", "Sterile Female Adult", "Mated Female Adult"]
    fig, axs = plt.subplots(2, 4, figsize=(15, 10), constrained_layout=False)
    axs = axs.flatten()
    time_interval = range(real.shape[0])
    max_val = max(np.max(real), np.max(pred))
    for i in range(7):
        ax = axs[i]
        ax.plot(time_interval, real[:, 7*patch+i])
        ax.plot(time_interval, pred[:, 7*patch+i], linestyle='--')
        ax.set_title(names[i])
        ax.set_xlim(time_interval[0], time_interval[-1])
        ax.set_ylim(0, max_val)
    fig.suptitle(f"Patch n°{patch}")
    plt.show()

def plot_loss(model):
    history = model.history
    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.title("Model loss")
    plt.ylabel("loss")
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

def read_simulation_control(filepath):
    return pd.read_csv(filepath).set_index('Time').values
