import random

import numpy as np

from Models.epoch import Epoch
from utils.per_charts_util import PerChartsUtil


def activate_function(u_values):
    return np.array([1 if u_values[i] >= 0 else 0 for i in range(len(u_values))])


class RedNeuUtil:
    def __init__(self, parameters, data, name_file):
        self.parameter = parameters
        self.list_epoch = []
        self.weights = []
        self.weights0 = []
        self.all_weights = []
        self.x_values = data.iloc[:, :-1]
        self.y_values_desired = data.iloc[:, -1]
        self.generated_figure = []
        self.name_file = name_file
        self.delta_x = 0
        np.set_printoptions(precision=4, suppress=True)

    def start_process(self):
        self.initialize()
        self.optimization_process()

    def initialize(self):
        self.add_bias()
        self.calculate_weights()

    def make_charts(self):
        charts_util = PerChartsUtil(self.list_epoch, self.name_file)
        self.generated_figure.append(charts_util.make_weights_chars())
        self.generated_figure.append(charts_util.make_error_chars())

    def optimization_process(self):
        for i in range(0, self.parameter.epochs):
            u = np.linalg.multi_dot([self.x_values[:, 1:], np.transpose(self.weights[1:])]) + self.weights[0]
            errors_y = np.array(self.y_values_desired - np.array(activate_function(u)))
            norm_error_y = np.linalg.norm(errors_y)
            if norm_error_y > self.parameter.tolerance:
                self.delta_x = self.calculate_delta(errors_y)
                self.update_weights(self.delta_x)
            self.all_weights.append(self.weights)
            self.list_epoch.append(Epoch(i, norm_error_y, self.weights, self.all_weights))
        self.make_charts()
        self.print_all_epochs()

    def update_weights(self, delta_x):
        self.weights = np.round(np.add(self.weights, delta_x), 4)

    def calculate_weights(self):
        self.weights = np.array(
            [1 if i == 0 else float(f"{random.uniform(0, 1):.4f}") for i in range(len(self.x_values[0]))])

    def add_bias(self):
        ones_columns = np.ones((self.x_values.shape[0], 1))
        self.x_values = np.hstack((ones_columns, self.x_values))

    def calculate_delta(self, error_y):
        return abs(self.parameter.eta) * np.dot(np.transpose(error_y), self.x_values)

    def print_all_epochs(self):
        for epoch in self.list_epoch:
            print(epoch)
