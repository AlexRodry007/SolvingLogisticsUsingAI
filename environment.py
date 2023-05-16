import random

import Field
import Map
import Requests


class Environment:
    def __init__(self, seed=None,
                 amountOfNodes=10, amountOfEdges=15,
                 weightsMin=25, weightsMax=100,
                 hubsAmount=2, hubsServices=None,
                 courierName="Clone Trooper", couriersAmount=2,
                 chanceToSpawnRequest=1, outOf=3000, requestServices=None):
        self.seed = seed
        self.amountOfNodes = amountOfNodes
        self.observationSpace = amountOfNodes*5
        self.amountOfEdges = amountOfEdges
        self.weightsMin = weightsMin
        self.weightsMax = weightsMax
        self.hubsAmount = hubsAmount
        self.hubsServices = hubsServices
        self.courierName = courierName
        self.couriersAmount = couriersAmount
        self.chanceToSpawnRequest = chanceToSpawnRequest
        self.outOf = outOf
        self.requestServices = requestServices
        self.field = None
        self.fieldCalculator = None

    def reset(self):
        if self.seed is not None:
            random.seed(self.seed)
        if self.hubsServices is None:
            hubsServices = ["Test"]
        else:
            hubsServices = self.hubsServices
        if self.requestServices is None:
            requestServices = ["Test"]
        else:
            requestServices = self.requestServices

        self.field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=self.amountOfNodes, amountOfEdges=self.amountOfEdges))
        Map.MapCreator.randomiseWeights(self.field.map, self.weightsMin, self.weightsMax)

        self.field.addRandomPassiveHubs(self.hubsAmount, hubsServices)

        self.field.addCouriers(self.courierName, "ai", self.couriersAmount)

        mainRequestGenerator = Requests.RequestGenerator(self.chanceToSpawnRequest, self.outOf, requestServices)
        self.field.addRequestGenerator(mainRequestGenerator)

        self.fieldCalculator = Field.FieldCalculator(self.field)
        self.fieldCalculator.start()
        # ADHOC down
        self.fieldCalculator.addRandomRequest()
        # ADHOC up
        random.seed(None)
        return self.fieldCalculator.observeForCourier(0)

    def step(self, action):
        return self.fieldCalculator.step(action)
