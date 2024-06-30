import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self.graph = nx.Graph()

    def fillDD(self):
        years = self._model.getYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))

    def fillDDShape(self, e):
        year = self._view.ddyear.value
        shapes = self._model.getShapes(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()


    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        self.graph = self._model.createGraph(shape, year)
        self._view.txt_result.controls.clear()
        numero_nodi = self.graph.number_of_nodes()
        numero_archi = self.graph.number_of_edges()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {numero_nodi}, Numero di archi: {numero_archi}"))
        for nodo in self.graph.nodes:
            output = self._model.stampaPesoNodiAd(nodo)
            self._view.txt_result.controls.append(ft.Text(f"Nodo: {output[0]}, Peso archi adiacenti: {output[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        result = self._model.handlepath()
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Cammino di peso massimo: {result[0]}"))
        for string in result[1]:
            self._view.txtOut2.controls.append(ft.Text(string))
        self._view.update_page()

