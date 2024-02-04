import random

import numpy as np
from matplotlib import pyplot as plt


class PerChartsUtil:
    def __init__(self, epochs, namefile):
        plt.style.use('dark_background')
        self.epochs=epochs
        self.namefile=namefile

    def make_weights_chars(self):
        fig, ax = plt.subplots()
        all_weights_t = np.transpose(self.epochs[-1].all_weights)
        for i in range(len(all_weights_t)):
            random_color = (random.randint(100, 255)/255, random.randint(100, 255)/255, random.randint(100, 255)/255)
            ax.plot(all_weights_t[i], label=f'w{(i+1)}', color=random_color)
        ax.legend()
        ax.set_xlabel('Epochs')
        ax.set_ylabel('Weights')
        ax.set_title(f'Evolution of weights in each epoch, from file: {self.namefile}')
        return fig

    def make_error_chars(self):
        fig, ax = plt.subplots()
        errors = [epoch.error_norma for epoch in self.epochs]
        ax.plot(errors, label=f'Norma Error', color='red')
        ax.legend()
        ax.set_xlabel('Epochs')
        ax.set_ylabel('Error')
        ax.set_title(f'Evolution of norma Error in each epoch, from file: {self.namefile}')
        return fig

