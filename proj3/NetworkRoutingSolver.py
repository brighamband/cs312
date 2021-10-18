#!/usr/bin/python3


from CS312Graph import *
import time
import math


class ArrayQueue():
    def __init__(self):
        self.queue = []

    def deleteMin(self, dist):
        min_dist_idx = 0
        for i in self.queue:
            if dist[i] < dist[min_dist_idx]:
                min_dist_idx = i
        del self.queue[min_dist_idx]
        return min_dist_idx

    def decreaseKey(self, idx, dist):
        pass    # Don't have to do anything here for array implementation

    def insert(self, dist_arr_idx):
        self.queue.append(dist_arr_idx)

    def makeQueue(self, num_dist_arr_indices):
        for i in range(num_dist_arr_indices):
            self.insert(i)
    
    def __len__(self):
        return len(self.queue)


class HeapQueue():
    def __init__(self):
        self.queue = []

    def __bubble_up(self):
        pass

    def __sift_down(self):
        pass

    def __min_child(self):
        pass

    def deleteMin(self):
        pass

    def decreaseKey(self, idx, dist):
        self.__bubble_up(idx)

    def insert(self, item):
        pass

    def makeQueue(self, items):
        pass


class NetworkRoutingSolver:
    def __init__(self):
        self.dist = []
        self.prev = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        
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

        # Clear arrays each time you start over
        self.dist.clear()
        self.prev.clear()

        queue = ArrayQueue()
        # queue = HeapQueue() if use_heap else ArrayQueue()   # Sets the right queue implementation based on settings

        self.dist = [math.inf] * len(self.network.nodes)
        self.prev = [None] * len(self.network.nodes)
        self.dist[srcIndex] = 0

        queue.makeQueue(len(self.network.nodes))
        while len(queue) > 0:
            cur_node_idx = queue.deleteMin(self.dist)

            cur_edges = self.network.nodes[cur_node_idx].neighbors

            for i in range(len(cur_edges)):
                dest_node_idx = cur_edges[i].dest.node_id

                if self.dist[dest_node_idx] > self.dist[cur_node_idx] + cur_edges[i].length:
                    self.dist[dest_node_idx] = self.dist[cur_node_idx] + cur_edges[i].length
                    self.prev[dest_node_idx] = cur_node_idx
                    queue.decreaseKey(dest_node_idx, self.dist)

        t2 = time.time()
        return (t2-t1)