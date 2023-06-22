import random

INITIAL_WEIGHT_RATE = 1.0
BIAS = 1


def relu(x):
    if x < 0:
        return 0
    elif x < 10000:
        return x
    else:
        return 10000


class Neuron:
    def __init__(self, connection_amount):
        self.weight = []
        self.error = 0.0
        self.out_value = 1.0
        self.connection_amount = connection_amount


class Layer:
    def __init__(self, amount_neuron, amount_connections):
        self.amount_neuron = amount_neuron
        self.neurons = [Neuron(amount_connections) for i in range(amount_neuron)]


class NeuralNetwork:
    BIAS = 1
    AMOUNT_ENTRY_NEURON = 3 + BIAS
    AMOUNT_HIDDEN_NEURON = [5 + BIAS]
    AMOUNT_OUT_NEURON = 5

    # hidden_layers_array is an array of int. The nth position is the number of neurons in the nth layer
    def __init__(self):
        self.entry_layer = Layer(self.AMOUNT_ENTRY_NEURON, 0)
        self.hidden_layer = [Layer(self.AMOUNT_HIDDEN_NEURON[i], self.AMOUNT_ENTRY_NEURON) for i in
                             range(len(self.AMOUNT_HIDDEN_NEURON))]
        self.out_layer = Layer(self.AMOUNT_OUT_NEURON, self.AMOUNT_HIDDEN_NEURON[-1])
        self.amount_of_hidden_layers = len(self.AMOUNT_HIDDEN_NEURON)


def neural_network_copy_to_entry_layer(neural_network, entry_vector):
    for i in range(neural_network.entry_layer.amount_neuron - BIAS):
        neural_network.entry_layer.neurons[i].out_value = entry_vector[i]


def neural_network_get_weight_amount(neural_network):
    Sum = 0
    for i in range(neural_network.amount_of_hidden_layers):
        for j in range(neural_network.hidden_layer[i].amount_neuron):
            Sum = Sum + neural_network.hidden_layer[i].neurons[j].connection_amount

    for i in range(neural_network.out_layer.amount_neuron):
        Sum = Sum + neural_network.out_layer.neurons[i].connection_amount
    return Sum


def neural_network_copy_weights(neural_network):
    out_layer = []
    for i in range(neural_network.out_layer.amount_neuron):
        out_layer.append(neural_network.out_layer.neurons[i].out_value)
    return out_layer


def neural_network_calculate_weights(neural_network):
    # Calculando saídas entre a camada de entrada e a primeira camada escondida
    hidden_layer_1 = neural_network.hidden_layer[0]

    for neuron_h1 in hidden_layer_1.neurons:
        summation = sum(neuron_i.out_value * weight_i for neuron_i, weight_i in zip(neural_network.entry_layer.neurons, neuron_h1.weight))
        neuron_h1.out_value = relu(summation)

    # Calculando saídas entre as camadas escondidas
    amount_hidden_layers = neural_network.amount_of_hidden_layers
    hidden_layers = neural_network.hidden_layer

    for k in range(1, amount_hidden_layers):
        hidden_layer_k = hidden_layers[k]

        for neuron_hk in hidden_layer_k.neurons:
            summation = sum(neuron_prev.out_value * weight_prev for neuron_prev, weight_prev in zip(hidden_layers[k - 1].neurons, neuron_hk.weight))
            neuron_hk.out_value = relu(summation)

    # Calculando saídas entre a última camada escondida e a camada de saída
    out_layer = neural_network.out_layer

    for neuron_out in out_layer.neurons:
        summation = sum(neuron_hk.out_value * weight_hk for neuron_hk, weight_hk in zip(hidden_layers[-1].neurons, neuron_out.weight))
        neuron_out.out_value = relu(summation)

    # Definindo a maior saída como 1 e o restante como 0
    max_out_value = max(out_layer.neurons, key=lambda neuron: neuron.out_value)
    for neuron_out in out_layer.neurons:
        neuron_out.out_value = 1 if neuron_out == max_out_value else 0


def neural_network_initialize_neuron_weight(neuron):
    for i in range(neuron.connection_amount):
        if random.randint(0, 1) == 0:
            weight_to_add = random.uniform(0, 1) / INITIAL_WEIGHT_RATE
        else:
            weight_to_add = -random.uniform(0, 1) / INITIAL_WEIGHT_RATE
        neuron.weight.append(weight_to_add)


# hidden_amount is an array of integers. The nth position is the number of neurons in the nth layer
def neural_network_create():
    entry_neuron_amount = NeuralNetwork.AMOUNT_ENTRY_NEURON
    out_neuron_amount = NeuralNetwork.AMOUNT_OUT_NEURON
    hidden_amount = NeuralNetwork.AMOUNT_HIDDEN_NEURON

    neural_network = NeuralNetwork()

    for i in range(entry_neuron_amount):
        neuron = Neuron(hidden_amount[0])
        neural_network.entry_layer.neurons[i] = neuron

    for i in range(len(hidden_amount)):
        layer = Layer(hidden_amount[i], hidden_amount[i])

        for j in range(hidden_amount[i]):
            neural_network_initialize_neuron_weight(neural_network.hidden_layer[i].neurons[j])

        neural_network.hidden_layer.append(layer)

    for i in range(out_neuron_amount):
        neural_network_initialize_neuron_weight(neural_network.out_layer.neurons[i])

    return neural_network
