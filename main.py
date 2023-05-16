import random
import numpy as np
import matplotlib.pyplot as plt

import Hive
import ppo
import environment
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
    env = environment.Environment(seed=0,  amountOfNodes=100, amountOfEdges=150, hubsAmount=20, couriersAmount=20)

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
        if n_steps%1600 == 0:
            print(n_steps*100/160000, '%')
        if n_steps % 160000 == 0:
            done = True

    print('Analytical', 'score %.1f' % score, 'Relative score', 1000*score/totalTicks)

    # ppo (calculated only)
    env = environment.Environment(seed=0, amountOfNodes=100, amountOfEdges=150, hubsAmount=20, couriersAmount=20)

    N = 400
    batch_size = 10
    n_epochs = 4
    alpha = 0.00003
    agent = ppo.Agent(n_actions=env.amountOfNodes, batch_size=batch_size,
                      alpha=alpha, n_epochs=n_epochs,
                      input_dims=(env.observationSpace,))
    n_games = 1000

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
            if n_steps % 8000 == 0:
                done = True
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'Relative score', 1000*score/totalTicks, 'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
    x = [i + 1 for i in range(len(score_history))]
    plt.plot(x, score_history)
    plt.savefig("results.png")
    plt.show()

    # Complex analytical visualised
    # field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=10, amountOfEdges=15))
    # Map.MapCreator.randomiseWeights(field.map, 25, 100)
    #
    # field.addRandomPassiveHubs(2, ["Test"])
    #
    # field.addCouriers('Clone Trooper', "ai", 2)
    #
    # mainRequestGenerator = Requests.RequestGenerator(1, 3000, ["Test"])
    # field.addRequestGenerator(mainRequestGenerator)
    #
    # analyticalAgent = Hive.AnalyticalAi("complex analytical")
    #
    # FV = Field.FieldVisualiser(field, hasAi=True, agent=analyticalAgent)
    # FV.visualiseField()

    # Visualise agent
    # batch_size = 10
    # n_epochs = 8
    # alpha = 0.00003
    # agent = ppo.Agent(n_actions=env.amountOfNodes, batch_size=batch_size,
    #                   alpha=alpha, n_epochs=n_epochs,
    #                   input_dims=(env.observationSpace,))
    # agent.load_models()
    #
    # field = env.field
    #
    # FV = Field.FieldVisualiser(field, hasAi=True, agent=agent)
    # FV.visualiseField()



