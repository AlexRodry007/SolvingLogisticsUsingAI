import Field
import Map

if __name__ == '__main__':
    field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=50, amountOfEdges=75))
    Map.MapCreator.randomiseWeights(field.map, 25, 100)

    field.addPassiveCourier("Alex", "random to random to random", 1)
    field.addPassiveCourier("Berta", "random to random to random", 2)
    field.addPassiveCourier("Charlie", "random to random to random", 3)
    field.addPassiveCourier("Daisy", "random to random to random", 4)
    field.addPassiveCourier("Eve", "random to random to random", 5)
    field.addPassiveCourier("Frank", "random to random to random", 6)
    field.addPassiveCourier("Greg", "random to random to random", 7)
    field.addPassiveCourier("Harold", "random to random to random", 8)
    field.addPassiveCourier("Ivan", "random to random to random", 9)
    field.addPassiveCourier("Jessie", "random to random to random", 10)


    FV = Field.FieldVisualiser(field)
    FV.visualiseField()
