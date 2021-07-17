from dataclasses import dataclass, field
import numpy as np

# Representation of a node in the Graph.
@dataclass
class Node:
    id: str
    position: np.array
    adjList: set = field(default_factory = set)

# Implementation for a undirected graph.
class Graph:
    def __init__(self):
        self.adjList = []
        self.labels = []
    
    def addNode(self, newNode):
        success = False

        # If the node doesn't already exist, add it.
        if (newNode.id not in self.labels):
            self.labels.append(newNode.id)
            self.adjList.append(newNode)
            success = True
        
        return success
    
    def addEdge(self, startID, endID):
        success = False

        # Grab both nodes.
        startNode = self.getNode(startID)
        endNode = self.getNode(endID)

        # Create the edge if both nodes exist.
        if ((startNode is not None) and (endNode is not None)):
            startNode.adjList.add(endID)
            endNode.adjList.add(startID)
            success = True

        return success

    def doesEdgeExist(self, startID, endID):
        # Grab both nodes.
        startNode = self.getNode(startID)
        endNode = self.getNode(endID)

        # Check if the nodes themselves exist.
        nodesExist = (startNode is not None) and (endNode is not None)
        
        # Check if the edge exists.
        edgeExists = False
        if (nodesExist):
            edgeExists = (endID in startNode.adjList) and (startID in endNode.adjList)
        
        return nodesExist and edgeExists
    
    def getNode(self, id):
        try:
            idx = self.labels.index(id)
            return self.adjList[idx]
        except:
            return None
        
    def print(self):
        for node in self.adjList:
            print(node.id + ':')
            for foo in node.adjList:
                print(foo)
                print(self.doesEdgeExist(node.id, foo))
            print('\n')