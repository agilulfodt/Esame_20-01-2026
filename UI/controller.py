import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert('inserire un valore numerico valido')
            return
        if n_alb <= 0:
            self._view.show_alert('inserire un valore numerico maggiore di 0')
            return

        self._model.load_artists_with_min_albums(n_alb)
        self._model.build_graph()

        self._view.txt_result.controls.clear()
        txt = f'grafo creato: {self._model.num_nodes()} nodi (artisti), {self._model.num_edges()} archi'
        self._view.txt_result.controls.append(ft.Text(txt))

        #popola dd
        self._view.ddArtist.disabled = False
        self._view.ddArtist.options.clear()
        for artist in self._model.nodes.values():
            option = ft.dropdown.Option(key=artist.id, text=artist.name)
            self._view.ddArtist.options.append(option)

        self._view.btnArtistsConnected.disabled = False

        self._view.update_page()

    def handle_connected_artists(self, e):
        ar_id = int(self._view.ddArtist.value)
        try:
            conn_art = self._model.connected_artists(ar_id)
        except KeyError:
            self._view.show_alert('artista non presente nel grafo, provare a ricaricare il grafo')
            return

        ar = conn_art[0][0]
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"artisti direttamente collegati all'artista {ar}"))
        for a in conn_art:
            txt = f'{a[1]} - numero di generi in comune: {a[2]}'
            self._view.txt_result.controls.append(ft.Text(txt))

        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False
        self._view.update_page()

    def handle_search_artists(self, e):
        try:
            d_min = float(self._view.txtMinDuration.value)
            a_max = int(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.show_alert('inserire valori numerici validi')
            return
        if d_min <= 0:
            self._view.show_alert('inserire un valore numerico maggiore di 0')
            return
        if a_max not in range(1, self._model.num_nodes() + 1):
            self._view.show_alert('inserire un valore numerico tra 1 e il numero di nodi massimo')
            return

        ar_id = int(self._view.ddArtist.value)
        start, percorso, peso = self._model.calcola_percorso(ar_id, d_min, a_max)

        self._view.txt_result.controls.clear()
        txt = f"cammino di peso massimo dall'artista {start}"
        self._view.txt_result.controls.append(ft.Text(txt))
        self._view.txt_result.controls.append(ft.Text(f'lunghezza: {len(percorso)}'))
        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.txt_result.controls.append(ft.Text(f'peso massimo: {peso}'))

        self._view.update_page()