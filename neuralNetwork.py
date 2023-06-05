import random

LEARNING_RATE = 0.1
INITIAL_WEIGHT_RATE = 1.0
BIAS = 1


def func(X):
    if X == 0:
        return 0
    elif X < 0:
        return -1
    else:
        return 1


def reluDx(X):
    if X < 0:
        return 0
    else:
        return 1


def relu(X):
    if X < 0:
        return 0
    elif X < 10000:
        return X
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
    AMOUNT_ENTRY_NEURON = 8 + BIAS
    AMOUNT_HIDDEN_NEURON = [8 + BIAS]
    AMOUNT_OUT_NEURON = 8

    # hidden_layers_array is an array of int. The nth position is the number of neurons in the nth layer
    def __init__(self):
        self.entry_layer = Layer(self.AMOUNT_ENTRY_NEURON, 0)
        self.hidden_layer = [Layer(self.AMOUNT_HIDDEN_NEURON[i], self.AMOUNT_ENTRY_NEURON) for i in
                             range(len(self.AMOUNT_HIDDEN_NEURON))]
        self.out_layer = Layer(self.AMOUNT_OUT_NEURON, self.AMOUNT_HIDDEN_NEURON[-1])
        self.amount_of_hidden_layers = len(self.AMOUNT_HIDDEN_NEURON)


def RNA_CopiarVetorParaCamadas(neural_network, Vetor):
    j = 0
    for i in range(neural_network.QuantidadeEscondidas):
        for k in range(neural_network.hidden_layer[i].amount_neuron):
            for l in range(neural_network.hidden_layer[i].Neuronios[k].QuantidadeLigacoes):
                neural_network.hidden_layer[i].Neuronios[k].Peso[l] = Vetor[j]
                j += 1

    for k in range(neural_network.out_layer.amount_neuron):
        for l in range(neural_network.out_layer.Neuronios[k].QuantidadeLigacoes):
            neural_network.out_layer.Neuronios[k].Peso[l] = Vetor[j]
            j += 1


def RNA_CopiarCamadasParaVetor(neural_network, Vetor):
    j = 0

    for i in range(neural_network.QuantidadeEscondidas):
        for k in range(neural_network.hidden_layer[i].amount_neuron):
            for l in range(neural_network.hidden_layer[i].Neuronios[k].QuantidadeLigacoes):
                Vetor[j] = neural_network.hidden_layer[i].Neuronios[k].Peso[l]
                j += 1

    for k in range(neural_network.out_layer.amount_neuron):
        for l in range(neural_network.out_layer.Neuronios[k].QuantidadeLigacoes):
            Vetor[j] = neural_network.out_layer.Neuronios[k].Peso[l]
            j += 1


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
    # Calculando saidas entre a camada de entrada e a primeira camada escondida
    for i in range(neural_network.hidden_layer[0].amount_neuron - BIAS):
        summation = 0
        for j in range(neural_network.entry_layer.amount_neuron):
            summation += neural_network.entry_layer.neurons[j].out_value * \
                         neural_network.hidden_layer[0].neurons[i].weight[j]
        neural_network.hidden_layer[0].neurons[i].out_value = relu(summation)

    k = 0
    # Calculando saidas entre a camada escondida k e a camada escondida k-1
    for k in range(1, neural_network.amount_of_hidden_layers):
        for i in range(neural_network.hidden_layer[k].amount_neuron - BIAS):
            summation = 0
            for j in range(neural_network.hidden_layer[k - 1].amount_neuron):
                print("hidden_layer len: " + str(len(neural_network.hidden_layer)) + " / k: " + str(k))
                print("neuron len: " + str(len(neural_network.hidden_layer[k].neurons)) + " / j: " + str(j))
                print("weight len: " + str(len(neural_network.hidden_layer[k].neurons[i].weight)) + " / i: " + str(i))
                summation += neural_network.hidden_layer[k - 1].neurons[j].out_value * \
                             neural_network.hidden_layer[k].neurons[i].weight[j]
            neural_network.hidden_layer[k].neurons[i].out_value = relu(summation)

    # Calculando saidas entre a camada de saida e a ultima camada escondida
    for i in range(neural_network.out_layer.amount_neuron):
        summation = 0
        for j in range(neural_network.hidden_layer[k - 1].amount_neuron):
            summation += neural_network.hidden_layer[k - 1].neurons[j].out_value * \
                         neural_network.out_layer.neurons[i].weight[j]
        neural_network.out_layer.neurons[i].out_value = relu(summation)


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
