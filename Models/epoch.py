class Epoch:
    def __init__(self, id, error_norma, weights, all_weights):
        self.epoch = id
        self.error_norma = error_norma
        self.weights = weights
        self.all_weights = all_weights

    def __str__(self):
        return f"Epoch: {self.epoch}, Error Norma: {self.error_norma}, Weights: {self.weights}"