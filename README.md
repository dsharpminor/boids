## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is an extension to the starship vs asteroids game. The functions in it implement flocking, attacking and evading behaviours. 
	
## Technologies
Project is created with:
* Python version: 2
* Codeskulptor simplegui API

## Setup
To run this project, run 'lab2LIB.py'. 
In order to choose only one or a few type of behaviour, go to "apply_behaviour" function and comment/uncomment respective lines of code.
For instance, if you only uncomment these 3 lines of code, you will get flocking behavior.

```python
    self.acc = vector_add(self.acc, alignment)
    self.acc = vector_add(self.acc, separation)
    self.acc = vector_add(self.acc, cohesion)
```
If you add these two lines, then boids will evade both the ships and its missiles.
```python
    self.acc = vector_add(self.acc, dodge)
    self.acc = vector_add(self.acc, evasion)
```
Choosing to uncomment this line instead of the previous two will lead to attacking behaviour.
```python
self.acc = vector_add(self.acc, attack)
```
