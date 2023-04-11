import time

import networkx as nx
from matplotlib import pyplot as plt, animation as animation
import random

import Courier
import Hive
import Hub
import Profiling
import Requests


class Field:
    def __init__(self, map):
        self.map = map
        self.passiveCouriers = list()
        self.passiveHubs = list()
        self.requestGenerators = list()

    def addPassiveCourier(self, courierName, aiName, node):
        self.passiveCouriers.append((courierName, aiName, node))

    def addPassiveHub(self, node, services):
        self.passiveHubs.append((node, services))

    def addRandomPassiveHubs(self, amount, services):
        for _ in range(amount):
            while True:
                allNodes = list(self.map.adj.keys())
                randomNode = allNodes[random.randint(0, len(allNodes) - 1)]
                if randomNode not in self.passiveHubs:
                    break
            self.addPassiveHub(randomNode, services)

    def addRequestGenerator(self, requestGenerator):
        self.requestGenerators.append(requestGenerator)

    def addCouriers(self, courierName, aiName, amount):
        for _ in range(amount):
            allNodes = list(self.map.adj.keys())
            randomNode = allNodes[random.randint(0, len(allNodes) - 1)]
            self.addPassiveCourier(courierName, aiName, randomNode)


class FieldVisualiser:
    def __init__(self, field):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.passiveHubs = self.field.passiveHubs
        self.activeCouriers = list()
        self.activeRequests = list()
        self.activeHubs = list()
        self.ax = None
        self.pos = None
        self.fig = None
        self.axes = None
        self.profilingAx = None

    def addRequest(self, node, serviceRequest):
        self.activeRequests.append(Requests.Request(node, serviceRequest, self.pos, self.ax))

    def addHub(self, node, services):
        self.activeHubs.append(Hub.Hub(node, services, self.pos, self.ax))

    def addRandomRequest(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addRequest(target, "Test")

    def addRandomActiveHub(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addHub(target, ['Test'])

    def generateRequests(self):
        for node in list(self.field.map.adj.keys()):
            for requestGenerator in self.field.requestGenerators:
                possibleRequest = requestGenerator.generateRequest(node, self.pos, self.ax)
                if possibleRequest is not None:
                    self.activeRequests.append(possibleRequest)

    def hideCourierMovement(self, event):
        for courier in self.activeCouriers:
            courier.courierMovement.animated = False

    def showCourierMovement(self, event):
        for courier in self.activeCouriers:
            courier.courierMovement.animated = True

    def visualiseField(self):
        gs_kw = dict(width_ratios=[1, 2])
        self.fig, self.axes = plt.subplots(ncols=2, gridspec_kw=gs_kw)
        plt.tight_layout()
        self.profilingAx = self.axes[0]
        self.ax = self.axes[1]
        self.profilingAx.get_xaxis().set_visible(False)
        self.profilingAx.get_yaxis().set_visible(False)
        profiler = Profiling.Profiling(self.profilingAx, self)
        self.pos = nx.spring_layout(self.field.map)
        edges = self.field.map.edges()
        colors = [self.field.map[u][v]['color'] for u, v in edges]
        nx.draw_networkx(self.field.map, self.pos, edge_color=colors)
        hivemind = Hive.Hivemind(self)
        profiler.startingText()

        self.ax.set_visible(False)

        # ADHOC manual hubs and requests D
        # for _ in range(10):
        #     self.addRandomRequest()
        # for _ in range(3):
        #    self.addRandomActiveHub()
        # ADHOC U

        for passiveHub in self.passiveHubs:
            self.addHub(passiveHub[0], passiveHub[1])

        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(
                Courier.Courier(passiveCourier[0], passiveCourier[1], self.pos, passiveCourier[2],
                                self.ax, hivemind))

        changedCouriers = []

        def init_tick():
            everything = []
            everything.extend(self.ax.get_children())
            everything.extend(self.profilingAx.get_children())
            return everything

        @Profiling.timeTracker(Profiler=profiler)
        def tickField(frame):
            for courier in self.activeCouriers:
                changedCouriers.append(courier.iterateCourier())
            self.generateRequests()
            profiler.tickProfiling()

            # ADHOC manual request update D
            # if len(self.activeRequests) < 10:
            #    self.addRandomRequest()
            # ADHOC U

        delayCap = 0
        ani = animation.FuncAnimation(fig=self.fig,
                                      func=tickField,
                                      frames=1,
                                      # init_func=None,
                                      interval=delayCap,
                                      repeat_delay=delayCap,
                                      blit=False,
                                      repeat=True)
        # self.fig.canvas.flush_events()
        # self.fig.canvas.draw()
        plt.show()
