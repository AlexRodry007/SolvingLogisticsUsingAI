# Solving Logistics Using AI
This is a project that aims at solving some problem of logistics using neural networks and machine learning
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Illustration](#illustration)
* [How to change stuff](#how-to-change-stuff)
* [Project Status](#project-status)
## General info
Currently this project creates a random graph called "map" and ten "couriers". 
Those couriers move from node to node randomly, at random speeds independently from one-another.
## Technologies
Project is created with:
* Pillow	9.4.0	
* contourpy	1.0.7	
* cycler	0.11.0	
* fonttools	4.39.2	
* importlib-resources	5.12.0 
* kiwisolver	1.4.4	
* matplotlib	3.7.1	
* networkx	3.0
* numpy	1.24.2	
* packaging	23.0	
* pip	22.3.1	
* pyparsing	3.0.9	
* python-dateutil	2.8.2	
* setuptools	65.5.1	
* six	1.16.0	
* wheel	0.38.4	
* zipp	3.15.0	
## Setup
To run this project, install it locally, then open using IDE of your choice (https://www.jetbrains.com/pycharm/ for example), and run 'main'.
## Illustration
If everything is set up correctly, it should look somewhat like this:
![image](https://user-images.githubusercontent.com/55761576/228178925-8e2851ce-bb83-451b-8f02-269a97cd1437.png)
## How to change stuff
### Change amount of nodes
To change amount of nodes that are in a graph, in main.py find line that says:
```
field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=50, amountOfEdges=75))
```
And the set number you want instead of 50
### Change amount of edges
To change amount of edges that are in a graph, in main.py find line that says:
```
field = Field.Field(Map.MapCreator.createRandomMap(amountOfNodes=50, amountOfEdges=75))
```
And the set number you want instead of 75
### Change amount of couriers
At the time of writing, the program creates 10 couriers at nodes 1 to 10, represented by the folowing code:
```
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
```
To change amount of couriers you can delete or add lines 
```
field.addCourier([Courier Name], [Ai Name], [Starting Node])
```
First argument currently does nothing.
You can read about second argument lower
### AI Names
* **"random"** - courier will move to the random neighbors every time
* **"complex random"** - courier will choose random node and move to it
* **"random to random"** - courier will go to the random request point, delivering them with no need to resupply
* **"random to random to random"** - courier will go to the random hub, picking up service and delivering it to the random request
### Change courier speed
To change amount of ticks that couriers needs to reach their target, in main.py find line that says:
```
Map.MapCreator.randomiseWeights(field.map, 25, 100)
```
First number is minimal ticks needed to reach the target, second is maximal ticks needed.
## Project Status
The project is in an early stages of development
