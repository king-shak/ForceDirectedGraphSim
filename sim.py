# TODO: Look into maybe making some sort of visualizer? If we have time, and
#       it doesn't take too much time. The goal would be to visualize it and
#       be able to change the constants, as well as the steps and the number
#       of steps to perform per second (should report if there are
#       performance issues).

from Graph import Graph, Node
from math import log, pow
import random
import numpy as np
import matplotlib.pyplot as plt
import time

# Constant definitions.
NUM_STEPS = 250
NUM_NODES = 20        # Don't exceed 30.
NODES_PER_GROUP = 5

C1 = 2.0    # This is the strength of the attractive force.
C2 = 10.0   # This is the distance desired between nodes
C3 = 5.0    # This is the strength of the repelling force.
C4 = 1.0    # This is the effective speed of the nodes.

# Now we define our graph.
graph = Graph(NUM_NODES)
nodes = []

# This is used to make sure the starting position of each node is unique.
def isUniquePos(pos):
    for node in nodes:
        if np.array_equal(pos, node.position):
            return False
    return True

# Create our nodes.
random.seed(a = 10)
for i in range(NUM_NODES):
    # Keep generating random positions till we get something unique.
    x = random.randrange(320, 340, 1)
    y = random.randrange(240, 260, 1)

    pos = np.array([x, y], dtype=np.double)
    while (not isUniquePos(pos)):
        pos[0] = random.randrange(320, 340, 1)
        pos[1] = random.randrange(240, 260, 1)

    # Create the label for the node.
    label = str(i)

    # If this is the 'leader' of a group (it's directly connected to all the
    # nodes in the group) add *** to the label to distinguish it from others.
    if (i % NODES_PER_GROUP == 0):
        label += '***'

    # Create the node, add it to our list and add it to the graph.
    # The ID will be assigned by the graph.
    node = Node(label = label, position = pos)
    nodes.append(node)
    graph.addNode(node)

# Create the edges.
# TODO: Clean this up to model groups which actually would appear in ProVis.
#       (Having one node sticking out from the "leader" of the group which
#        used to connect to the other groups).
# TODO: Try to add a way to add other disjoint groups.
for i in range(0, NUM_NODES, NODES_PER_GROUP):
    if (i != 0 and i != NUM_NODES):
        graph.addEdge(nodes[i - NODES_PER_GROUP].id, nodes[i].id)
        print('***(' + str(i - NODES_PER_GROUP) + ', ' + str(i) + ')')
    stop = i + NODES_PER_GROUP
    if (stop > NUM_NODES):
        stop = NUM_NODES - i
    for j in range (i + 1, stop):
        graph.addEdge(nodes[i].id, nodes[j].id)
        print('(' + str(i) + ', ' + str(j) + ')')

# Revised edge creation method which has the commit node, with the software agent node
# connected to that, and a activity node connected to that, which has 4 entity nodes
# connected to it.
# for i in range(0, NUM_NODES, NODES_PER_GROUP):
#     # Create the commit node.


#     # If this isn't the first one, (i.e., node ID 0) create an edge between this commit
#     # node and the previous one.

#     # Create the software agent node and an edge between it and the commit node.

#     # Create the activity node and an edge between it and the software agent node.

#     # Create the 4 entity nodes and created edges between them and the activity node.


# graph.print()

# This gets the X and Y values of the positions of all the nodes, as well as
# their labels, for when we want to plot their positions.
def getXY():
    x = []
    y = []
    labels = []

    for node in nodes:
        x.append(node.position[0])
        y.append(node.position[1])
        labels.append(node.label)

    return x, y, labels

# Graph the initial positions of the nodes.
fig, axes = plt.subplots(2, 2, figsize = (20, 20))

x, y, labels = getXY()
axes[0][0].scatter(x, y)

for i, txt in enumerate(labels):
    axes[0][0].annotate(txt, (x[i], y[i]))

axes[0][0].set_title('Initial Positions')
axes[0][0].set_xlabel('X')
axes[0][0].set_ylabel('Y')

# Helper methods for calculating forces between the nodes.
def getDistance(src, dest):
    return np.linalg.norm(src - dest)

def normalizedVector(src, dest):
    return (dest - src) / np.linalg.norm(src - dest)

# These calculate the forces bewteen the nodes.
def attractiveForce(src, dest):
    # Calculate the distance and normalized vector of src and dest.
    distance = getDistance(src, dest)
    vec = normalizedVector(src, dest)
    
    # Calculate the attractive force and apply it.
    force = C1 * log(distance / C2)
    
    vec[0] = vec[0] * force
    vec[1] = vec[1] * force
    
    return vec, force

