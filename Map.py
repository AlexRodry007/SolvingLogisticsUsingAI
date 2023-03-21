import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Courier


class MapCreator:

    @staticmethod
    def createEmptyMap():
        return nx.Graph()

    @staticmethod
    def createRandomMap(amountOfNodes=None, amountOfEdges=None):
        EDGE_CHANCE_MAGIC_NUMBER = 5
        if amountOfNodes is None and amountOfEdges is None:
            amountOfNodes = random.randint(10, 50)

        if amountOfEdges is None:
            return MapCreator.createRandomMapWithSetNodes(amountOfNodes, EDGE_CHANCE_MAGIC_NUMBER)

        if amountOfNodes is None:
            return MapCreator.createRandomMapWithSetEdges(amountOfEdges, EDGE_CHANCE_MAGIC_NUMBER)

        print("TO DO: Add function to create random map with set both edges and nodes. "
              "\nCurrently if both edges and nodes are set, only nodes are used")
        return MapCreator.createRandomMapWithSetNodes(amountOfNodes, EDGE_CHANCE_MAGIC_NUMBER)

    @staticmethod
    def createRandomMapWithSetNodes(amountOfNodes, edgeChance):
        map = nx.Graph()
        for newNode in range(amountOfNodes):
            map.add_node(newNode)
            isolatedNode = True
            for oldNode in range(newNode):
                if random.randint(0, 99) < edgeChance:
                    map.add_edge(newNode, oldNode)
                    isolatedNode = False
            if isolatedNode and newNode != 0:
                map.add_edge(newNode, random.randint(0, newNode-1))
        return map

    @staticmethod
    def createRandomMapWithSetEdges(amountOfEdges, edgeChance):
        map = nx.Graph()
        currentAmountOfEdges = 0
        currentAmountOfNodes = 0
        while currentAmountOfEdges < amountOfEdges:
            map.add_node(currentAmountOfNodes)
            currentAmountOfNodes += 1
            isolatedNode = True
            for oldNode in range(currentAmountOfNodes):
                if random.randint(0, 99) < edgeChance:
                    map.add_edge(currentAmountOfNodes, oldNode)
                    currentAmountOfEdges += 1
                    isolatedNode = False
                    if currentAmountOfEdges >= amountOfEdges:
                        break
            if isolatedNode and currentAmountOfNodes != 0:
                map.add_edge(currentAmountOfNodes, random.randint(0, currentAmountOfNodes - 1))
                currentAmountOfEdges += 1
        return map


class Field:
    def __init__(self, map):
        self.map = map
        self.passiveCouriers = list()

    def addCourier(self, courierName, aiName, node):
        self.passiveCouriers.append((courierName, aiName, node))


class FieldVisualiser:
    def __init__(self, field):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.activeCouriers = list()

    def visualiseField(self):
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.field.map)
        nx.draw_networkx(self.field.map, pos)
        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(Courier.Courier(passiveCourier[0], passiveCourier[1],
                                                       self.field.map, pos, passiveCourier[2], ax))

        def tickField(frame):
            for courier in self.activeCouriers:
                courier.iterateCourier()

        ani = animation.FuncAnimation(fig=fig, func=tickField, frames=60, interval=25)
        plt.show()




