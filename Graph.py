from dataclasses import dataclass, field
import numpy as np

# Representation of a node in the Graph.
@dataclass
class Node:
    label: str
    position: np.array
    id: int = -1

# Implementation for a unweighted, undirected graph. Implemented with an
# adjacency matrix.
class Graph:
    # Constructor. Takes in the maximum number of nodes to support.
    def __init__(self, MAX_NODES):
        # Store the maximum number of nodes.
        self.MAX_NODES = MAX_NODES
        self.numNodes = 0

        # Set up our internal data structures.
        self.adjMatrix = np.zeros((MAX_NODES, MAX_NODES), dtype=np.int)
        # Set the diagnoal of the matrix to -1. No cycles in this graph.
        np.fill_diagonal(self.adjMatrix, -1)
        self.nodes = []

    # Adds the given node to the graph.
    def addNode(self, newNode):
        success = False

        # Check the graph isn't full, and this node doesn't already exist in
        # the graph.
        if ((self.numNodes != self.MAX_NODES) and (newNode not in self.nodes)):
            # Assign the node its ID.
            newNode.id = self.numNodes
            self.numNodes = self.numNodes + 1

            # Add the node.
            self.nodes.append(newNode)

            # Mark the operation as successful.
            success = True
        
        # Return a boolean indicating the success of the operation.
        return success
    
    # Adds an edge betwen the node with the specified start ID and the node
    # with the specified end ID.
    def addEdge(self, startID, endID):
        success = False

        # First, make sure both nodes exist.
        startIDValid = (startID > -1) and (startID < self.numNodes)
        endIDValid = (endID > -1) and (endID < self.numNodes)
        if (startIDValid and endIDValid):
            # First, create the edge from startID to endID.
            self.adjMatrix[startID][endID] = 1

            # Then, create the edge from startID to endID.
            self.adjMatrix[endID][startID] = 1

            # Mark the operation as successful.
            success = True

        # Return a boolean indicating the success of the operation.
        return success

    # Returns a node given its ID.
    def getNode(self, id):
        node = None

        # Make sure the ID is valid.
        idValid = (id > -1) and (id < self.numNodes)
        if (idValid):
            node = self.nodes[id]

        # Return the node.
        return node

    # Checks for an edge betwen the node with the specified start ID and the
    # node with the specified end ID.
    def doesEdgeExist(self, startID, endID):
        edgeExists = False

        # First, make sure both nodes exist.
        startIDValid = (startID > -1) and (startID < self.numNodes)
        endIDValid = (endID > -1) and (endID < self.numNodes)
        if (startIDValid and endIDValid):
            # Check if the edge from startID to endID exists.
            startToEnd = self.adjMatrix[startID][endID] == 1
            endToStart = self.adjMatrix[endID][startID] == 1
            edgeExists = startToEnd and endToStart
        
        # Return a boolean indicating whether the node exists.
        return edgeExists
    
    # Print each node in the graph and its neighbors.
    def print(self):
        for i in range(self.numNodes):
            # Print the label of the node.
            print(self.nodes[i].id, end = '')

            # Print all its neighbors.
            for j in range(self.numNodes):
                if (self.adjMatrix[i][j] == 1):
                    print(' ' + str(self.nodes[i].id), end = '')
            
            # Print a newline.
            print('')