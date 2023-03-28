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
    def createRandomMapWithSetNodesAndEdges(amountOfNodes, amountOfEdges):
        map = nx.Graph()
        map.add_node(0)
        for newNode in range(1, amountOfNodes):
            map.add_node(newNode)
            map.add_edge(newNode, random.randint(0, newNode-1))
        for _ in range(amountOfNodes-1, amountOfEdges):
            firstNode = random.randint(0, amountOfNodes-1)
            allNodes = list(range(0, amountOfNodes))
            firstNodeNeighbors = list(map.adj[firstNode].keys())
            allNodes.pop(firstNode)
            notNeighbors = [i for i in allNodes if i not in firstNodeNeighbors]
            map.add_edge(firstNode, notNeighbors[random.randint(0, len(notNeighbors)-1)])
        return map

    @staticmethod
    def randomiseWeights(graph, minWeight, maxWeight):
        for edge in list(graph.edges.keys()):
            weight = random.randint(minWeight, maxWeight)
            if weight <= (minWeight + (maxWeight-minWeight) / 3):
                color = 'green'
            elif weight <= (minWeight + 2*(maxWeight - minWeight) / 3):
                color = 'yellow'
            else:
                color = 'red'
            graph[edge[0]][edge[1]]['weight'] = weight
            graph[edge[0]][edge[1]]['color'] = color




