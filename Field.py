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

    # Додавання пасивного кур'єра записує необхідні дані для його створення
    def addPassiveCourier(self, courierName, aiName, node, oneStepBehind=False):
        self.passiveCouriers.append((courierName, aiName, node, oneStepBehind))

    # Додавання пасивного депо записує необхідні дані для його створення
    def addPassiveHub(self, node, services):
        self.passiveHubs.append((node, services))

    # Додавання генератора запитів дозволяє зручно їх зберігати
    def addRequestGenerator(self, requestGenerator):
        self.requestGenerators.append(requestGenerator)

    # Ця функція додає декілька пасивних депо на випадкові вузли мапи
    def addRandomPassiveHubs(self, amount, services):
        # Стільки разів, скільки необхідно депо
        for _ in range(amount):
            # Намагаємось знайти вузол, на якому ще нема депо
            while True:
                # Створюємо список усіх вузлів
                allNodes = list(self.map.adj.keys())

                # Обираємо серед них випадковий
                randomNode = allNodes[random.randint(0, len(allNodes) - 1)]

                # Якщо цього вузла нема серед тих на якому вже є депо - вузол знайдено
                if randomNode not in self.passiveHubs:
                    break
            # Додаємо пасивне депо
            self.addPassiveHub(randomNode, services)

    # Ця функція додає декілька пасивних кур'єрів на випадкові вузли мапи
    def addCouriers(self, courierName, aiName, amount, oneStepBehind=False):
        # Стільки разів, скільки необхідно кур'єрів
        for _ in range(amount):
            # Створюємо список усіх вузлів
            allNodes = list(self.map.adj.keys())

            # Обираємо серед них випадковий
            randomNode = allNodes[random.randint(0, len(allNodes) - 1)]

            # Додаємо пасивного кур'єра
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
        # Знаходимо кур'єра по номеру
        courier = self.activeCouriers[courierId]

        # Формуємо список найкоротших шляхів
        dictOfShortestPaths = self.allShortestPaths[courier.courierAi.currentNode][0]

        # Сортуємо список за номером вузлів
        myKeys = list(dictOfShortestPaths.keys())
        myKeys.sort()
        sorted_dict = {i: dictOfShortestPaths[i] for i in myKeys}

        # Записуємо довжину найкоротших шляхів
        listOfShortestPaths = list(sorted_dict.values())

        # Нормуємо список найкоротших шляхів
        maxx = max(listOfShortestPaths)
        listOfShortestPathsNormalizedAgainstTheMaximum = [float(i) / maxx for i in listOfShortestPaths]

        # Записуємо вузли на яких знаходяться важливі речі
        nodesContainingRequests = [activeRequest.node for activeRequest in self.activeRequests]
        nodesContainingHubs = [activeHub.node for activeHub in self.activeHubs]
        nodesContainingCouriers = [activeCourier.courierAi.currentNode for activeCourier in self.activeCouriers]
        nodesThatAreTargets = [activeCourier.courierAi.finalTargetNode for activeCourier in self.activeCouriers]

        # Кодуємо та записуємо спостереження
        observation = list()
        observation.extend(listOfShortestPathsNormalizedAgainstTheMaximum)
        observation.extend(self.encodeNodes(nodesContainingRequests))
        observation.extend(self.encodeNodes(nodesContainingHubs))
        observation.extend(self.encodeNodes(nodesContainingCouriers))
        observation.extend(self.encodeNodes(nodesThatAreTargets))

        # Додаємо біт перевезень, якщо він є
        if self.addCarryingBit:
            if not courier.carryingService:
                observation.append(0)
            else:
                observation.append(1)
        return observation

    def killRequests(self, courierId):
        length = len(self.activeRequests)
        i = 0
        while i < length:
            request = self.activeRequests[i]
            if request.delayedDeletion == courierId:
                self.deleteRequest(request)
                length -= 1
            else:
                i += 1

    def deleteRequest(self, request):
        self.activeRequests.remove(request)
        request.deleteRequest()

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

        i = 1
        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(
                Courier.Courier(courierName=passiveCourier[0], aiName=passiveCourier[1], currentNode=passiveCourier[2],
                                oneStepBehind=passiveCourier[3], fieldCalculator=self,
                                hivemind=hivemind, id=i))
            i+=1

    def tickField(self):
        # Ітеруємо усіх кур'єрів
        for _ in range(self.courierId, len(self.activeCouriers)):
            courier = self.activeCouriers[self.courierId]
            # Якщо кур'єр потребує команди - повертаємо спостереження
            if courier.noPathAndMovement():
                return self.observeForCourier(self.courierId)
            courier.iterateCourier()
            self.courierId += 1
        self.courierId = 0

        # Застосовуємо генератор запитів для усіх вершин
        self.generateRequests()
        self.totalTicks += 1
        return None

    def step(self, action):
        # Застосовуємо команду до поточного кур'єра, та продовжуємо симуляцію
        courier = self.activeCouriers[self.courierId]
        courier.iterateCourier(action)
        self.courierId += 1
        while True:
            # Якщо мить не поверне спостереження - в команді нема потреби
            observation = self.tickField()
            if observation is not None:
                # Якщо мить повернула спостереження - рахуємо нагороду
                reward = self.evaluate()

                # Повертаємо результати кроку
                return observation, reward, False, "nothing", self.totalTicks

    def evaluate(self):
        # Підраховуємо деякі альтернативні параметри
        self.previousTicks = self.totalTicks
        self.previousReceivedRequests = self.totalReceivedRequests
        self.previousVisitedHubs = self.totalVisitedHubs

        # Рахуємо нагороду для кур'єра
        courier = self.activeCouriers[self.courierId]
        reward = courier.reward - courier.punishment
        if courier.reward != 0:
            courier.punishment = 0
            courier.reward = 0

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

        i=0
        for passiveHub in self.passiveHubs:
            self.addHub(passiveHub[0], passiveHub[1])
            # print(self.activeHubs[i].node)
            i+=1

        i=1
        for passiveCourier in self.passiveCouriers:
            self.activeCouriers.append(
                Courier.Courier(passiveCourier[0], passiveCourier[1], self.pos, passiveCourier[2],
                                self.ax, hivemind, oneStepBehind=passiveCourier[3], fieldCalculator=self, id=i))
            i+=1

        changedCouriers = []

        def init_tick():
            everything = []
            everything.extend(self.ax.get_children())
            everything.extend(self.profilingAx.get_children())
            return everything

        @Profiling.timeTracker(Profiler=profiler)
        def tickField(frame):
            # Для сумісності зі старим кодом йде перевірка наявності агента
            if not self.hasAi:
                # Якщо агента нема, ітеруємо усіх кур'єрів
                for courier in self.activeCouriers:
                    changedCouriers.append(courier.iterateCourier())
            else:
                i = 0
                # При наявності агента, ми ітеруємо через усіх кур'єрів
                for courier in self.activeCouriers:
                    if courier.noPathAndMovement():
                        # Якщо кур'єр потребує команди - робимо спостереження
                        observation = self.observeForCourier(i)

                        # Обираємо команду в залежності від спостереження
                        action = self.agent.choose_action(observation)

                        # Ітеруємо кур'єра, даючи йому команду
                        changedCouriers.append(courier.iterateCourier(action=action))
                    else:
                        # Якщо кур'єр не потребує команди - просто ітеруємо його
                        changedCouriers.append(courier.iterateCourier())
                    i += 1

            # Застосовуємо генератор запитів для усіх вершин
            self.generateRequests()

            # Ітеруємо профілювання
            profiler.tickProfiling()

        delayCap = 0
        ani = animation.FuncAnimation(fig=self.fig,
                                      func=tickField,
                                      frames=1,
                                      # init_func=None,
                                      interval=delayCap,
                                      repeat_delay=delayCap,
                                      blit=False,
                                      repeat=True)

        plt.show()
