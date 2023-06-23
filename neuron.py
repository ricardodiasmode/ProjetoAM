class Neuron:
    def __init__(self, connection_amount):
        self.Weights = []
        self.Error = 0.0
        self.OutValue = 1.0
        self.ConnectionAmount = connection_amount
