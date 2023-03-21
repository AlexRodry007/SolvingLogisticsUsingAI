# Solving Logistics Using AI
This is a project that aims at solving some problem of logistics using neural networks and machine learning
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
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
![image](https://user-images.githubusercontent.com/55761576/226570569-deab1092-d360-4473-8fef-192a320b1d7d.png)
## How to change stuff
### Change amount of nodes
To change amount of nodes that are in a graph, in main.py find line that says (line 4 at the time of writing)
```
field = Map.Field(Map.MapCreator.createRandomMap(amountOfNodes=50))
```
And the number you want instead of 50
### Change amount of couriers
At the time of writing, the program creates 10 couriers at nodes 1 to 10, represented by the folowing code:
```
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
```
To change amount of couriers you can delete or add lines 
```
addCourier([Courier Name], [Ai Name], [Starting Node])
```
First two arguments currently do nothing.
