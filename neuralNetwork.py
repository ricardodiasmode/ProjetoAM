import random
import struct
import time

global Gerador

def func(X):
    if X == 0:
        return 0
    elif X < 0:
        return -1
    else:
        return 1

def relu(X):
    if X < 0:
        return 0
    else:
        if X < 10000:
            return X
        else:
            return 10000

def reluDx(X):
    if X < 0:
        return 0
    else:
        return 1

TAXA_APRENDIZADO = 0.1
TAXA_PESO_INICIAL = 1.0
BIAS = 1

def relu(X):
    if X < 0:
        return 0
    elif X < 10000:
        return X
    else:
        return 10000

class Neuronio:
    def __init__(self, QuantidadeLigacoes):
        self.Peso = [TAXA_PESO_INICIAL] * QuantidadeLigacoes
        self.Erro = 0.0
        self.Saida = 0.0
        self.QuantidadeLigacoes = QuantidadeLigacoes

class Camada:
    def __init__(self, QuantidadeNeuronios, QuantidadeLigacoes):
        self.QuantidadeNeuronios = QuantidadeNeuronios
        self.Neuronios = [Neuronio(QuantidadeLigacoes) for i in range(QuantidadeNeuronios)]

class RedeNeural:
    def __init__(self, QuantidadeEntrada, QuantidadeEscondidas, QuantidadeSaida):
        self.CamadaEntrada = Camada(QuantidadeEntrada, 0)
        self.CamadaEscondida = [Camada(QuantidadeEscondidas, QuantidadeEntrada) for i in range(QuantidadeEscondidas)]
        self.CamadaSaida = Camada(QuantidadeSaida, QuantidadeEscondidas)
        self.QuantidadeEscondidas = QuantidadeEscondidas

def RNA_CopiarVetorParaCamadas(Rede, Vetor):
    j = 0
    for i in range(Rede.QuantidadeEscondidas):
        for k in range(Rede.CamadaEscondida[i].QuantidadeNeuronios):
            for l in range(Rede.CamadaEscondida[i].Neuronios[k].QuantidadeLigacoes):
                Rede.CamadaEscondida[i].Neuronios[k].Peso[l] = Vetor[j]
                j += 1

    for k in range(Rede.CamadaSaida.QuantidadeNeuronios):
        for l in range(Rede.CamadaSaida.Neuronios[k].QuantidadeLigacoes):
            Rede.CamadaSaida.Neuronios[k].Peso[l] = Vetor[j]
            j += 1

def RNA_CopiarCamadasParaVetor(Rede, Vetor):
    j = 0

    for i in range(Rede.QuantidadeEscondidas):
        for k in range(Rede.CamadaEscondida[i].QuantidadeNeuronios):
            for l in range(Rede.CamadaEscondida[i].Neuronios[k].QuantidadeLigacoes):
                Vetor[j] = Rede.CamadaEscondida[i].Neuronios[k].Peso[l]
                j += 1

    for k in range(Rede.CamadaSaida.QuantidadeNeuronios):
        for l in range(Rede.CamadaSaida.Neuronios[k].QuantidadeLigacoes):
            Vetor[j] = Rede.CamadaSaida.Neuronios[k].Peso[l]
            j += 1

def RNA_CopiarParaEntrada(Rede, VetorEntrada):
    for i in range(Rede.CamadaEntrada.QuantidadeNeuronios - BIAS):
        Rede.CamadaEntrada.Neuronios[i].Saida = VetorEntrada[i]

def RNA_QuantidadePesos(Rede):
    Soma = 0
    for i in range(Rede.QuantidadeEscondidas):
        for j in range(Rede.CamadaEscondida[i].QuantidadeNeuronios):
            Soma = Soma + Rede.CamadaEscondida[i].Neuronios[j].QuantidadeLigacoes

    for i in range(Rede.CamadaSaida.QuantidadeNeuronios):
        Soma = Soma + Rede.CamadaSaida.Neuronios[i].QuantidadeLigacoes
    return Soma

def RNA_CopiarDaSaida(Rede, VetorSaida):
    for i in range(Rede.CamadaSaida.QuantidadeNeuronios):
        VetorSaida[i] = Rede.CamadaSaida.Neuronios[i].Saida

def RNA_CalcularSaida(Rede):
    Somatorio = 0
    # Calculando saidas entre a camada de entrada e a primeira camada escondida
    for i in range(Rede.CamadaEscondida[0].QuantidadeNeuronios - BIAS):
        Somatorio = 0
        for j in range(Rede.CamadaEntrada.QuantidadeNeuronios):
            Somatorio += Rede.CamadaEntrada.Neuronios[j].Saida * Rede.CamadaEscondida[0].Neuronios[i].Peso[j]
        Rede.CamadaEscondida[0].Neuronios[i].Saida = AtivacaoOcultas(Somatorio)

    # Calculando saidas entre a camada escondida k e a camada escondida k-1
    for k in range(1, Rede.QuantidadeEscondidas):
        for i in range(Rede.CamadaEscondida[k].QuantidadeNeuronios - BIAS):
            Somatorio = 0
            for j in range(Rede.CamadaEscondida[k-1].QuantidadeNeuronios):
                Somatorio += Rede.CamadaEscondida[k-1].Neuronios[j].Saida * Rede.CamadaEscondida[k].Neuronios[i].Peso[j]
            Rede.CamadaEscondida[k].Neuronios[i].Saida = AtivacaoOcultas(Somatorio)

    # Calculando saidas entre a camada de saida e a ultima camada escondida
    for i in range(Rede.CamadaSaida.QuantidadeNeuronios):
        Somatorio = 0
        for j in range(Rede.CamadaEscondida[k-1].QuantidadeNeuronios):
            Somatorio += Rede.CamadaEscondida[k-1].Neuronios[j].Saida * Rede.CamadaSaida.Neuronios[i].Peso[j]
        Rede.CamadaSaida.Neuronios[i].Saida = AtivacaoSaida(Somatorio)

def RNA_CriarNeuronio(Neuron, QuantidadeLigacoes):
    Neuron.QuantidadeLigacoes = QuantidadeLigacoes
    Neuron.Peso = [0] * QuantidadeLigacoes

    for i in range(QuantidadeLigacoes):
        if random.randint(0, 1) == 0:
            Neuron.Peso[i] = random.uniform(0, 1) / TAXA_PESO_INICIAL
        else:
            Neuron.Peso[i] = -random.uniform(0, 1) / TAXA_PESO_INICIAL

    Neuron.Erro = 0
    Neuron.Saida = 1

def RNA_CriarRedeNeural(QuantidadeEscondidas, QtdNeuroniosEntrada, QtdNeuroniosEscondida, QtdNeuroniosSaida):
    QtdNeuroniosEntrada = QtdNeuroniosEntrada + BIAS
    QtdNeuroniosEscondida = QtdNeuroniosEscondida + BIAS
    Rede = RedeNeural()
    Rede.CamadaEntrada.QuantidadeNeuronios = QtdNeuroniosEntrada
    Rede.CamadaEntrada.Neuronios = []

    for i in range(QtdNeuroniosEntrada):
        Neuronio = Neuronio()
        Neuronio.Saida = 1.0
        Rede.CamadaEntrada.Neuronios.append(Neuronio)

    Rede.QuantidadeEscondidas = QuantidadeEscondidas
    Rede.CamadaEscondida = []

    for i in range(QuantidadeEscondidas):
        Camada = Camada()
        Camada.QuantidadeNeuronios = QtdNeuroniosEscondida
        Camada.Neuronios = []

        for j in range(QtdNeuroniosEscondida):
            if i == 0:
                Neuronio = RNA_CriarNeuronio(QtdNeuroniosEntrada)
            else:
                Neuronio = RNA_CriarNeuronio(QtdNeuroniosEscondida)

            Camada.Neuronios.append(Neuronio)

        Rede.CamadaEscondida.append(Camada)

    Rede.CamadaSaida.QuantidadeNeuronios = QtdNeuroniosSaida
    Rede.CamadaSaida.Neuronios = []

    for j in range(QtdNeuroniosSaida):
        Neuronio = RNA_CriarNeuronio(QtdNeuroniosEscondida)
        Rede.CamadaSaida.Neuronios.append(Neuronio)

    return Rede

def RNA_CarregarRede(String):
    with open(String, "rb") as f:
        QtdEscondida, QtdNeuroEntrada, QtdNeuroEscondida, QtdNeuroSaida = struct.unpack("iiii", f.read(16))

        Temp = RNA_CriarRedeNeural(QtdEscondida, QtdNeuroEntrada, QtdNeuroEscondida, QtdNeuroSaida)

        for k in range(Temp.QuantidadeEscondidas):
            for i in range(Temp.CamadaEscondida[k].QuantidadeNeuronios):
                for j in range(Temp.CamadaEscondida[k].Neuronios[i].QuantidadeLigacoes):
                    Temp.CamadaEscondida[k].Neuronios[i].Peso[j] = struct.unpack("d", f.read(8))[0]
        for i in range(Temp.CamadaSaida.QuantidadeNeuronios):
            for j in range(Temp.CamadaSaida.Neuronios[i].QuantidadeLigacoes):
                Temp.CamadaSaida.Neuronios[i].Peso[j] = struct.unpack("d", f.read(8))[0]

        return Temp

def RNA_SalvarRede(Temp, String):
    with open(String, "wb") as f:
    f.write(struct.pack("i", Temp.QuantidadeEscondidas))
    f.write(struct.pack("i", Temp.CamadaEntrada.QuantidadeNeuronios))
    f.write(struct.pack("i", Temp.CamadaEscondida[0].QuantidadeNeuronios))
    f.write(struct.pack("i", Temp.CamadaSaida.QuantidadeNeuronios))
    for k in range(Temp.QuantidadeEscondidas):
        for i in range(Temp.CamadaEscondida[k].QuantidadeNeuronios):
            for j in range(Temp.CamadaEscondida[k].Neuronios[i].QuantidadeLigacoes):
                f.write(struct.pack("d", Temp.CamadaEscondida[k].Neuronios[i].Peso[j]))

    for i in range(Temp.CamadaSaida.QuantidadeNeuronios):
        for j in range(Temp.CamadaSaida.Neuronios[i].QuantidadeLigacoes):
            f.write(struct.pack("d", Temp.CamadaSaida.Neuronios[i].Peso[j]))

def RNA_ImprimirPesos(Temp):
    for k in range(Temp.QuantidadeEscondidas):
        print("Camada escondida", k)
        for i in range(Temp.CamadaEscondida[k].QuantidadeNeuronios):
            print("\tNeuronio", i)
            for j in range(Temp.CamadaEscondida[k].Neuronios[i].QuantidadeLigacoes):
                print("\t\tPeso", j, ":", Temp.CamadaEscondida[k].Neuronios[i].Peso[j])

    print("Camada saida", k)
    for i in range(Temp.CamadaSaida.QuantidadeNeuronios):
        print("\tNeuronio", i)
        for j in range(Temp.CamadaSaida.Neuronios[i].QuantidadeLigacoes):
            print("\t\tPeso", j, ":", Temp.CamadaSaida.Neuronios[i].Peso[j])

def InicializarGeradorAleatorio():
    Gerador = random.Random()
    Gerador.seed(time.time())


