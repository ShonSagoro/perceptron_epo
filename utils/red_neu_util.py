import random

import numpy as np
import pandas as pd

from Models.epoch import Epoch
from Models.parameter import Parameter

# values =  pd.read_csv('test/test.csv', header=None)
values = pd.read_csv(r'C:\Users\ramos\Documents\Python_Project\EpoNeu\test\test.csv', header=None)


def activate_function(u_values):
    y_values_calculate = []
    for i in range(len(u_values)):
        if u_values[i] >= 0:
            y_values_calculate.append(1)
        else:
            y_values_calculate.append(0)
    return y_values_calculate


class RedNeuUtil:
    def __init__(self, parameters, data):
        self.parameter = parameters
        self.list_epoch = []
        self.weights = []
        self.weights0 = []
        self.x_values = data.iloc[:, :-1]
        self.y_values_desired = data.iloc[:, -1]

    def init_optimization(self):
        self.add_bias()
        self.calculate_weights()
        for i in range(0, self.parameter.epochs):
            u = np.linalg.multi_dot([self.x_values[:, 1:], np.transpose(self.weights[1:])]) + self.weights[0]
            errors_y = np.array(self.y_values_desired - activate_function(u))
            delta_x = self.calculate_delta(errors_y)
            norm_error_y = np.linalg.norm(errors_y)
            self.list_epoch.append(Epoch(i, norm_error_y, self.weights))
            self.update_weights(delta_x)
        self.print_all_epochs()

    def calculate_weights(self):
        self.weights = np.array(
            [1 if i == 0 else float(f"{random.uniform(0, 1):.4f}") for i in range(len(self.x_values[0]))])

    def update_weights(self, delta_x):
        self.weights = np.add(self.weights, delta_x)

    def calculate_delta(self, error_y):
        return self.parameter.eta * np.dot(np.transpose(error_y), self.x_values)

    def add_bias(self):
        ones_columns = np.ones((self.x_values.shape[0], 1))
        self.x_values = np.hstack((ones_columns, self.x_values))

    def print_all_epochs(self):
        for epoch in self.list_epoch:
            print(epoch)


eta = 0.25
toledacia = 0.1
epochs = 100

parameter = Parameter(eta, toledacia, epochs)

util = RedNeuUtil(parameter, values)
util.init_optimization()