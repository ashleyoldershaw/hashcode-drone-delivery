# Drone delivery

This is from a Google HashCode competition.

We have to get drones to deliver orders in a grid.

## Current status

We use the naïve implementation which actually delivers all packages on time (but gives us a score of 0).

The aim of this for me is not necessarily to make amazingly smart drones, but use the data generated to work out what
behaviours could make the system better.

## Running instructions

Using Python 3.7:

To run the simulation
```bash
python simulate.py
```
To analyse the output and generate a list of instructions for the competition
```bash
python analyse_results.py
```

You may need to `pip install` some packages if they come up, but I'm not using anything crazy.
## Visualisation

We can visualise the grid with a set of characters representing the map, W is a warehouse, O is an order, we can show all
the orders and warehouse locations in the simulation at any given time. This was done early on and isn't triggered right now.

## Representation of time

The simulation is done in turns, where each turn the robot can move one tile or pick up/drop off items

The way we can indicate progress is that as soon as the robot is on the way to deliver an item we cross it off the list of that order.

So that we don't give tasks to busy robots we can see which robots are available. When a robot has a task it is then 'busy' and then reappears on the list once it is done.

## Calculating the actions

The search space is way to big to go doe a breadth first search or anything like that. We need to find a smarter way (nice)

### Options:

- Naïve implementation
    - Just cycle through the orders, initial implementation does this and ends up on time on test scenario
- Best first search (such as A*)
  - Need an heuristic function that does not overestimate
  - Perform actions that will decrease the "distance" to completion - could naively use the number of items to deliver - will be useful in a general case
  - Come up with weightings w for parameters x such that estimation of completion = sum(x[i]w[i])
  - Could train a model to know how much weighting to give each parameter
  
- Reinforcement learning
  
#### Heuristic estimation

There are several ways we can calculate the heuristic function, using a combination of the below:

- The number of orders left to deliver (minus the ones on their way)
- A measure of the distance of every product to its destination (could use the "average" square for location of products relative to the location of the orders)
- Could use reinforcement learning to adjust the weights of these parameters!