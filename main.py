import Map

if __name__ == '__main__':
    field = Map.Field(Map.MapCreator.createRandomMap(amountOfNodes=50))
    field.addCourier("Alex", "RandomAi", 1)
    field.addCourier("Berta", "RandomAi", 2)
    field.addCourier("Charlie", "RandomAi", 3)
    field.addCourier("Daisy", "RandomAi", 4)
    field.addCourier("Eve", "RandomAi", 5)
    field.addCourier("Frank", "RandomAi", 6)
    field.addCourier("Greg", "RandomAi", 7)
    field.addCourier("Harold", "RandomAi", 8)
    field.addCourier("Ivan", "RandomAi", 9)
    field.addCourier("Jessie", "RandomAi", 10)

    FV = Map.FieldVisualiser(field)
    FV.visualiseField()
