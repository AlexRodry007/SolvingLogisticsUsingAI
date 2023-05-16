import time

import numpy as np
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


class FieldCalculator:
    def __init__(self, field):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.passiveHubs = self.field.passiveHubs
        self.activeCouriers = list()
        self.activeRequests = list()
        self.previousReceivedRequests = 0
        self.totalReceivedRequests = 0
        self.previousTicks = 0
        self.totalTicks = 0
        self.activeHubs = list()
        self.allShortestPaths = self.calculateAllShortestPaths()
        self.courierId = 0

    def calculateAllShortestPaths(self):
        graph = self.field.map
        result = dict()
        for i in range(graph.number_of_nodes()):
            length, path = nx.single_source_dijkstra(graph, i)
            result[i] = (length, path)
        return result

    def receiveRequest(self, request):
        self.activeRequests.remove(request)
        self.totalReceivedRequests += 1

    def addRequest(self, node, serviceRequest):
        self.activeRequests.append(Requests.Request(node, serviceRequest))

    def addHub(self, node, services):
        self.activeHubs.append(Hub.Hub(node, services))

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
                possibleRequest = requestGenerator.generateRequest(node)
                if possibleRequest is not None:
                    self.activeRequests.append(possibleRequest)

    def start(self):
        hivemind = Hive.Hivemind(self)
        for passiveHub in self.passiveHubs:
            self.addHub(passiveHub[0], passiveHub[1])

        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(
                Courier.Courier(courierName=passiveCourier[0], aiName=passiveCourier[1], currentNode=passiveCourier[2],
                                hivemind=hivemind))

    def encodeNodes(self, listOfNodeIds):
        result = list()
        for node in list(self.field.map.adj.keys()):
            result.append(1 if node in listOfNodeIds else 0)
        return result

    def observeForCourier(self, courierId):
        courier = self.activeCouriers[courierId]
        listOfShortestPaths = self.allShortestPaths[courier.courierAi.currentNode][0]
        summ = sum(listOfShortestPaths)
        listOfShortestPathsNormalizedAgainstTheMaximum = [float(i)/summ for i in listOfShortestPaths]
        nodesContainingRequests = [activeRequest.node for activeRequest in self.activeRequests]
        nodesContainingHubs = [activeHub.node for activeHub in self.activeHubs]
        nodesContainingCouriers = [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers]
        nodesThatAreTargets = [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers]
        observation = list()
        observation.extend(listOfShortestPathsNormalizedAgainstTheMaximum)
        observation.extend(self.encodeNodes(nodesContainingRequests))
        observation.extend(self.encodeNodes(nodesContainingHubs))
        observation.extend(self.encodeNodes(nodesContainingCouriers))
        observation.extend(self.encodeNodes(nodesThatAreTargets))
        return observation

    def tickField(self):
        for _ in range(self.courierId, len(self.activeCouriers)):
            courier = self.activeCouriers[self.courierId]
            if courier.noPathAndMovement():
                return self.observeForCourier(self.courierId)
            courier.iterateCourier()
            self.courierId += 1
        self.courierId = 0
        self.generateRequests()
        self.totalTicks += 1
        return None

    def step(self, action):
        # self.showAllData()
        # input("Press any key to continue")
        courier = self.activeCouriers[self.courierId]
        courier.iterateCourier(action)
        self.courierId += 1
        while True:
            observation = self.tickField()
            if observation is not None:
                reward = self.evaluate()
                return observation, reward, False, "idk", self.totalTicks

    def evaluate(self):
        if self.totalTicks-self.previousTicks != 0:
            reward = self.calculateReward()
            self.previousReceivedRequests = self.totalReceivedRequests
            self.previousTicks = self.totalTicks
        else:
            reward = 0
        # if reward!=0:
        #    print("Reward is", reward)
        return reward

    def calculateReward(self):
        return (self.totalReceivedRequests-self.previousReceivedRequests)-(self.totalTicks-self.previousTicks)/1000

    def showAllData(self):
        print("Couriers are at", [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers])
        print("Requests are at", [activeRequest.node for activeRequest in self.activeRequests])
        print("Hubs are at", [activeHub.node for activeHub in self.activeHubs])
        print("Targets are", [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers])


class FieldVisualiser:
    def __init__(self, field, hasAi=False, agent=None):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.passiveHubs = self.field.passiveHubs
        self.activeCouriers = list()
        self.activeRequests = list()
        self.totalReceivedRequests = 0
        self.activeHubs = list()
        self.ax = None
        self.pos = None
        self.fig = None
        self.axes = None
        self.profilingAx = None
        self.allShortestPaths = self.calculateAllShortestPaths()
        self.hasAi = hasAi
        self.agent = agent

    def calculateAllShortestPaths(self):
        graph = self.field.map
        result = dict()
        for i in range(graph.number_of_nodes()):
            length, path = nx.single_source_dijkstra(graph, i)
            result[i] = (length, path)
        return result

    def receiveRequest(self, request):
        self.activeRequests.remove(request)
        self.totalReceivedRequests += 1

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

    def encodeNodes(self, listOfNodeIds):
        result = list()
        for node in list(self.field.map.adj.keys()):
            result.append(1 if node in listOfNodeIds else 0)
        return result

    def observeForCourier(self, courierId):
        courier = self.activeCouriers[courierId]
        listOfShortestPaths = self.allShortestPaths[courier.courierAi.currentNode][0]
        summ = sum(listOfShortestPaths)
        listOfShortestPathsNormalizedAgainstTheMaximum = [float(i)/summ for i in listOfShortestPaths]
        nodesContainingRequests = [activeRequest.node for activeRequest in self.activeRequests]
        nodesContainingHubs = [activeHub.node for activeHub in self.activeHubs]
        nodesContainingCouriers = [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers]
        nodesThatAreTargets = [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers]
        observation = list()
        observation.extend(listOfShortestPathsNormalizedAgainstTheMaximum)
        observation.extend(self.encodeNodes(nodesContainingRequests))
        observation.extend(self.encodeNodes(nodesContainingHubs))
        observation.extend(self.encodeNodes(nodesContainingCouriers))
        observation.extend(self.encodeNodes(nodesThatAreTargets))
        return observation

    def showAllData(self):
        print("Couriers are at", [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers])
        print("Requests are at", [activeRequest.node for activeRequest in self.activeRequests])
        print("Hubs are at", [activeHub.node for activeHub in self.activeHubs])
        print("Targets are", [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers])

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
            if not self.hasAi:
                for courier in self.activeCouriers:
                    changedCouriers.append(courier.iterateCourier())
            else:
                i = 0
                for courier in self.activeCouriers:
                    if courier.noPathAndMovement():
                        observation = self.observeForCourier(i)
                        changedCouriers.append(courier.iterateCourier(action=self.agent.choose_action(observation)))
                        # self.showAllData()
                    else:
                        changedCouriers.append(courier.iterateCourier())
                    i += 1
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
