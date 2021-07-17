from Graph import Graph, Node
from math import log, pow
import random
import numpy as np
import matplotlib.pyplot as plt

# Constant definitions.
NUM_STEPS = 250
NUM_NODES = 30        # Don't exceed 30.
NODES_PER_GROUP = 5

# These are the constants used in calculating the attractive and repelling forces.
c1 = 2.0    # This is the strength of the attractive force.
c2 = 10.0   # This is the distance desired between nodes
c3 = 5.0   # This is the strength of the repelling force.
c4 = 1.0    # THIS is the effective speed of the nodes.

# This is our graph.
graph = Graph()

# This contains all our nodes.
nodes = []

# Create our nodes.
def isUniquePos(pos):
    for node in nodes:
        if np.array_equal(pos, node.position):
            return False
    return True

random.seed(a = 10)
for i in range(NUM_NODES):
    x = random.randrange(320, 340, 1)
    y = random.randrange(240, 260, 1)

    pos = np.array([x, y], dtype=np.double)
    while (not isUniquePos(pos)):
        pos[0] = random.randrange(320, 340, 1)
        pos[1] = random.randrange(240, 260, 1)

    label = str(i)
    if (i % NODES_PER_GROUP == 0):
        label += '***'

    node = Node(label, pos)
    nodes.append(node)
    graph.addNode(node)

# Create the edges.
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

# graph.print()

def getXY():
    x = []
    y = []
    labels = []

    for node in nodes:
        x.append(node.position[0])
        y.append(node.position[1])
        labels.append(node.id)

    return x, y, labels

# Graph the initial positions of the nodes.
fig, ax = plt.subplots(figsize = (10, 10))

x, y, labels = getXY()

ax.scatter(x, y)

for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))

# plt.legend()
plt.savefig('before.png')
plt.show()

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
    force = c1 * log(distance / c2)
    
    vec[0] = vec[0] * force
    vec[1] = vec[1] * force
    
    return vec, force

def repellingForce(src, dest):
    # Calculate the distance and normalized vector of src and dest.
    distance = getDistance(src, dest)
    vec = normalizedVector(src, dest)
    
    # Calculate the repelling force and apply it.
    force = -c3 / pow(distance, 2)
    
    vec[0] = vec[0] * force
    vec[1] = vec[1] * force
    
    return vec, force

# Simulate the connected nodes.
x = range(NUM_STEPS)
attractiveForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
repellingForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
netForces = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
posX = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)
posY = np.zeros((len(nodes), NUM_STEPS), dtype = np.double)

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
        node1.position[0] = node1.position[0] + (c4 * netForce[0])
        node1.position[1] = node1.position[1] + (c4 * netForce[1])
        
        # Save our data.
        posX[i][step] = node1.position[0]
        posY[i][step] = node1.position[1]
        
        attractiveForces[i][step] = netAttractiveForce
        repellingForces[i][step] = netRepellingForce

fig, ax = plt.subplots(figsize = (10, 10))

# Graph the net forces of each node.
for i in range(NUM_NODES):
    label = "Node " + str(i) + " Net"
    ax.plot(x, netForces[i], label = label, marker = 'o')

# ax.plot(x, netForces[0], label = "Node A Net", marker = 'o')
# ax.plot(x, attractiveForces[0], label = "Node A Attractive")
# ax.plot(x, repellingForces[0], label = "Node A Repelling")

# ax.plot(x, netForces[1], label = "Node B Net", marker = 'o')
# ax.plot(x, attractiveForces[1], label = "Node B Attractive")
# ax.plot(x, repellingForces[1], label = "Node B Repelling")

plt.ylim([-10, 100])
# plt.xlim([0, 10])
plt.legend()
plt.show()

# Graph the final positions of the nodes.
fig, ax = plt.subplots(figsize = (10, 10))

x, y, labels = getXY()

ax.scatter(x, y)

for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))

# plt.legend()
plt.savefig('after.png')
plt.show()

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

print('Mean edge length: ' + str(meanEdgeLength))
print('Edge length STD: ' + str(edgeLengthStd))