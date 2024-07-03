import copy
import itertools
from database import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.idMap = {}

    def getYears(self):
        years = DAO.DAO.getYears()
        return years

    def getNumAvvistamenti(self, year):
        numAvvistamenti = DAO.DAO.getNumAvv(year)
        return numAvvistamenti

    def createGraph(self, year):

        nodi = DAO.DAO.getNodes(year)
        self.graph.add_nodes_from(nodi)

        for nodo in nodi:
            self.idMap[nodo.id] = nodo
        print(self.idMap)

        edges = DAO.DAO.getEdges(year, self.idMap)
        self.graph.add_edges_from(edges)

        return self.graph







