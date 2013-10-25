"""
A modified version of David Eppstein's implementation of
Dijkstra's algorithm.  See his implementation at
http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/.
"""
from heapq import *

def Dijkstra(G, start, end=None):
    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = [] # queue of vertices whose edges need to be explored
    finished = set() # vertices all of whose edges have been explored

    heappush(Q, (0, start))
    D[start] = 0

    while Q:
        d, v = heappop(Q)
        finished.add(v)
        for w in G[v]:
            if w not in finished:
                dvw = D[v] + G[v][w]
                if w not in D or dvw < D[w]:
                    D[w] = dvw
                    heappush(Q, (dvw, w))
                    P[w] = v

    return (D,P)

def shortestPath(G, start, end):
    D,P = Dijkstra(G, start, end)
    path = []
    while True:
        path.append(end)
        if end == start:
            break
        end = P[end]
    path.reverse()
    return path

if __name__ == "__main__":
    """
    A simple example.
    """
    G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}, 'a': {}}
    print shortestPath(G, 's', 'v')