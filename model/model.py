import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self._artists_alb = {}
        self.nodes = {}
        self._artisti_track_max_map = {}
        self._best_path = []
        self._best_weight = 0

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self._artists_alb.clear()
        self._artists_alb = DAO.get_artists_alb(min_albums)


    def build_graph(self):
        self._graph.clear()
        self.nodes.clear()

        for artist in self._artists_list:
            if artist.id in self._artists_alb:
                self.nodes[artist.id] = artist

        self._graph.add_nodes_from(self.nodes.values())

        artist_genre_map = DAO.get_genre_map()

        nodes = list(self.nodes.values())
        for i, a1 in enumerate(nodes):
            for a2 in nodes[i+1:]:
                if artist_genre_map[a1.id].intersection(artist_genre_map[a2.id]):
                    weight = len(artist_genre_map[a1.id].intersection(artist_genre_map[a2.id]))
                    self._graph.add_edge(a1, a2, weight=weight)

    def num_nodes(self):
        return self._graph.number_of_nodes()
    def num_edges(self):
        return self._graph.number_of_edges()

    def connected_artists(self, ar_id):
        start = self.nodes[ar_id]
        result = []
        for neigh in self._graph.neighbors(start):
            weight = self._graph[start][neigh]['weight']
            result.append((start, neigh, weight))

        return result

    def calcola_percorso(self, ar_id, d_min, a_max):
        self._artisti_track_max_map.clear()
        self._best_path.clear()
        self._best_weight = 0

        start = self.nodes[ar_id]
        self._artisti_track_max_map = DAO.get_max_track_map()

        self._ricorsione(start, d_min, a_max, [start], 0)
        print(self._best_path)

        return start, self._best_path, self._best_weight

    def _ricorsione(self, start, d_min, a_max, partial_path, partial_weight):
        if len(partial_path) >= a_max+1:
            return

        if partial_weight > self._best_weight:
            self._best_weight = partial_weight
            self._best_path = partial_path.copy()


        admissable_neighbours = self._get_admissable_neighbours(start, d_min)
        for n in admissable_neighbours:
            if n in partial_path:
                continue

            w = self._graph[start][n]['weight']
            partial_path.append(n)
            self._ricorsione(n, d_min, a_max, partial_path, partial_weight + w)
            partial_path.pop()

    def _get_admissable_neighbours(self, start, d_min):
        admissable_neighbours = []
        for neigh in self._graph.neighbors(start):
            if float(self._artisti_track_max_map[neigh.id]) >= d_min:
                admissable_neighbours.append(neigh)

        return admissable_neighbours
