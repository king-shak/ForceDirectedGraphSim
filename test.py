from Graph import Graph, Node
import random
import numpy as np

NUM_NODES = 15
NODES_PER_GROUP = 5

graph = Graph()

nodes = []
random.seed(a = 10)
for i in range(NUM_NODES):
    x = random.randrange(320, 340, 1)
    y = random.randrange(240, 260, 1)
    node = Node(str(i + 1), np.array([x, y], dtype=np.double))
    nodes.append(node)
    graph.addNode(node)

for i in range(0, NUM_NODES, NODES_PER_GROUP):
    if (i != 0 and i != NUM_NODES):
        graph.addEdge(nodes[i].id, nodes[j].id)
        print('***(' + str(i - NODES_PER_GROUP) + ', ' + str(i) + ')')
    stop = i + NODES_PER_GROUP
    if (stop > NUM_NODES):
        stop = NUM_NODES - i
    for j in range (i + 1, stop):
        graph.addEdge(nodes[i].id, nodes[j].id)
        print('(' + str(i) + ', ' + str(j) + ')')