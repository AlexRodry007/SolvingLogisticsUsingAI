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

    def addPassiveCourier(self, courierName, aiName, node, oneStepBehind=False):
        self.passiveCouriers.append((courierName, aiName, node, oneStepBehind))

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

    def addCouriers(self, courierName, aiName, amount, oneStepBehind=False):
        for _ in range(amount):
            allNodes = list(self.map.adj.keys())
            randomNode = allNodes[random.randint(0, len(allNodes) - 1)]
            self.addPassiveCourier(courierName, aiName, randomNode, oneStepBehind)


class MetaFieldCalculator:
    def __init__(self, field, addCarryingBit=False):
        self.field = field
        self.passiveCouriers = self.field.passiveCouriers
        self.passiveHubs = self.field.passiveHubs
        self.activeCouriers = list()
        self.activeRequests = list()
        self.totalReceivedRequests = 0
        self.activeHubs = list()
        self.allShortestPaths = self.calculateAllShortestPaths()
        self.addCarryingBit = addCarryingBit

    def calculateAllShortestPaths(self):
        graph = self.field.map
        result = dict()
        for i in range(graph.number_of_nodes()):
            length, path = nx.single_source_dijkstra(graph, i)
            result[i] = (length, path)
        return result

    def receiveRequest(self, request):
        if not request.delayedDeletion:
            self.activeRequests.remove(request)
        self.totalReceivedRequests += 1

    def addRandomRequest(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addRequest(target, "Test")

    def addRandomActiveHub(self):
        allNodes = list(self.field.map.adj.keys())
        target = allNodes[random.randint(0, len(allNodes) - 1)]
        self.addHub(target, ['Test'])

    def encodeNodes(self, listOfNodeIds):
        result = list()
        for node in list(self.field.map.adj.keys()):
            result.append(1 if node in listOfNodeIds else 0)
        return result

    def observeForCourier(self, courierId):
        courier = self.activeCouriers[courierId]
        dictOfShortestPaths = self.allShortestPaths[courier.courierAi.currentNode][0]
        myKeys = list(dictOfShortestPaths.keys())
        myKeys.sort()
        sorted_dict = {i: dictOfShortestPaths[i] for i in myKeys}
        listOfShortestPaths = list(sorted_dict.values())
        maxx = max(listOfShortestPaths)
        listOfShortestPathsNormalizedAgainstTheMaximum = [float(i) / maxx for i in listOfShortestPaths]
        # print(listOfShortestPaths)
        # print(listOfShortestPathsNormalizedAgainstTheMaximum)
        # input()
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
        if self.addCarryingBit:
            if not courier.carryingService:
                observation.append(0)
            else:
                observation.append(1)
        return observation

    def killRequests(self):
        length = len(self.activeRequests)
        i = 0
        while i < length:
            request = self.activeRequests[i]
            if request.delayedDeletion:
                self.activeRequests.remove(request)
                request.deleteRequest()
                length -= 1
            else:
                i += 1

    def showAllData(self):
        print("Couriers are at", [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers])
        print("Requests are at", [activeRequest.node for activeRequest in self.activeRequests])
        print("Hubs are at", [activeHub.node for activeHub in self.activeHubs])
        print("Targets are", [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers])

    def addHub(self, target, param):
        pass

    def addRequest(self, target, param):
        pass


class FieldCalculator(MetaFieldCalculator):
    def __init__(self, field, addCarryingBit=False):
        super().__init__(field, addCarryingBit)
        self.previousVisitedHubs = 0
        self.totalVisitedHubs = 0
        self.previousReceivedRequests = 0
        self.previousTicks = 0
        self.totalTicks = 0
        self.courierId = 0

    def addRequest(self, node, serviceRequest):
        self.activeRequests.append(Requests.Request(node, serviceRequest))

    def addHub(self, node, services):
        self.activeHubs.append(Hub.Hub(node, services))

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
                                oneStepBehind=passiveCourier[3], fieldCalculator=self,
                                hivemind=hivemind))

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
        # if self.totalTicks-self.previousTicks != 0:
        #     reward = self.calculateReward()
        #     self.previousReceivedRequests = self.totalReceivedRequests
        #     self.previousTicks = self.totalTicks
        # else:
        #     reward = 0
        # # if reward!=0:
        # #    print("Reward is", reward)
        reward = self.calculateReward()
        self.previousTicks = self.totalTicks
        self.previousReceivedRequests = self.totalReceivedRequests
        self.previousVisitedHubs = self.totalVisitedHubs
        return reward

    def calculateReward(self):
        if self.totalReceivedRequests == self.previousReceivedRequests and \
                self.totalVisitedHubs == self.previousVisitedHubs:
            punishment = (self.totalTicks-self.previousTicks)/500
        else:
            punishment = 0
        return (self.totalReceivedRequests-self.previousReceivedRequests)*2\
            + (self.totalVisitedHubs-self.previousVisitedHubs)*2\
            - punishment


class FieldVisualiser(MetaFieldCalculator):
    def __init__(self, field, hasAi=False, agent=None, addCarryingBit=False):
        super().__init__(field, addCarryingBit)
        self.ax = None
        self.pos = None
        self.fig = None
        self.axes = None
        self.profilingAx = None
        self.hasAi = hasAi
        self.agent = agent

    def addRequest(self, node, serviceRequest):
        self.activeRequests.append(Requests.Request(node, serviceRequest, ax=self.ax, pos=self.pos))

    def addHub(self, node, services):
        self.activeHubs.append(Hub.Hub(node, services, pyplotAx=self.ax, pos=self.pos))

    def hideCourierMovement(self, event):
        for courier in self.activeCouriers:
            courier.courierMovement.animated = False

    def showCourierMovement(self, event):
        for courier in self.activeCouriers:
            courier.courierMovement.animated = True

    def generateRequests(self):
        for node in list(self.field.map.adj.keys()):
            for requestGenerator in self.field.requestGenerators:
                possibleRequest = requestGenerator.generateRequest(node, self.pos, self.ax)
                if possibleRequest is not None:
                    self.activeRequests.append(possibleRequest)

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
        i=0
        for passiveHub in self.passiveHubs:
            self.addHub(passiveHub[0], passiveHub[1])
            # print(self.activeHubs[i].node)
            i+=1

        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(
                Courier.Courier(passiveCourier[0], passiveCourier[1], self.pos, passiveCourier[2],
                                self.ax, hivemind, oneStepBehind=passiveCourier[3], fieldCalculator=self))

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
                        # print(observation)
                        action = self.agent.choose_action(observation)
                        # print(action)
                        changedCouriers.append(courier.iterateCourier(action=action))
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
