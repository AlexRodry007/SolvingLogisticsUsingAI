import random


class Request:
    def __init__(self, node, serviceRequest, pos=None, ax=None, ticksToServe=60):
        self.serviceRequest = serviceRequest
        self.ticksToServe = ticksToServe
        self.node = node
        self.delayedDeletion = False
        if node is None or pos is None or ax is None:
            self.animated = False
        else:
            self.animated = True
            self.x = pos[node][0]
            self.y = pos[node][1]
            self.ax = ax
            self.dot, = self.ax.plot(self.x, self.y, marker='o', color='#848ac4', zorder=0, lw=5,
                                     markersize=23, markeredgewidth=3)

    def receiveService(self, receivedService):
        if receivedService == self.serviceRequest:
            return self.ticksToServe
        else:
            return -1

    def deleteRequest(self):
        if self.animated:
            self.dot.remove()


class RequestGenerator:
    def __init__(self, chanceToSpawn, outOf, possibleServices):
        self.chanceToSpawn = chanceToSpawn
        self.outOf = outOf
        self.possibleServices = possibleServices

    def generateRequest(self, node, pos=None, ax=None):
        if random.randint(1, self.outOf) <= self.chanceToSpawn:
            service = self.possibleServices[random.randint(0, len(self.possibleServices)-1)]
            return Request(node, service, pos, ax)
