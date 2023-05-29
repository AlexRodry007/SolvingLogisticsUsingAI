import networkx as nx
import random


class MapCreator:

    @staticmethod
    def createEmptyMap():
        return nx.Graph()

    @staticmethod
    def createRandomMap(amountOfNodes=None, amountOfEdges=None):
        EDGE_CHANCE_MAGIC_NUMBER = 5
        if amountOfNodes is None and amountOfEdges is None:
            amountOfNodes = random.randint(10, 50)

        if amountOfEdges is None:
            return MapCreator.createRandomMapWithSetNodes(amountOfNodes, EDGE_CHANCE_MAGIC_NUMBER)

        if amountOfNodes is None:
            return MapCreator.createRandomMapWithSetEdges(amountOfEdges, EDGE_CHANCE_MAGIC_NUMBER)

        return MapCreator.createRandomMapWithSetNodesAndEdges(amountOfNodes, amountOfEdges)

    @staticmethod
    def createRandomMapWithSetNodes(amountOfNodes, edgeChance):
        map = nx.Graph()
        for newNode in range(amountOfNodes):
            map.add_node(newNode)
            isolatedNode = True
            for oldNode in range(newNode):
                if random.randint(0, 99) < edgeChance:
                    map.add_edge(newNode, oldNode)
                    isolatedNode = False
            if isolatedNode and newNode != 0:
                map.add_edge(newNode, random.randint(0, newNode-1))
        return map

    @staticmethod
    def createRandomMapWithSetEdges(amountOfEdges, edgeChance):
        map = nx.Graph()
        currentAmountOfEdges = 0
        currentAmountOfNodes = 0
        while currentAmountOfEdges < amountOfEdges:
            map.add_node(currentAmountOfNodes)
            currentAmountOfNodes += 1
            isolatedNode = True
            for oldNode in range(currentAmountOfNodes):
                if random.randint(0, 99) < edgeChance:
                    map.add_edge(currentAmountOfNodes, oldNode)
                    currentAmountOfEdges += 1
                    isolatedNode = False
                    if currentAmountOfEdges >= amountOfEdges:
                        break
            if isolatedNode and currentAmountOfNodes != 0:
                map.add_edge(currentAmountOfNodes, random.randint(0, currentAmountOfNodes - 1))
                currentAmountOfEdges += 1
        return map

    @staticmethod
    # Ця функція повертає випадковий граф із кількістю вузлів та ребер на графі.
    def createRandomMapWithSetNodesAndEdges(amountOfNodes, amountOfEdges):
        # Створюємо порожній граф
        map = nx.Graph()

        # Додаємо до нього перший вузол, його номер дорівнює нулю
        map.add_node(0)

        # Якщо кількість створених вузлів відповідає заданій – завершуємо цикл
        for newNode in range(1, amountOfNodes):
            # Додаємо новий вузол
            map.add_node(newNode)

            # З’єднуємо його з випадковим існуючим вузлом
            map.add_edge(newNode, random.randint(0, newNode - 1))

        # Якщо кількість ребер більше або відповідає бажаній – завершуємо цикл
        for _ in range(amountOfNodes - 1, amountOfEdges):
            # Обираємо випадковий вузол
            firstNode = random.randint(0, amountOfNodes - 1)

            # Робимо список усіх вузлів
            allNodes = list(range(0, amountOfNodes))

            # Робимо список сусідів обраного вузла
            firstNodeNeighbors = list(map.adj[firstNode].keys())

            # Прибираємо обраний вузел зі списку усіх вузлів
            allNodes.pop(firstNode)

            # Робимо список усіх вузлів, які не є обраним вузлом, або його сусідами
            notNeighbors = [i for i in allNodes if i not in firstNodeNeighbors]

            # З'єднуємо обраний вузол із випадковим зі списку
            map.add_edge(firstNode, notNeighbors[random.randint(0, len(notNeighbors) - 1)])

        # Повертаємо отриманий граф
        return map

    @staticmethod
    # Ця функція встановлює випадкову вагу всім ребрам графа, та колір відповідно до ваги
    def randomiseWeights(graph, minWeight, maxWeight):
        # Для усіх ребер
        for edge in list(graph.edges.keys()):
            # Генеруємо випадкову вагу
            weight = random.randint(minWeight, maxWeight)

            # Аналізуємо отриману вагу
            # Якщо вага є у перший третині області - обираємо зелений колір
            if weight <= (minWeight + (maxWeight-minWeight) / 3):
                color = 'green'
            # Якщо вага є у другій третині області - обираємо зелений жовтий
            elif weight <= (minWeight + 2*(maxWeight - minWeight) / 3):
                color = 'yellow'
            # Якщо вага є у третій третині області - обираємо червоний колір
            else:
                color = 'red'

            # Встановлюємо вагу та колір ребра відповідно
            graph[edge[0]][edge[1]]['weight'] = weight
            graph[edge[0]][edge[1]]['color'] = color



