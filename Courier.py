import networkx as nx
import random


class CourierMovement:

    def __init__(self, xCoord, yCoord, pyplotAx):
        self.x = xCoord
        self.y = yCoord
        self.xVelocity = 0
        self.yVelocity = 0
        self.ticksOfMovementLeft = 0

        self.ax = pyplotAx
        self.dot, = self.ax.plot(self.x, self.y, 'ro', zorder=5)

    def moveTo(self, xCoord, yCoord):
        self.x = xCoord
        self.y = yCoord
        self.dot.set_xdata(xCoord)
        self.dot.set_ydata(yCoord)

    def startMovementToCoord(self, xTargetCoord, yTargetCoord, ticksToReachTarget):
        self.xVelocity = (xTargetCoord-self.x)/ticksToReachTarget
        self.yVelocity = (yTargetCoord-self.y)/ticksToReachTarget
        self.ticksOfMovementLeft = ticksToReachTarget

    def stopMovementToCoord(self):
        self.xVelocity = 0
        self.yVelocity = 0
        self.ticksOfMovementLeft = 0

    def iterateMovement(self):
        if self.ticksOfMovementLeft > 0:
            self.moveTo(self.x+self.xVelocity, self.y+self.yVelocity)
            self.ticksOfMovementLeft -= 1
        else:
            self.stopMovementToCoord()


class Courier:
    def __init__(self, courierName, aiName, map, pos, currentNode, pyplotAx):
        self.name = courierName
        self.courierMovement = CourierMovement(pos[currentNode][0], pos[currentNode][1], pyplotAx)
        self.courierAi = CourierAi(aiName, self.courierMovement, map, pos, currentNode)

    def iterateCourier(self):
        self.courierAi.iterateAi()
        self.courierMovement.iterateMovement()


class CourierAi:

    def __init__(self, name, courierMovement, map, pos, currentNode):
        self.name = name
        self.courierMovement = courierMovement
        self.pos = pos
        self.currentNode = currentNode
        self.map = map

    def startMovementToNode(self, targetNode, ticksToReachTarget):
        self.courierMovement.startMovementToCoord(self.pos[targetNode][0], self.pos[targetNode][1], ticksToReachTarget)

    def iterateAi(self):
        self.randomAi()

    def randomAi(self):
        TICKS_TO_REACH_TARGET_MAGIC_NUMBER = random.randint(25, 75)
        if self.courierMovement.ticksOfMovementLeft == 0:
            neighbours = self.map.adj[self.currentNode]
            # print(neighbours)
            self.currentNode = list(neighbours.keys())[random.randint(0, len(neighbours)-1)]
            self.startMovementToNode(self.currentNode, TICKS_TO_REACH_TARGET_MAGIC_NUMBER)
