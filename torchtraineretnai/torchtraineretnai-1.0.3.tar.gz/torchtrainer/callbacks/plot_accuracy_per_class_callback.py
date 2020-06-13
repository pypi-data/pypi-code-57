from torchtrainer.callbacks.training_callback import TrainingCallback
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import path

class PlotAccuracyPerClassCallback(TrainingCallback):
    def __init__(self, num_classes, folder_path):
        self.num_classes = num_classes
        self.folder_path = folder_path
        self.exp_name = path.basename(path.normpath(folder_path))

    def on_mode_end(self, mode, log):
        per_class_accuracies = [log["Class {:d} Accuracy".format(class_index)] for class_index in range(self.num_classes)]
        img_file_path = path.join(self.folder_path, "AccuracyPerClass-{:s}.png".format(mode))
        self.save_frequency_plot(img_file_path, per_class_accuracies, title="Accuracy Per Class", bar_labels=("Class", "Accuracy"), ytick_major_step=0.1, ytick_minor_step=0.05, max_val=1)

    def save_frequency_plot(self, plot_file_path, data, title="", bar_labels=("",""), bar_labelrotation=0, ytick_major_step=0.1, ytick_minor_step=0.05, ytick_labels=None, max_val=None):
        data = pd.DataFrame(data)
        ax1 = data.plot.bar(figsize=(20, 13))
        plt.title(title)
        plt.suptitle(self.exp_name)

        if not max_val:
            max_val = np.max(data.values)+5
        ax1.set_yticks(np.arange(0, max_val, ytick_major_step))
        ax1.set_yticks(np.arange(0, max_val, ytick_minor_step), minor=True)
        if ytick_labels:
            ax1.set_yticklabels(labels = ytick_labels)
        ax1.yaxis.grid(which='major', color='#555555', linestyle='-', alpha=0.5)
        ax1.yaxis.grid(which='minor', color='#AAAAAA', linestyle=':', alpha=0.9)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=bar_labelrotation)

        plt.xlabel(bar_labels[0])
        plt.ylabel(bar_labels[1])
        ax1.get_legend().remove()

        plt.tight_layout()
        plt.savefig(plot_file_path)
        plt.close()
