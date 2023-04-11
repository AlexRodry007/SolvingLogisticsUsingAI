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
        self.animated = True
        self.dot, = self.ax.plot(self.x, self.y, marker='o', color='black', zorder=5, lw=5,
                                 markersize=5, markeredgewidth=3, animated=False)

    def moveTo(self, xCoord, yCoord):
        self.x = xCoord
        self.y = yCoord
        if self.animated:
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
        return self.dot


class Courier:
    def __init__(self, courierName, aiName, pos, currentNode, pyplotAx, hivemind):
        self.name = courierName
        self.courierMovement = CourierMovement(pos[currentNode][0], pos[currentNode][1], pyplotAx)
        self.courierAi = CourierAi(aiName, self, currentNode, hivemind)
        self.carryingService = None

    def iterateCourier(self):
        self.courierAi.iterateAi()
        return self.courierMovement.iterateMovement()

    def noPathAndMovement(self):
        return len(self.courierAi.courierPath) == 0 and self.courierMovement.ticksOfMovementLeft == 0


class CourierAi:

    def __init__(self, name, courier, currentNode, hivemind):
        self.name = name
        self.courier = courier
        self.currentNode = currentNode
        self.currentTargetNode = currentNode
        self.finalTargetNode = None
        self.hivemind = hivemind
        self.courierPath = ()
        self.freeze = 0

    def iterateAi(self):
        if self.freeze <= 0:
            if self.courier.courierMovement.ticksOfMovementLeft == 0:
                self.currentNode = self.currentTargetNode
            self.hiveMindAi()
        else:
            self.freeze -= 1

    def hiveMindAi(self):
        self.hivemind.getCommands(self.courier)
