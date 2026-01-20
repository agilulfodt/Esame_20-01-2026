from database.DB_connect import DBConnect
from model.artist import Artist
from collections import defaultdict

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_alb(min_album):
        """
        Funzione per estrarre i nodi del grafo dal database
        Estrae gli artisti che hanno un numero di album maggiore o uguale a min_album
        :return: dizionario[id_artista] = numero di album
        """
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id, COUNT(*) as count
                FROM artist ar, album al
                WHERE ar.id = al.artist_id
                GROUP BY ar.id
                """

        cursor.execute(query)
        for row in cursor:
            if row['count'] >= min_album:
                result[row['id']] = row['count']

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_genre_map():
        """
        per ogni artista ne estrae i generi delle sue canzoni
        :return: dizionario[id_artista] = set(id_genere,...)
        """
        conn = DBConnect.get_connection()
        result = defaultdict(set)
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id, tr.genre_id
                FROM artist ar, album al, track tr
                WHERE ar.id = al.artist_id AND al.id = tr.album_id
                GROUP by ar.id, tr.genre_id
                """

        cursor.execute(query)
        for row in cursor:
            result[row['id']].add(row['genre_id'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_max_track_map():
        """
        per ogni artista ne estrae la durata massima in minuti tra tutte le sue canzoni
        :return: dizionario[id_artista] = durata
        """
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id, MAX(tr.milliseconds)/60000 AS dmax
                FROM artist ar, album al, track tr
                WHERE ar.id = al.artist_id AND al.id = tr.album_id
                GROUP BY ar.id
                """

        cursor.execute(query)
        for row in cursor:
            result[row['id']] = row['dmax']

        cursor.close()
        conn.close()
        return result
