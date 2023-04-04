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
Currently this project creates a random graph called "map", a few "couriers" and logistical "hubs".
Guring the runtime every node has a chance of becoming a "request".
Couriers move to random logistical hub, and then fulfill random request.
To the left will be some profiling data.
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
![image](https://user-images.githubusercontent.com/55761576/229723249-2a567b6b-9284-4a3a-8313-53a6d85c056c.png)
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
To change amount of couriers that are on a map, in main.py find line that says:
```
field.addCouriers('Clone Trooper', "random to random to random", 4)
```
And set the number you wnat isntead of 4
### Change AI Type
To change amount of couriers that are on a map, in main.py find line that says:
```
field.addCouriers('Clone Trooper', "random to random to random", 4)
```
And change the "random to random to random" to one of the folowing:
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
