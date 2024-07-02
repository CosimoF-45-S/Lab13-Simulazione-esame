import copy
import itertools
from geopy.distance import geodesic

from database import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def getYears(self):
        years = DAO.DAO.getYears()
        return years

    def getShapes(self, year):
        shapes = DAO.DAO.getShapes(year)
        return shapes

    def createGraph1(self, shape, year):

        nodes = DAO.DAO.getStates()
        self.graph.add_nodes_from(nodes)

        node_tuples = list(itertools.combinations(nodes, 2))
        for t in node_tuples:
            edgeWeight = DAO.DAO.getWeight(t[0].id, t[1].id, shape, year)
            if edgeWeight != -1:
                self.graph.add_edge(t[0], t[1], weight=edgeWeight)

        return self.graph

    def createGraph2(self, shape, year):
        nodes = DAO.DAO.getStates()
        for node in nodes:
            self.idMap[node.id] = node
        self.graph.add_nodes_from(nodes)

        edges = DAO.DAO.getEdges(shape, year, self.idMap)
        for edge in edges:
            self.graph.add_edge(edge[0], edge[1], weight=edge[2])

        return self.graph


    def stampaPesoNodiAd(self, nodo):
        tot_weight = 0
        for edge in self.graph.edges(nodo, data=True):
            tot_weight += edge[2]["weight"]
        return nodo.id, tot_weight

    def handlepath(self):
        self.maxdistance = 0
        self.bestpath = []

        for nodo in self.graph.nodes():
            last_node = nodo
            self.recursive(last_node, [], 0, [last_node])

        printable_path = self.printablepath(self.bestpath)

        return self.maxdistance, printable_path

    def recursive(self, last_node, partial, last_weight, visited):

        archiammissibili = self.getArchiAmmissibili(last_node, last_weight, visited)

        if not archiammissibili:
            distTot = self.calcolaDistTot(partial)
            if distTot > self.maxdistance:
                self.maxdistance = distTot
                self.bestpath = copy.deepcopy(partial)
        else:
            for edge in archiammissibili:
                partial.append(edge)
                visited.append(edge[1])
                self.recursive(edge[1], partial, edge[2]["weight"], visited)
                partial.pop()
                visited.pop()



    def getArchiAmmissibili(self, last_node, last_weight, visited):
        output = []
        archivicini = self.graph.edges(last_node, data=True)
        for edge in archivicini:
            if edge[2]["weight"] > last_weight and edge[1] not in visited:
                output.append(edge)
        return output

    def calcolaDistTot(self, partial):
        distTot = 0
        for edge in partial:
            dist = geodesic((edge[0].Lat, edge[0].Lng), (edge[1].Lat, edge[1].Lng)).kilometers
            distTot += dist
        return distTot

    def printablepath(self, path):
        result = []
        for edge in path:
            result.append(f"{edge[0].id}->{edge[1].id}, peso: {edge[2]['weight']}, distanza: {geodesic((edge[0].Lat, edge[0].Lng), (edge[1].Lat, edge[1].Lng)).kilometers}")
        return result





