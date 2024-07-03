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

    def fillAvvistamenti(self, e):
        year = self._view.ddyear.value
        num_avv = self._model.getNumAvvistamenti(year)
        self._view.txt_name.value = num_avv
        self._view.update_page()

    def handle_graph(self, e):
        year = int(self._view.ddyear.value)
        self.graph = self._model.createGraph(year)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self.graph.number_of_nodes()}, Numero di archi: {self.graph.number_of_edges()}"))
        self._view.update_page()


    def handle_path(self, e):
        pass





