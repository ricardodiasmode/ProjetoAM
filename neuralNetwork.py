# Description: This file contains the neural network class and its functions
import random

import utils
from layer import Layer

INITIAL_WEIGHT_RATE = 1.0
BIAS = 1
AMOUNT_ENTRY_NEURON = 2 + BIAS
AMOUNT_HIDDEN_NEURON = [4 + BIAS]
AMOUNT_OUT_NEURON = 5


def relu(x):
    return max(0, x)


def GetEntryParams(character, background):
    ClosestLogDistance = utils.GetClosestDistance(character.CurrentLocation, background.LogLocations)
    return [  # character.HasLog, # Lets hide this till he doesn't get log
        ClosestLogDistance[0], ClosestLogDistance[1]]


class NeuralNetwork:
    EntryLayer = []
    HiddenLayer = []
    OutLayer = []

    LastCalculatedOutput = []

    def __init__(self):
        self.EntryLayer = Layer(AMOUNT_ENTRY_NEURON, 0)
        self.HiddenLayers = [Layer(AMOUNT_HIDDEN_NEURON[i], AMOUNT_ENTRY_NEURON) for i in
                             range(len(AMOUNT_HIDDEN_NEURON))]
        self.OutLayer = Layer(AMOUNT_OUT_NEURON, AMOUNT_HIDDEN_NEURON[-1])

        self.InitializeWeights()

    def InitializeWeights(self):
        for i in range(len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                self.HiddenLayers[i].Neurons[j].Weights.append(
                    random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
        for j in range(len(self.OutLayer.Neurons)):
            self.OutLayer.Neurons[j].Weights.append(
                random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))

    def Think(self, character, background):
        self.FeedEntryLayer(character, background)
        self.CalculateWeights()
        self.LastCalculatedOutput = self.GetOutput()

    def FeedEntryLayer(self, character, background):
        EntryParams = GetEntryParams(character, background)
        for i in range(len(self.EntryLayer.Neurons) - BIAS):
            self.EntryLayer.Neurons[i].OutValue = EntryParams[i]

    def CalculateWeights(self):
        # Calculate the first Hidden Layer
        for j in range(len(self.HiddenLayers[0].Neurons)):
            Sum = 0
            for k in range(len(self.HiddenLayers[0].Neurons[j].Weights)):
                Sum = Sum + self.HiddenLayers[0].Neurons[j].Weights[k] * self.EntryLayer.Neurons[k].OutValue
            self.HiddenLayers[0].Neurons[j].OutValue = relu(Sum)
        # Calculate the other Hidden Layers
        for i in range(1, len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                Sum = 0
                for k in range(len(self.HiddenLayers[i].Neurons[j].Weights)):
                    Sum += self.HiddenLayers[i].Neurons[j].Weights[k] * self.HiddenLayers[i - 1].Neurons[k].OutValue
                self.HiddenLayers[i].Neurons[j].OutValue = relu(Sum)
        # Calculate the Out Layer
        for j in range(len(self.OutLayer.Neurons)):
            Sum = 0
            for k in range(len(self.OutLayer.Neurons[j].Weights)):
                Sum += self.OutLayer.Neurons[j].Weights[k] * self.HiddenLayers[-1].Neurons[k].OutValue
            self.OutLayer.Neurons[j].OutValue = relu(Sum)

    def GetOutput(self):
        GreaterOutValueIndex = 0
        Output = []
        OutputToPrint = []
        for i in range(len(self.OutLayer.Neurons)):
            OutputToPrint.append(self.OutLayer.Neurons[i].OutValue)
            if self.OutLayer.Neurons[i].OutValue > self.OutLayer.Neurons[GreaterOutValueIndex].OutValue:
                GreaterOutValueIndex = i
        for i in range(len(self.OutLayer.Neurons)):
            if i != GreaterOutValueIndex:
                Output.append(0)
            else:
                Output.append(1)
        return Output

    def GetWeightAmount(self):
        Sum = 0
        for i in range(len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                Sum += len(self.HiddenLayers[i].Neurons[j].Weights)

        for j in range(len(self.OutLayer.Neurons)):
            Sum += len(self.OutLayer.Neurons[j].Weights)
        return Sum
