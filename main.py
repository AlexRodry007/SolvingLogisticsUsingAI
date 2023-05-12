import random

import Field
import Map
import Requests


if __name__ == '__main__':
    random.seed(0)
    field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=10, amountOfEdges=15))
    Map.MapCreator.randomiseWeights(field.map, 25, 100)

    field.addRandomPassiveHubs(2, ["Test"])

    field.addCouriers('Clone Trooper', "simple analytical", 2)

    mainRequestGenerator = Requests.RequestGenerator(1, 3000, ["Test"])
    field.addRequestGenerator(mainRequestGenerator)

    FV = Field.FieldVisualiser(field)
    FV.visualiseField()
