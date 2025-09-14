import flet as ft
from flet_core import Dropdown

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def caricaDDstore(self, dd : Dropdown):
        neg = DAO.getStores()
        for n in neg:
            dd.options.append(ft.dropdown.Option(text=n.store_id,
                                                    data=n,
                                                    on_click=self.read_DD_Store))

    def read_DD_Store(self, e):
        if e.control.data is None:
            self.store = None
        else:
            self.store = e.control.data


    def handleCreaGrafo(self, e):
        if self.store is None:
            pass
        else:
            k = self._view._txtIntK.value
            print(k)
            self._model.creaGrafo(self.store, k)
            self.caricaDDnodi()

    def handleCerca(self, e):
        nodes = self._model.getCammino(self.nodo)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self.nodo.store_id}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        bestpath, bestscore = self._model.getBestPath(self.nodo)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato un cammino che parte da {self.nodo} "
                    f"con somma dei pesi uguale a {bestscore}."))

        print(bestpath)
        for v in bestpath:
            self._view.txt_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()

    def caricaDDnodi(self):
        nodi = self._model.getNodi()
        for n in nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(text=n.order_id,
                                                                data=n,
                                                                on_click=self.read_DD_nodi))
        self._view.update_page()

    def read_DD_nodi(self, e):
        if e.control.data is None:
            self.nodo = None
        else:
            self.nodo = e.control.data