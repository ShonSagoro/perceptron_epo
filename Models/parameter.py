class Parameter:
    def __init__(self, eta, epochs, tolerance):
        self.eta=eta
        self.epochs=epochs
        self.tolerance=tolerance

    def __str__(self):
        return f'Parameter(eta={self.eta}, epochs={self.epochs}, tolerance={self.tolerance})'
