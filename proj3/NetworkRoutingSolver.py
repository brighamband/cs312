#!/usr/bin/python3


from CS312Graph import *
import time
import math


class ArrayQueue():
    def delete_min(self):
        highest_priority_item = min(self.queue)
        self.queue.remove(highest_priority_item)
        return highest_priority_item

    def decrease_key(self):
        pass    # Don't have to do anything here for array implementation

    def insert(self, item):
        self.queue.append(item)

    def make_queue(self, items):
        for item in items:
            self.insert(item)


class HeapQueue():
    def __bubble_up(self):
        pass

    def __sift_down(self):
        pass

    def __min_child(self):
        pass

    def delete_min(self):
        pass

    def decrease_key(self):
        pass

    def insert(self, item):
        pass

    def make_queue(self, items):
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
        # print('srcI', srcIndex)
        print('network', self.network)
        print('nodes', self.network.nodes)

        queue = HeapQueue() if use_heap else ArrayQueue()   # Sets the right queue implementation based on settings

        dist = [math.inf] * len(self.network.nodes)
        prev = [None] * len(self.network.nodes)
        dist[srcIndex] = 0

        Queue.make_queue(V distances as keys)
        while len()



        t2 = time.time()
        return (t2-t1)