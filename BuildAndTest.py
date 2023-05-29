import random

import numpy as np
import matplotlib.pyplot as plt

import Field
import Map
import Requests
import Hive
import ppo
import environment


def runComplexAnalyticalAgent(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
                              totalSteps=160000, chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False,
                              oneStepBehind=False):
    env = environment.Environment(seed=seed, amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges,
                                  hubsAmount=hubsAmount, couriersAmount=couriersAmount,
                                  chanceToSpawnRequest=chanceToSpawnRequest, outOf=outOf, addCarryingBit=addCarryingBit,
                                  oneStepBehind=oneStepBehind)

    observation = env.reset()
    done = False
    score = 0
    n_steps = 0
    totalTicks = 0
    while not done:
        action = Hive.Hivemind.complexAnalyticalAgent(observation)
        observation_, reward, done, info, totalTicks = env.step(action)
        n_steps += 1
        score += reward
        observation = observation_
        # if n_steps % (totalSteps / 100) == 0:
        #     print(n_steps * 100 / totalSteps, '%')
        if n_steps % totalSteps == 0:
            done = True
    print(env.fieldCalculator.totalVisitedHubs, env.fieldCalculator.previousVisitedHubs,
          env.fieldCalculator.totalReceivedRequests, env.fieldCalculator.previousReceivedRequests)
    print('Analytical', 'score', score, 'Relative score', 1000 * (score + totalTicks / 1000) / totalTicks)


def runPpoAgent(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
                N=4, batchSize=10, n_epochs=4, alpha=0.000003, numberOfGames=300, checkpointDir='tmp/ppo',
                actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
                numberOfSteps=800, chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False,
                entropyRegularizationMagnitude=0, oneStepBehind=False):
    env = environment.Environment(seed=seed, amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges,
                                  hubsAmount=hubsAmount, couriersAmount=couriersAmount,
                                  chanceToSpawnRequest=chanceToSpawnRequest, outOf=outOf, addCarryingBit=addCarryingBit,
                                  oneStepBehind=oneStepBehind)

    N = N
    batch_size = batchSize
    n_epochs = n_epochs
    alpha = alpha
    agent = ppo.Agent(n_actions=env.amountOfNodes, batch_size=batch_size,
                      alpha=alpha, n_epochs=n_epochs,
                      actor_fc1=actor_fc1, actor_fc2=actor_fc2, critic_fc1=critic_fc1, critic_fc2=critic_fc2,
                      input_dims=(env.observationSpace,), chkpt_dir=checkpointDir,
                      entropyRegularizationMagnitude=entropyRegularizationMagnitude)
    n_games = numberOfGames

    best_score = 0
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        totalTicks = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info, totalTicks = env.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
            if n_steps % numberOfSteps == 0:
                done = True
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'Relative score', 1000 * (score + totalTicks / 1000) / totalTicks,
              'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
    x = [i + 1 for i in range(len(score_history))]
    plt.plot(x, score_history)
    plt.savefig("results.png")
    plt.show()


def loadAndRunPpoAgent(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
                       N=4, batchSize=10, n_epochs=4, alpha=0.000003, numberOfGames=300, checkpointDir='tmp/ppo',
                       actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048,
                       numberOfSteps=800, chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False,
                       entropyRegularizationMagnitude=0, oneStepBehind=False):
    env = environment.Environment(seed=seed, amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges,
                                  hubsAmount=hubsAmount, couriersAmount=couriersAmount,
                                  chanceToSpawnRequest=chanceToSpawnRequest, outOf=outOf, addCarryingBit=addCarryingBit,
                                  oneStepBehind=oneStepBehind)

    N = N
    batch_size = batchSize
    n_epochs = n_epochs
    alpha = alpha
    agent = ppo.Agent(n_actions=env.amountOfNodes, batch_size=batch_size,
                      alpha=alpha, n_epochs=n_epochs,
                      actor_fc1=actor_fc1, actor_fc2=actor_fc2, critic_fc1=critic_fc1, critic_fc2=critic_fc2,
                      input_dims=(env.observationSpace,), chkpt_dir=checkpointDir,
                      entropyRegularizationMagnitude=entropyRegularizationMagnitude)
    agent.load_models()
    n_games = numberOfGames

    best_score = 0
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        totalTicks = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info, totalTicks = env.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
            if n_steps % numberOfSteps == 0:
                done = True
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'Relative score', 1000 * (score + totalTicks / 1000) / totalTicks,
              'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
    x = [i + 1 for i in range(len(score_history))]
    plt.plot(x, score_history)
    plt.savefig("results.png")
    plt.show()


