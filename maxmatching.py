import sys
import copy
from dijkstra import *

class MaxMatching(object):
    """
    Finds a maximum matching in a bipartite graph.
    
    Constructed from a data file representing a bipartite graph with vertex
    classes A, B.  Data file assumed to be in the following form:
    [line 1] vertices in A, labelled as integers, separated by space
    [line 2] vertices in B, labelled as integers (distinct from those in A)
    [lines 3-END] i j, where i j is an edge, with i in A, j in B
    
    Example data file:
    1 2 3
    4 5 6
    1 5
    2 4
    3 6
    3 5
    
    Usage: 
    >>> mm = MaxMatching("yourgraph.in")
    >>> print mm.findMaxMatching()
    """
    def __init__(self, filename):
        self.A = []
        self.B = []
        self.g = dict() # underlying bipartite graph with vertex classes A, B
        with open(filename, 'r') as f:
            self.A = map(int, f.readline().strip().split())
            self.B = map(int, f.readline().strip().split())
            for u in self.A:
                self.g[u] = dict()
            for v in self.B:
                self.g[v] = dict()
            for line in f:
                u, v = map(int, line.strip().split()) # u in A, v in B
                # only add directed edge u -> v
                # this is needed for directGraphForMatching to work properly
                self.g[u][v] = 1

    def _directGraphForMatching(self, M):
        """
        Directs underlying bipartite graph with respect to the matching M, as 
        in the algorithm for producing a maximum matching.
        
        M assumed to be a list of ordered tuples (a,b) with a in A, b in B
        """
        dg = copy.deepcopy(self.g)
        for v in self.B:
            dg[v] = dict()
        for u, v in M:
            del dg[u][v]
            dg[v][u] = 1
        return dg 

    def _findAlternatingPath(self, X, Y, M):
        """
        Finds a path from a subset X of A to a subset Y of B,
        whose edges alternate being in/not in the collection M of edges.
        Returns ordered tuple of edges along a shortest path.
        """
        dg = self._directGraphForMatching(M)

        for x in X:
            reachable, P = Dijkstra(dg, x)
            for y in Y:
                if y in reachable:
                    return shortestPath(dg, x, y) # doubling work, but oh well
        return None
    
    def _APrimeBPrime(self, M):  
        """
        Given a matching of the graph, outputs the subsets A', B' of vertices 
        of A, B, resp., so that A' and B' are precisely the unmatched
        vertices.
        """
        dg = self._directGraphForMatching(M)
        
        APrime = set(self.A)
        BPrime = set(self.B)
        AToDelete = set()
        BToDelete = set()
        for e in M:
            AToDelete.add(e[0])
            BToDelete.add(e[1])
        APrime = APrime.difference(AToDelete)
        BPrime = BPrime.difference(BToDelete) 
        return (APrime, BPrime)            

    def _augmentMatching(self, M):
        """
        If possible, augments the matching M in G.
        M is a list of edges (ordered pairs) with first vertex in A, second in B.
        Returns larger matching, if one exists. Otherwise, returns None.
        """
        dg = self._directGraphForMatching(M)
        # X = set(self.A)
        # Y = set(self.B)
        # xToDelete = set()
        # yToDelete = set()
        # for e in M:
        #     xToDelete.add(e[0])
        #     yToDelete.add(e[1])
        # X = X.difference(xToDelete)
        # Y = Y.difference(yToDelete)
        X, Y = self._APrimeBPrime(M)
        path = self._findAlternatingPath(X, Y, M)
        if path is None:
            return M
        edgesOfPath = set([(path[i], path[i+1]) for i in range(len(path)-1) if i % 2 == 0])    
        edgesOfPath = edgesOfPath.union(set([(path[i+1], path[i]) for i in range(len(path)-1) if i % 2 == 1]))
        
        return M.symmetric_difference(edgesOfPath)
    
    def findMaxMatching(self):
        match = set()
        while True:
            newMatch = self._augmentMatching(match)
            if newMatch == match:
                break
            else:
                match = newMatch
        return match
    
    def minCoverFromMaxMatching(self, maxM):
        """
        Given a maximum matching of the bipartite graph G, 
        outputs a minimum vertex cover.  The correctness of this algorithm
        is a consequence of one of the proofs of Konig's Theorem.
        """
        mincover = set()
        dg = self._directGraphForMatching(maxM)
        X, Y = self._APrimeBPrime(maxM)
        for a, b in maxM:
            pathEndingInb = False
            for x in X:
                D, P = Dijkstra(dg, x)
                if b in D:
                    pathEndingInb = True
                    break
            if pathEndingInb:
                mincover.add(b)
            else:
                mincover.add(a)
        return mincover
             
if __name__ == "__main__":
    mm = MaxMatching("graph.in")
    print "The edges in a maximum matching of the input graph are:"
    matching = mm.findMaxMatching()
    for e in matching:
        print e
    print "The vertices in a minimum vertex cover are:"
    for v in mm.minCoverFromMaxMatching(matching):
        print v
    