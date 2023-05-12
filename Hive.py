import Courier
import random
import networkx
import copy


class Hivemind:
    def __init__(self, fieldVisualiser):
        self.fieldVisualiser = fieldVisualiser
        self.allShortestPaths = self.calculateAllShortestPaths()

    def getCommands(self, courier):
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
            pass

    def directMoveToTarget(self, courier):
        if courier.courierAi.currentNode != courier.courierAi.currentTargetNode:
            courier.courierMovement.startMovementToCoord(
                self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][0],
                self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][1],
                self.fieldVisualiser.field.map[courier.courierAi.currentNode][
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
                request.deleteRequest()
                courier.carryingService = None
                self.fieldVisualiser.receiveRequest(request)
                courier.courierAi.freeze += providedService
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

    def buildPathDijkstra(self, courier):
        courier.courierAi.courierPath = (
            list(networkx.dijkstra_path(self.fieldVisualiser.field.map, courier.courierAi.currentNode,
                                        courier.courierAi.finalTargetNode)))

    def getPathFromAllShortestPaths(self, courier):
        courier.courierAi.courierPath = self.getPathToNode(courier.courierAi.currentNode,
                                                           courier.courierAi.finalTargetNode)

    def followPath(self, courier):
        if courier.courierMovement.ticksOfMovementLeft == 0:
            if courier.courierAi.courierPath:
                courier.courierAi.currentTargetNode = courier.courierAi.courierPath.pop(0)
            self.directMoveToTarget(courier)

    def moveToFinalNodeDijkstra(self, courier):
        if courier.noPathAndMovement():
            self.buildPathDijkstra(courier)
        self.followPath(courier)

    def moveToFinalNode(self, courier):
        if courier.noPathAndMovement():
            self.getPathFromAllShortestPaths(courier)
        self.followPath(courier)

    def calculateAllShortestPaths(self):
        graph = self.fieldVisualiser.field.map
        result = dict()
        for i in range(graph.number_of_nodes()):
            length, path = networkx.single_source_dijkstra(graph, i)
            result[i] = (length, path)
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
