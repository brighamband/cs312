#!/usr/bin/python3


from CS312Graph import *
import time
import math


class ArrayQueue():
    queue = []

    def delete_min(self, dist):
        min_dist_idx = 0
        for i in self.queue:
            if dist[i] < dist[min_dist_idx]:
                min_dist_idx = i
        del self.queue[min_dist_idx]
        return min_dist_idx

    def decrease_key(self, idx, dist):
        pass    # Don't have to do anything here for array implementation

    def insert(self, distArrIdx):
        self.queue.append(distArrIdx)

    def make_queue(self, numDistArrIndices):
        for i in range(numDistArrIndices):
            self.insert(i)
    
    def __len__(self):
        return len(self.queue)


class HeapQueue():
    def __init__(self):
        queue = []

    def __bubble_up(self):
        pass

    def __sift_down(self):
        pass

    def __min_child(self):
        pass

    def delete_min(self):
        pass

    def decrease_key(self, idx, dist):
        self.__bubble_up(idx)

    def insert(self, item):
        pass

    def make_queue(self, items):
        pass


class NetworkRoutingSolver:
    def __init__(self):
        dist = []
        prev = []

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

        # print('network', self.network)
        # print('nodes', self.network.nodes)

        queue = ArrayQueue()
        # queue = HeapQueue() if use_heap else ArrayQueue()   # Sets the right queue implementation based on settings

        dist = [math.inf] * len(self.network.nodes)
        prev = [None] * len(self.network.nodes)
        dist[srcIndex] = 0

        queue.make_queue(len(self.network.nodes))
        while len(queue) > 0:
            curNodeIdx = queue.delete_min(dist)

            curKidEdges = self.network.nodes[curNodeIdx].neighbors

            for i in range(len(curKidEdges)):
                destNodeIdx = curKidEdges[i].dest.node_id

                if dist[destNodeIdx] > dist[curNodeIdx] + curKidEdges[i].length:
                    dist[destNodeIdx] = dist[curNodeIdx] + curKidEdges[i].length
                    prev[destNodeIdx] = curNodeIdx
                    queue.decrease_key(destNodeIdx, dist)

        t2 = time.time()
        return (t2-t1)