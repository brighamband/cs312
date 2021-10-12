#!/usr/bin/python3


from CS312Graph import *
import time


class Queue:
    queue = []

    def bubble_up():
        pass

    def sift_down():
        pass

    def min_child():
        pass

    # UPDATE

    def delete_min():
        pass

    def decrease_key():
        pass

    def insert():
        pass


class ArrayQueue(Queue):

    def delete_min():
        pass

    def decrease_key():
        pass    # Don't have to do anything here for array implementation

    def insert():
        pass

class HeapQueue(Queue):
    pass


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        t2 = time.time()
        return (t2-t1)