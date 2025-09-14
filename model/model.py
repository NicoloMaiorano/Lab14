import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self._idMap = {}

    def creaGrafo(self, store, k):
        self.ordini = DAO.getOrdiniStore(store.store_id)
        for o in self.ordini:
            self._idMap[o.order_id] = o

        self.grafo.add_nodes_from(self.ordini)

        for o in self.ordini:
            for o2 in self.ordini:
                if o == o2:
                    pass
                else:
                    if o.order_date > o2.order_date:
                        diffdate = (o.order_date - o2.order_date).days
                        if diffdate < int(k):
                            print(f"differenza date: {diffdate}")
                            somma = DAO.getOggettiOrdine(o.order_id)
                            somma = somma + DAO.getOggettiOrdine(o2.order_id)
                            if not self.grafo.has_edge(o, o2):
                                self.grafo.add_edge(o, o2, weight=somma)

        print("Grafo creato")
        print(f"Numero di nodi: {self.grafo.number_of_nodes()}")
        print(f"Numero di archi: {self.grafo.number_of_edges()}")

    def getNodi(self):
        return self.ordini

    def getCammino(self, source):
        lp = []

        tree = nx.dfs_tree(self.grafo, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp

    def _ricorsione(self, parziale):
        if self.getScore(parziale) > self._bestScore:
            self._bestScore = self.getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for v in self.grafo.neighbors(parziale[-1]):
            if (v not in parziale and  # check if not in parziale
                    self.grafo[parziale[-2]][parziale[-1]]["weight"] >
                    self.grafo[parziale[-1]][v]["weight"]):  # check if peso nuovo arco è minore del precedente
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def getScore(self, listOfNodes):
        tot = 0
        for i in range(len(listOfNodes) - 1):
            tot += self.grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return tot

    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]

        vicini = self.grafo.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore
