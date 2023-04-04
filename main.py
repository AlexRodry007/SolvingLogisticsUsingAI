import Field
import Map
import Requests


if __name__ == '__main__':
    field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=50, amountOfEdges=75))
    Map.MapCreator.randomiseWeights(field.map, 25, 100)

    field.addRandomPassiveHubs(4, ["Test"])

    field.addCouriers('Clone Trooper', "random to random to random", 4)

    mainRequestGenerator = Requests.RequestGenerator(1, 3500, ["Test"])
    field.addRequestGenerator(mainRequestGenerator)

    FV = Field.FieldVisualiser(field)
    FV.visualiseField()
