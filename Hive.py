import Courier
import random
import networkx
import copy
import numpy as np


class Hivemind:
    def __init__(self, fieldVisualiser):
        self.fieldVisualiser = fieldVisualiser
        self.allShortestPaths = self.calculateAllShortestPaths()

    def getCommands(self, courier, action=None):
        if courier.courierAi.name == 'random':
            self.randomHivemind(courier)
        if courier.courierAi.name == 'moveToNode test':
            courier.courierAi.finalTargetNode = 30
            self.moveToFinalNodeDijkstra(courier)
        if courier.courierAi.name == "complex random":
            self.complexRandomHivemind(courier)
        if courier.courierAi.name == "random to random":
            self.randomToRandomHivemind(courier)
        if courier.courierAi.name == "random to random to random":
            self.randomToRandomToRandomHivemind(courier)
        if courier.courierAi.name == "simple analytical":
            self.simpleAnalyticalHivemind(courier)
        if courier.courierAi.name == "ai":
            return self.aiHivemind(courier, action)

    def directMoveToTarget(self, courier):
        # print(courier.courierAi.currentNode, courier.courierAi.currentTargetNode)
        if courier.courierAi.currentNode != courier.courierAi.currentTargetNode:
            if courier.courierMovement.animated:
                courier.courierMovement.startMovementToCoord(
                    self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][0],
                    self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][1],
                    self.fieldVisualiser.field.map[courier.courierAi.currentNode][
                        courier.courierAi.currentTargetNode]
                    ['weight'])
            else:
                courier.courierMovement.startMovementToCoord(
                    ticksToReachTarget=self.fieldVisualiser.field.map[courier.courierAi.currentNode][
                        courier.courierAi.currentTargetNode]
                    ['weight'])

    def provideService(self, courier):
        nodesContainingRequests = [activeRequest.node for activeRequest in
                                   self.fieldVisualiser.activeRequests]
        onTheRequest = courier.courierAi.currentNode in nodesContainingRequests
        providedService = -1
        if onTheRequest:
            request = self.fieldVisualiser.activeRequests[
                nodesContainingRequests.index(courier.courierAi.currentNode)]
            providedService = request.receiveService(courier.carryingService)
            if providedService != -1:
                if courier.oneStepBehind:
                    request.delayedDeletion=True
                else:
                    request.deleteRequest()
                courier.carryingService = None
                self.fieldVisualiser.receiveRequest(request)
                courier.courierAi.freeze += providedService
                # print(courier.courierAi.currentNode, courier.courierAi.finalTargetNode)
        return providedService != -1

    def getService(self, courier, service):
        nodesContainingHubs = [activeHub.node for activeHub in
                               self.fieldVisualiser.activeHubs]
        onTheHub = courier.courierAi.currentNode in nodesContainingHubs
        gotService = False
        if onTheHub:
            hub = self.fieldVisualiser.activeHubs[
                nodesContainingHubs.index(courier.courierAi.currentNode)]
            gotService, ticksItTook = hub.getService(service)
            if gotService:
                courier.carryingService = service
                courier.courierAi.freeze += ticksItTook
        return gotService

    def randomHivemind(self, courier):
        if courier.courierMovement.ticksOfMovementLeft == 0:
            courier.courierAi.currentNode = courier.courierAi.currentTargetNode
            neighbours = self.fieldVisualiser.field.map.adj[courier.courierAi.currentNode]
            endNode = list(neighbours.keys())[random.randint(0, len(neighbours) - 1)]
            courier.courierAi.currentTargetNode = endNode
            self.directMoveToTarget(courier.courierAi)

    def complexRandomHivemind(self, courier):
        if len(courier.courierAi.courierPath) == 0:
            allNodes = list(self.fieldVisualiser.field.map.adj.keys())
            target = allNodes[random.randint(0, len(allNodes) - 1)]
            courier.courierAi.finalTargetNode = target
        self.moveToFinalNodeDijkstra(courier)

    def randomToRandomHivemind(self, courier):
        if len(self.fieldVisualiser.activeRequests) != 0:
            if courier.noPathAndMovement():
                self.provideService(courier)
                courier.carryingService = "Test"
                courier.courierAi.finalTargetNode = [activeRequest.node
                                                     for activeRequest
                                                     in self.fieldVisualiser.activeRequests][
                    random.randint(0, len(self.fieldVisualiser.activeRequests) - 1)]
            self.moveToFinalNodeDijkstra(courier)

    def randomToRandomToRandomHivemind(self, courier):
        if len(self.fieldVisualiser.activeRequests) != 0:
            if courier.carryingService is None and courier.noPathAndMovement():
                if self.getService(courier, "Test"):
                    courier.courierAi.finalTargetNode = [activeRequest.node
                                                         for activeRequest
                                                         in self.fieldVisualiser.activeRequests][
                        random.randint(0, len(self.fieldVisualiser.activeRequests) - 1)]
                else:
                    courier.courierAi.finalTargetNode = [activeHub.node
                                                         for activeHub
                                                         in self.fieldVisualiser.activeHubs][
                        random.randint(0, len(self.fieldVisualiser.activeHubs) - 1)]
            if courier.carryingService is not None and courier.noPathAndMovement():
                if self.provideService(courier):
                    courier.courierAi.finalTargetNode = [activeHub.node
                                                         for activeHub
                                                         in self.fieldVisualiser.activeHubs][
                        random.randint(0, len(self.fieldVisualiser.activeHubs) - 1)]
                else:
                    courier.courierAi.finalTargetNode = [activeRequest.node
                                                         for activeRequest
                                                         in self.fieldVisualiser.activeRequests][
                        random.randint(0, len(self.fieldVisualiser.activeRequests) - 1)]
            self.moveToFinalNodeDijkstra(courier)

    def simpleAnalyticalHivemind(self, courier):
        currentNode = courier.courierAi.currentNode
        if len(self.fieldVisualiser.activeRequests) != 0:
            if courier.carryingService is None and courier.noPathAndMovement():
                if self.getService(courier, "Test"):
                    courier.courierAi.finalTargetNode = self.getClosestRequestWithTag(currentNode, "Test")
                else:
                    courier.courierAi.finalTargetNode = self.getClosestHub(currentNode)
            if courier.carryingService is not None and courier.noPathAndMovement():
                if self.provideService(courier):
                    courier.courierAi.finalTargetNode = self.getClosestHub(currentNode)
                else:
                    courier.courierAi.finalTargetNode = self.getClosestRequestWithTag(currentNode, "Test")
            self.moveToFinalNode(courier)

    def aiHivemind(self, courier, action):
        # print(courier.carryingService, courier.noPathAndMovement())
        if type(action) is tuple:
            action = action[0]
        if courier.carryingService is None and courier.noPathAndMovement():
            # self.getService(courier, "Test")
            courier.courierAi.finalTargetNode = action
            # self.moveToFinalNode(courier)
            return False
        elif courier.carryingService is not None and courier.noPathAndMovement():
            # self.provideService(courier)
            courier.courierAi.finalTargetNode = action
            # self.moveToFinalNode(courier)
            return False
        else:
            # self.moveToFinalNode(courier)
            pass
        return True

    def provideOrGetService(self, courier):
        # print(courier.carryingService, courier.noPathAndMovement())
        if courier.carryingService is None and courier.noPathAndMovement():
            # print("getting service")
            gotService = self.getService(courier, "Test")
            if gotService and hasattr(self.fieldVisualiser, 'totalVisitedHubs'):
                self.fieldVisualiser.totalVisitedHubs += 1
        elif courier.carryingService is not None and courier.noPathAndMovement():
            # print("providing service")
            self.provideService(courier)

    @staticmethod
    # Ця функція готує дані та запускає відповідний алгоритм
    def complexAnalyticalAgent(observation):
        # Перевіряємо наявність біту перевезень
        if len(observation) % 5 == 1:
            # Якщо він існує - прибираємо його з масиву, та запам'ятовуємо значення
            carryingBit = observation.pop(-1)
        else:
            # Якщо його не існує - запам'ятовуємо це
            carryingBit = -1
        # Розділяємо масив на п'ять підмасивів
        splited = [list(array) for array in np.array_split(observation, 5)]

        # Індекс елементу зі значенням нуль відповідає пото
        currentNode = splited[0].index(0)

        # Запускаємо алгоритм відповідно до наявності біту перевезень
        if carryingBit == -1:
            return Hivemind.ComplexAnalyticalWithoutCarryingBit(splited, currentNode)
        else:
            return Hivemind.ComplexAnalyticalWithCarryingBit(splited, currentNode, carryingBit)

    @staticmethod
    def ComplexAnalyticalWithoutCarryingBit(splited, currentNode):
        if splited[2][currentNode] == 1:
            possibleTargets = list()
            request = 0
            for isRequest in splited[1]:
                if splited[4][request] == 0 and isRequest == 1:
                    possibleTargets.append(request)
                request += 1
            if not possibleTargets:
                return currentNode
            target = possibleTargets[0]
            closest = splited[0][target]

            for possibleTarget in possibleTargets:
                if splited[0][possibleTarget] < closest:
                    closest = splited[0][possibleTarget]
                    target = possibleTarget
            return target
        else:
            possibleTargets = list()
            hub = 0
            for isHub in splited[2]:
                if isHub == 1:
                    possibleTargets.append(hub)
                hub += 1
            # print(currentNode)
            # print(splited[0])
            # print(possibleTargets)

            target = possibleTargets[0]
            closest = splited[0][target]
            for possibleTarget in possibleTargets:
                # print(possibleTarget, splited[0][possibleTarget])
                if splited[0][possibleTarget] < closest:
                    closest = splited[0][possibleTarget]
                    target = possibleTarget
            # print(target)
            # input()
            return target

    @staticmethod
    # Ця функція аналітично визначає ціль, для кур'єра
    def ComplexAnalyticalWithCarryingBit(splited, currentNode, carryingBit):
        # Якщо кур'єр перевози ть товар
        if carryingBit == 1:
            # Підготовуємо дані
            possibleTargets = list()
            request = 0

            # Для усіх вузлів
            for isRequest in splited[1]:
                # Якщо на вузлі є запит, та він не є вже ціллю кур'єра
                if splited[4][request] == 0 and isRequest == 1:
                    # Додаємо вузол як потенційну ціль
                    possibleTargets.append(request)
                request += 1
            # Якщо потенційних цілей немає - кур'єр залишається на поточній позиції
            if not possibleTargets:
                return currentNode

            # Встановлюємо перший потенційний вузол як ціль
            target = possibleTargets[0]

            # Запам'ятовуємо відстань до цілі
            closest = splited[0][target]

            # Для кожної потенційної цілі
            for possibleTarget in possibleTargets:
                # Якщо відстань до потенційної цілі менше ніж до поточної
                if splited[0][possibleTarget] < closest:
                    # Встановлюємо нову відстань та ціль
                    closest = splited[0][possibleTarget]
                    target = possibleTarget
            # Повертаємо ціль
            return target
        # Якщо кур'єр не перевозить товар
        else:
            # Підготовуємо дані
            possibleTargets = list()
            hub = 0

            # Для усіх вузлів
            for isHub in splited[2]:
                # Якщо на вузлі є депо
                if isHub == 1:
                    # Додаємо вузол як потенційну ціль
                    possibleTargets.append(hub)
                hub += 1

            # Встановлюємо перший потенційний вузол як ціль
            target = possibleTargets[0]

            # Запам'ятовуємо відстань до цілі
            closest = splited[0][target]

            # Для кожної потенційної цілі
            for possibleTarget in possibleTargets:
                # Якщо відстань до потенційної цілі менше ніж до поточної
                if splited[0][possibleTarget] < closest:
                    # Встановлюємо нову відстань та ціль
                    closest = splited[0][possibleTarget]
                    target = possibleTarget
            # Повертаємо ціль
            return target

    def buildPathDijkstra(self, courier):
        courier.courierAi.courierPath = (
            list(networkx.dijkstra_path(self.fieldVisualiser.field.map, courier.courierAi.currentNode,
                                        courier.courierAi.finalTargetNode)))

    def getPathFromAllShortestPaths(self, courier):
        courier.courierAi.courierPath = self.getPathToNode(courier.courierAi.currentNode,
                                                           courier.courierAi.finalTargetNode)
        # print(courier.courierAi.courierPath)

    def followPath(self, courier):
        if courier.courierMovement.ticksOfMovementLeft == 0:
            if courier.courierAi.courierPath:
                courier.courierAi.currentTargetNode = courier.courierAi.courierPath.pop(0)
            self.directMoveToTarget(courier)
        # else:
        #     print(courier.courierMovement.ticksOfMovementLeft)

    def moveToFinalNodeDijkstra(self, courier):
        if courier.noPathAndMovement():
            self.buildPathDijkstra(courier)
        self.followPath(courier)

    def moveToFinalNode(self, courier):
        if courier.courierAi.freeze <=0:
            if courier.courierAi.finalTargetNode is None:
                courier.courierAi.finalTargetNode = courier.courierAi.currentNode
            # print(courier.courierAi.currentNode, courier.courierAi.finalTargetNode)
            if courier.noPathAndMovement():
                self.getPathFromAllShortestPaths(courier)
            self.followPath(courier)

    # Ця функція розраховує усі найкоротші шляхи у графі
    def calculateAllShortestPaths(self):
        # Дістаємо граф із поля
        graph = self.fieldVisualiser.field.map

        # Підготовуємо змінну для запису результатів
        result = dict()

        # Для усіх вершин
        for i in range(graph.number_of_nodes()):
            # Використовуємо single_source_dijkstra
            length, path = networkx.single_source_dijkstra(graph, i)

            # Записуємо результат
            result[i] = (length, path)
        # Повертаємо результат
        return result

    def getPathToNode(self, fromNode, toNode):
        return copy.deepcopy(self.allShortestPaths[fromNode][1][toNode])

    def getClosestHub(self, fromNode):
        allHubNodes = [activeHub.node for activeHub in self.fieldVisualiser.activeHubs]
        hubsWithLengths = dict()
        for node in allHubNodes:
            hubsWithLengths[node] = self.allShortestPaths[fromNode][0][node]
        return min(hubsWithLengths, key=hubsWithLengths.get)

    def getClosestRequestWithTag(self, fromNode, service):
        allRequestNodes = list()
        for request in self.fieldVisualiser.activeRequests:
            if request.serviceRequest == service:
                allRequestNodes.append(request.node)
        requestsWithLength = dict()
        for node in allRequestNodes:
            requestsWithLength[node] = self.allShortestPaths[fromNode][0][node]
        return min(requestsWithLength, key=requestsWithLength.get)


class AnalyticalAi:
    def __init__(self, aiName):
        self.aiName = aiName

    def choose_action(self, observation):
        if self.aiName == "complex analytical":
            return Hivemind.complexAnalyticalAgent(observation)