def visualiseComplexAnalytical(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
                               chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False, oneStepBehind=False):
    random.seed(seed)
    field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges))
    Map.MapCreator.randomiseWeights(field.map, 25, 100)

    field.addRandomPassiveHubs(hubsAmount, ["Test"])

    field.addCouriers('Clone Trooper', "ai", couriersAmount, oneStepBehind=oneStepBehind)

    mainRequestGenerator = Requests.RequestGenerator(chanceToSpawnRequest, outOf, ["Test"])
    field.addRequestGenerator(mainRequestGenerator)

    analyticalAgent = Hive.AnalyticalAi("complex analytical")

    FV = Field.FieldVisualiser(field, hasAi=True, agent=analyticalAgent, addCarryingBit=addCarryingBit)
    FV.visualiseField()


def visualiseLoadedAgent(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2,
                         loadFrom='tmp/ppo', chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False,
                         actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048, oneStepBehind=False):
    agent = ppo.Agent(n_actions=amountOfNodes, input_dims=(amountOfNodes * 5 + 1 if addCarryingBit else 0,),
                      chkpt_dir=loadFrom,
                      actor_fc1=actor_fc1, actor_fc2=actor_fc2, critic_fc1=critic_fc1, critic_fc2=critic_fc2)
    agent.load_models()

    random.seed(seed)
    field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges))
    Map.MapCreator.randomiseWeights(field.map, 25, 100)

    field.addRandomPassiveHubs(hubsAmount, ["Test"])

    field.addCouriers('Clone Trooper', "ai", couriersAmount, oneStepBehind=oneStepBehind)

    mainRequestGenerator = Requests.RequestGenerator(chanceToSpawnRequest, outOf, ["Test"])
    field.addRequestGenerator(mainRequestGenerator)

    FV = Field.FieldVisualiser(field, hasAi=True, agent=agent, addCarryingBit=addCarryingBit)
    FV.visualiseField()


def testLoadedAgent(seed=0, amountOfNodes=10, amountOfEdges=15, hubsAmount=2, couriersAmount=2, loadFrom='tmp/ppo',
                    numberOfTests=10, numberOfSteps=800, chanceToSpawnRequest=1, outOf=1500, addCarryingBit=False,
                    actor_fc1=2048, actor_fc2=2048, critic_fc1=2048, critic_fc2=2048, oneStepBehind=False):
    env = environment.Environment(seed=seed, amountOfNodes=amountOfNodes, amountOfEdges=amountOfEdges,
                                  hubsAmount=hubsAmount, couriersAmount=couriersAmount,
                                  chanceToSpawnRequest=chanceToSpawnRequest, outOf=outOf, addCarryingBit=addCarryingBit,
                                  oneStepBehind=oneStepBehind)
    agent = ppo.Agent(n_actions=env.amountOfNodes, input_dims=(env.observationSpace,), chkpt_dir=loadFrom,
                      actor_fc1=actor_fc1, actor_fc2=actor_fc2, critic_fc1=critic_fc1,
                      critic_fc2=critic_fc2,
                      )
    agent.load_models()
    n_games = numberOfTests

    best_score = 0
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        totalTicks = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info, totalTicks = env.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            observation = observation_
            if n_steps % numberOfSteps == 0:
                done = True

        print('episode', i, 'score %.1f' % score, 'Relative score', 1000 * (score + totalTicks / 1000) / totalTicks)
