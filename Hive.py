import Courier
import random
import networkx


class Hivemind:
    def __init__(self, fieldVisualiser):
        self.fieldVisualiser = fieldVisualiser

    def getCommands(self, courier):
        if courier.courierAi.name == 'random':
            self.randomHivemind(courier)
        if courier.courierAi.name == 'moveToNode test':
            courier.courierAi.finalTargetNode = 30
            self.moveToFinalNode(courier)
        if courier.courierAi.name == "complex random":
            self.complexRandomHivemind(courier)
        if courier.courierAi.name == "random to random":
            self.randomToRandomHivemind(courier)
        if courier.courierAi.name == "random to random to random":
            self.randomToRandomToRandomHivemind(courier)

    def directMoveToTarget(self, courier):
        if courier.courierAi.currentNode != courier.courierAi.currentTargetNode:
            courier.courierMovement.startMovementToCoord(self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][0],
                                                         self.fieldVisualiser.pos[courier.courierAi.currentTargetNode][1],
                                                         self.fieldVisualiser.field.map[courier.courierAi.currentNode][
                                                             courier.courierAi.currentTargetNode]
                                                         ['weight'])

    def provideService(self, courier):
        nodesContainingRequests = [activeRequest.node for activeRequest in
                                   self.fieldVisualiser.activeRequests]
        onTheRequest = courier.courierAi.currentNode in nodesContainingRequests
        providedService = False
        if onTheRequest:
            request = self.fieldVisualiser.activeRequests[
                nodesContainingRequests.index(courier.courierAi.currentNode)]
            providedService = request.receiveService(courier.carryingService)
            if providedService:
                request.deleteRequest()
                courier.carryingService = None
                self.fieldVisualiser.activeRequests.remove(request)
        return providedService

    def getService(self, courier, service):
        nodesContainingHubs = [activeHub.node for activeHub in
                                   self.fieldVisualiser.activeHubs]
        onTheHub = courier.courierAi.currentNode in nodesContainingHubs
        gotService = False
        if onTheHub:
            hub = self.fieldVisualiser.activeHubs[
                nodesContainingHubs.index(courier.courierAi.currentNode)]
            gotService = hub.getService(service)
            if gotService:
                courier.carryingService = service
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
        self.moveToFinalNode(courier)

    def randomToRandomHivemind(self, courier):
        if courier.noPathAndMovement():
            self.provideService(courier)
            courier.carryingService = "Test"
            courier.courierAi.finalTargetNode = [activeRequest.node
                                                 for activeRequest
                                                 in self.fieldVisualiser.activeRequests][
                random.randint(0, len(self.fieldVisualiser.activeRequests) - 1)]
        self.moveToFinalNode(courier)

    def randomToRandomToRandomHivemind(self, courier):
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
        self.moveToFinalNode(courier)

    def buildPathDijkstra(self, courier):
        if courier.noPathAndMovement():
            courier.courierAi.courierPath = (
                list(networkx.dijkstra_path(self.fieldVisualiser.field.map, courier.courierAi.currentNode,
                                            courier.courierAi.finalTargetNode)))

    def followPath(self, courier):
        if courier.courierMovement.ticksOfMovementLeft == 0:
            courier.courierAi.currentTargetNode = courier.courierAi.courierPath.pop(0)
            self.directMoveToTarget(courier)

    def moveToFinalNode(self, courier):
        self.buildPathDijkstra(courier)
        self.followPath(courier)
