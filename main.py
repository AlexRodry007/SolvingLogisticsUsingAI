import random
import numpy as np
import matplotlib.pyplot as plt

import Hive
import ppo
import environment
import BuildAndTest
import Field
import Map
import Requests

if __name__ == '__main__':
    # Simple analytical
    # random.seed(0)
    # field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=100, amountOfEdges=150))
    # Map.MapCreator.randomiseWeights(field.map, 25, 100)
    #
    # field.addRandomPassiveHubs(20, ["Test"])
    #
    # field.addCouriers('Clone Trooper', "simple analytical", 20)
    #
    # mainRequestGenerator = Requests.RequestGenerator(1, 3000, ["Test"])
    # field.addRequestGenerator(mainRequestGenerator)
    #
    # FV = Field.FieldVisualiser(field)
    # FV.visualiseField()

    # Complex analytical (calculated only)
    # 3 vertexes
    # BuildAndTest.runComplexAnalyticalAgent(amountOfNodes=3, amountOfEdges=2, couriersAmount=1, hubsAmount=1)
    # 10 vertexes
    for _ in range(10):
        BuildAndTest.runComplexAnalyticalAgent(seed=3, addCarryingBit=True, outOf=1500)
    # 100 vertexes
    # BuildAndTest.runComplexAnalyticalAgent(amountOfNodes=100, amountOfEdges=150, hubsAmount=20,
    #                                        couriersAmount=20, totalSteps=160000)

    # ppo (calculated only)
    # 3 vertexes
    # BuildAndTest.runPpoAgent(amountOfNodes=3, amountOfEdges=2, couriersAmount=1, hubsAmount=1, checkpointDir='tmp/ppo')
    # 10 vertexes
    # BuildAndTest.runPpoAgent(amountOfNodes=10, amountOfEdges=15, couriersAmount=2, hubsAmount=2,
    #                          actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
    #                          N=16, batchSize=40, numberOfSteps=2400, addCarryingBit=True, seed=3,
    #                          checkpointDir='tmp/ppo', numberOfGames=1000, outOf=1500, alpha=0.00006,
    #                          entropyRegularizationMagnitude=0.02, oneStepBehind=True)

    # 100 vertexes
    # BuildAndTest.runPpoAgent(amountOfNodes=100, amountOfEdges=150, couriersAmount=20, hubsAmount=20,
    #                          N=160, batchSize=400, numberOfSteps=24000, numberOfGames=1000, addCarryingBit=True,
    #                          checkpointDir='tmp/ppo')

    # Load and train (calculated only)
    # BuildAndTest.loadAndRunPpoAgent(amountOfNodes=10, amountOfEdges=15, couriersAmount=2, hubsAmount=2,
    #                                 actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
    #                                 N=16, batchSize=40, numberOfSteps=2400, addCarryingBit=True, seed=3,
    #                                 checkpointDir='tmp/ppo', numberOfGames=1000, outOf=1500, alpha=0.00006,
    #                                 entropyRegularizationMagnitude=0.02, oneStepBehind=True)

    # Complex analytical visualised
    # BuildAndTest.visualiseComplexAnalytical(seed=3,  amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
    #                                         addCarryingBit=True, oneStepBehind=False)

    # Load and test agent
    # BuildAndTest.testLoadedAgent(amountOfNodes=10, amountOfEdges=15, couriersAmount=2, hubsAmount=2,
    #                              actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
    #                              numberOfSteps=2400, addCarryingBit=True, seed=3,
    #                              loadFrom='tmp/ppo', outOf=1500, oneStepBehind=True)
    #
    # BuildAndTest.testLoadedAgent(amountOfNodes=10, amountOfEdges=15, couriersAmount=2, hubsAmount=2,
    #                              actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
    #                              numberOfSteps=2400, addCarryingBit=True, seed=3,
    #                              loadFrom='perm/10NodesRight', outOf=1500, oneStepBehind=True)

    # Visualise agent
    # BuildAndTest.visualiseLoadedAgent(amountOfNodes=10, amountOfEdges=15, couriersAmount=2, hubsAmount=2,
    #                                   actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
    #                                   addCarryingBit=True, seed=3, loadFrom='tmp/ppo',
    #                                   outOf=1500, oneStepBehind=True)
