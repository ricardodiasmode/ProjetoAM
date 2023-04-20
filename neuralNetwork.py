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
    # hidden_layers_array is a array of int. The nth position is the number of neurons in the nth layer
    def __init__(self, amount_of_entry_neurons, hidden_layers_array, amount_of_out_layer):
        self.entry_layer = Layer(amount_of_entry_neurons, 0)
        self.hidden_layer = [Layer(hidden_layers_array[i], amount_of_entry_neurons) for i in range(len(hidden_layers_array))]
        self.out_layer = Layer(amount_of_out_layer, hidden_layers_array[-1])
        self.amount_of_hidden_layers = len(hidden_layers_array)


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

    # Calculando saidas entre a camada escondida k e a camada escondida k-1
    for k in range(1, neural_network.amount_of_hidden_layers):
        for i in range(neural_network.hidden_layer[k].amount_neuron - BIAS):
            summation = 0
            for j in range(neural_network.hidden_layer[k-1].amount_neuron):
                summation += neural_network.hidden_layer[k-1].neurons[j].out_value * neural_network.hidden_layer[k].neurons[i].weight[j]
            neural_network.hidden_layer[k].neurons[i].out_value = relu(summation)

    # Calculando saidas entre a camada de saida e a ultima camada escondida
    for i in range(neural_network.out_layer.amount_neuron):
        summation = 0
        for j in range(neural_network.hidden_layer[k-1].amount_neuron):
            summation += neural_network.hidden_layer[k-1].neurons[j].out_value * neural_network.out_layer.neurons[i].weight[j]
        neural_network.out_layer.neurons[i].out_value = relu(summation)


def neural_network_initialize_neuron_weight(neuron):
    for i in range(neuron.connection_amount):
        if random.randint(0, 1) == 0:
            weightToAdd = random.uniform(0, 1) / INITIAL_WEIGHT_RATE
        else:
            weightToAdd = -random.uniform(0, 1) / INITIAL_WEIGHT_RATE
        neuron.weight.append(weightToAdd)


# hidden_amount is an array of integers. The nth position is the number of neurons in the nth layer
def neural_network_create(hidden_amount, entry_neuron_amount, out_neuron_amount):
    entry_neuron_amount += BIAS
    for i in range(len(hidden_amount)):
        hidden_amount[i] += BIAS
    neural_network = NeuralNetwork(entry_neuron_amount, hidden_amount, out_neuron_amount)

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


# def neural_network_load(String):
#     with open(String, "rb") as f:
#         QtdEscondida, QtdNeuroEntrada, QtdNeuroEscondida, QtdNeuroSaida = struct.unpack("iiii", f.read(16))
#
#         Temp = RNA_Criarneural_networkNeural(QtdEscondida, QtdNeuroEntrada, QtdNeuroEscondida, QtdNeuroSaida)
#
#         for k in range(Temp.QuantidadeEscondidas):
#             for i in range(Temp.hidden_layer[k].amount_neuron):
#                 for j in range(Temp.hidden_layer[k].Neuronios[i].QuantidadeLigacoes):
#                     Temp.hidden_layer[k].Neuronios[i].Peso[j] = struct.unpack("d", f.read(8))[0]
#         for i in range(Temp.out_layer.amount_neuron):
#             for j in range(Temp.out_layer.Neuronios[i].QuantidadeLigacoes):
#                 Temp.out_layer.Neuronios[i].Peso[j] = struct.unpack("d", f.read(8))[0]
#
#         return Temp

# def neural_network_save(Temp, String):
#     with open(String, "wb") as f:
#     f.write(struct.pack("i", Temp.QuantidadeEscondidas))
#     f.write(struct.pack("i", Temp.CamadaEntrada.amount_neuron))
#     f.write(struct.pack("i", Temp.hidden_layer[0].amount_neuron))
#     f.write(struct.pack("i", Temp.out_layer.amount_neuron))
#     for k in range(Temp.QuantidadeEscondidas):
#         for i in range(Temp.hidden_layer[k].amount_neuron):
#             for j in range(Temp.hidden_layer[k].Neuronios[i].QuantidadeLigacoes):
#                 f.write(struct.pack("d", Temp.hidden_layer[k].Neuronios[i].Peso[j]))
#
#     for i in range(Temp.out_layer.amount_neuron):
#         for j in range(Temp.out_layer.Neuronios[i].QuantidadeLigacoes):
#             f.write(struct.pack("d", Temp.out_layer.Neuronios[i].Peso[j]))

# def RNA_ImprimirPesos(Temp):
#     for k in range(Temp.QuantidadeEscondidas):
#         print("Camada escondida", k)
#         for i in range(Temp.hidden_layer[k].amount_neuron):
#             print("\tNeuronio", i)
#             for j in range(Temp.hidden_layer[k].Neuronios[i].QuantidadeLigacoes):
#                 print("\t\tPeso", j, ":", Temp.hidden_layer[k].Neuronios[i].Peso[j])
#
#     print("Camada saida", k)
#     for i in range(Temp.out_layer.amount_neuron):
#         print("\tNeuronio", i)
#         for j in range(Temp.out_layer.Neuronios[i].QuantidadeLigacoes):
#             print("\t\tPeso", j, ":", Temp.out_layer.Neuronios[i].Peso[j])
#
# def InicializarGeradorAleatorio():
#     Gerador = random.Random()
#     Gerador.seed(time.time())


