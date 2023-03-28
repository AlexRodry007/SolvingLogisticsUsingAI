import networkx as nx
from matplotlib import pyplot as plt, animation as animation
import random

import Courier
import Hive
import Hub
import Requests


class Field:
    def __init__(self, map):
        self.map = map
        self.passiveCouriers = list()

    def addPassiveCourier(self, courierName, aiName, node):
        self.passiveCouriers.append((courierName, aiName, node))


class FieldVisualiser:
    def __init__(self, field):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.activeCouriers = list()
        self.activeRequests = list()
        self.activeHubs = list()
        self.ax = None
        self.pos = None

    def addRequest(self, node, serviceRequest):
        self.activeRequests.append(Requests.Request(node, serviceRequest, self.pos, self.ax))

    def addHub(self, node, services):
        self.activeHubs.append(Hub.Hub(node, services, self.pos, self.ax))

    def addRandomRequest(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addRequest(target, "Test")

    def addRandomHub(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addHub(target, ['Test'])

    def visualiseField(self):
        fig, self.ax = plt.subplots()
        self.pos = nx.spring_layout(self.field.map)
        edges = self.field.map.edges()
        colors = [self.field.map[u][v]['color'] for u, v in edges]
        nx.draw_networkx(self.field.map, self.pos, edge_color=colors)
        hivemind = Hive.Hivemind(self)

        # ADHOC D
        for _ in range(10):
            self.addRandomRequest()
        for _ in range(3):
            self.addRandomHub()
        # ADHOC U

        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(Courier.Courier(passiveCourier[0], passiveCourier[1], self.pos, passiveCourier[2],
                                                       self.ax, hivemind))

        def tickField(frame):
            for courier in self.activeCouriers:
                courier.iterateCourier()
                # ADHOC D
            if len(self.activeRequests) < 10:
                self.addRandomRequest()
                # ADHOC U

        ani = animation.FuncAnimation(fig=fig, func=tickField, frames=60, interval=25)
        plt.show()
