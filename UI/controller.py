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



    def handle_graph(self, e):
        year = int(self._view.txt_year.value)
        days = int(self._view.txt_name.value)
        if year >= 1906 and year <= 2014 and days >= 1 and days <= 180:
            self._view.txt_result.controls.clear()
            self.graph = self._model.createGraph(year, days)
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Numero di nodi: {self.graph.number_of_nodes()}, Numero di archi: {self.graph.number_of_edges()}"))
            self._view.update_page()

            output_ad = self._model.ad_tostr()
            for o in output_ad:
                self._view.txt_result.controls.append(ft.Text(o))
            self._view.update_page()

        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un anno compreso tra 1906 e 2014 e una quantità di giorni tra 1 e 180"))
            self._view.update_page()



    def handle_path(self, e):
        pass