def repellingForce(src, dest):
    # Calculate the distance and normalized vector of src and dest.
    distance = getDistance(src, dest)
    vec = normalizedVector(src, dest)
    
    # Calculate the repelling force and apply it.
    force = -C3 / pow(distance, 2)
    
    vec[0] = vec[0] * force
    vec[1] = vec[1] * force
    
    return vec, force

# Create the arrays to store our data in.
simX = np.array(range(NUM_STEPS), dtype = np.double)
attractiveForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
repellingForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
netForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
posX = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
posY = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)

# Run the simulation.
simStart = time.time()
for step in range(NUM_STEPS):
    for i, node1 in enumerate(nodes):
        netForce = np.array([0.0, 0.0], dtype = np.double)
        netAttractiveForce = 0.0
        netRepellingForce = 0.0
        for j, node2 in enumerate(nodes):
            if (node1 is not node2):
                if (graph.doesEdgeExist(node1.id, node2.id)):
                    # Compute the attractive and repelling forces.
                    pull, f_pull = attractiveForce(node1.position, node2.position)
                    push, f_push = repellingForce(node1.position, node2.position)

                    # Compute the net force on the node.
                    netForce[0] = netForce[0] + (pull[0] + push[0])
                    netForce[1] = netForce[1] + (pull[1] + push[1])
                    
                    # Keep track of the net attractive and repelling forces (for analysis).
                    netAttractiveForce = netAttractiveForce + f_pull
                    netRepellingForce = netRepellingForce + f_push
                else:
                    # Compute the repelling forces.
                    push, f_push = repellingForce(node1.position, node2.position)

                    # Compute the net force on the node.
                    netForce[0] = netForce[0] + push[0]
                    netForce[1] = netForce[1] + push[1]
                    
                    # Keep track of the net repelling force (for analysis).
                    netRepellingForce = netRepellingForce + f_push

        # Finally, we apply the force on the node by updating its position.
        netForces[i][step] = np.linalg.norm(netForce)
        node1.position[0] = node1.position[0] + (C4 * netForce[0])
        node1.position[1] = node1.position[1] + (C4 * netForce[1])
        
        # Save our data.
        posX[i][step] = node1.position[0]
        posY[i][step] = node1.position[1]
        
        attractiveForces[i][step] = netAttractiveForce
        repellingForces[i][step] = netRepellingForce
simEnd = time.time()
print(simEnd - simStart)

# Graph the final positions of the nodes.
x, y, labels = getXY()
axes[0][1].scatter(x, y)

for i, txt in enumerate(labels):
    axes[0][1].annotate(txt, (x[i], y[i]))

axes[0][1].set_title('Final Positions')
axes[0][1].set_xlabel('X')
axes[0][1].set_ylabel('Y')

# Post analysis of node positions.
edgeLengths = []
for node1 in nodes:
    for node2 in nodes:
        if ((node1 is not node2) and graph.doesEdgeExist(node1.id, node2.id)):
            edgeLengths.append(getDistance(node1.position, node2.position))

data = np.array(edgeLengths, dtype=np.double)

# Calculate mean and standard deviation.
meanEdgeLength = np.mean(data)
edgeLengthStd = np.std(data)

results = f'Mean edge length: {round(meanEdgeLength, 2)}\nEdge length STD: {round(edgeLengthStd, 2)}'
axes[0][1].text(0.73, 0.02, results, size = 10, transform = axes[0][1].transAxes)

print('Mean edge length: ' + str(meanEdgeLength))
print('Edge length STD: ' + str(edgeLengthStd))

# TODO: Make a separate figure for drawing all the forces, do one per node
#       (showing attractive, repelling, and net forces).
# Graph the net forces of each node.
for i in range(NUM_NODES):
    label = "Node " + str(i) + " Net"
    axes[1][0].plot(simX, netForces[i], label = label, marker = 'o')

axes[1][0].axis(xmin = 0, xmax = 10)
axes[1][0].axis(ymin = -3, ymax = 15)
axes[1][0].set_xlabel('Sim Step')
axes[1][0].set_ylabel('Net Force')

# Graph the attractive and repelling forces of each node.
MARKERS = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for i in range(NUM_NODES):
    label = "Node " + str(i) + " Attractive"
    axes[1][1].plot(simX, attractiveForces[i], label = label, marker = MARKERS[i])

    label = "Node " + str(i) + " Repelling"
    axes[1][1].plot(simX, repellingForces[i], label = label, marker = MARKERS[i])

axes[1][1].axis(xmin = 0, xmax = 20)
axes[1][1].axis(ymin = -6, ymax = 5)
axes[1][1].set_xlabel('Sim Step')
axes[1][1].set_ylabel('Force')

plt.savefig('results.png', dpi = 300)