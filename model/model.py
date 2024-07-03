import copy
import itertools
from database import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.idMap = {}

    def createGraph(self, year, days):

        nodi = DAO.DAO.getStates()
        self.graph.add_nodes_from(nodi)

        for nodo in nodi:
            self.idMap[nodo.id] = nodo
        print(self.idMap)

        edges = DAO.DAO.getEdges(year, days, self.idMap)
        self.graph.add_weighted_edges_from(edges)

        return self.graph

    def ad_tostr(self):
        output = []
        nodi = self.graph.nodes
        for nodo in nodi:
            peso = 0
            adiac = self.graph.neighbors(nodo)
            for a in adiac:
                peso += self.graph[nodo][a]["weight"]
            output.append(f"{nodo.id}: peso archi adiacenti: {peso}")
        return output








