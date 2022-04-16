from typing import List
import spotify
import psycopg2
import json
import sql_requests
import sql_requests_2


def create_json(data: list, file_name: str):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_playlists(playlist_ids: list, limit: int, client_id, client_secret, file_name: str):
    sp = spotify.Spotify(client_id, client_secret)
    db_playlists = sp.get_playlists(playlist_ids, limit)
    create_json(db_playlists, file_name)


def get_albums(album_ids: list, limit: int, client_id, client_secret, file_name: str):
    sp = spotify.Spotify(client_id, client_secret)
    db_albums = sp.get_albums(album_ids, limit)
    create_json(db_albums, file_name)


def fill_playlists(dbname, user, password, host, file_name: str):
    db_data = load_json(file_name)

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    for item in db_data:

        cursor.execute(sql_requests.insert_albums, [item['album'], item['album_release'][0:4]])
        cursor.execute(sql_requests.insert_collections, [item['playlist'], item['playlist_release']])

        for artist in item['artists']:
            cursor.execute(sql_requests.insert_artists, [artist])
            cursor.execute(sql_requests.insert_albums_artists, [item['album'], artist])
            for genre in item['artists'][artist]:
                cursor.execute(sql_requests.insert_genres, [genre])

        cursor.execute(sql_requests.insert_tracks, [item['track'], item['duration'] / 1000, item['album']])
        cursor.execute(sql_requests.insert_collections_tracks, [item['playlist'], item['track']])

        for artist in item['artists']:
            for genre in item['artists'][artist]:
                cursor.execute(sql_requests.insert_genres_artists, [genre, artist])

    conn.commit()
    cursor.close()
    conn.close()

def fill_albums(dbname, user, password, host, file_name: str):
    db_data = load_json(file_name)

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    for item in db_data:
        cursor.execute(sql_requests.insert_albums, [item['album'], item['album_release'][0:4]])

        for artist in item['artists']:
            cursor.execute(sql_requests.insert_artists, [artist])
            cursor.execute(sql_requests.insert_albums_artists, [item['album'], artist])
            for genre in item['artists'][artist]:
                cursor.execute(sql_requests.insert_genres, [genre])

        cursor.execute(sql_requests.insert_tracks, [item['track'], item['duration'] / 1000, item['album']])

        for artist in item['artists']:
            for genre in item['artists'][artist]:
                cursor.execute(sql_requests.insert_genres_artists, [genre, artist])

    conn.commit()
    cursor.close()
    conn.close()



def save_results(dbname: str, user: str, password: str, host: str):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    cursor = conn.cursor()

    cursor.execute(sql_requests.sel_albums)
    records = cursor.fetchall()
    write_result(records, 'albums_2018.txt')

    cursor.execute(sql_requests.sel_max_duration_track)
    records = cursor.fetchall()
    write_result(records, 'max_duration_track.txt')

    cursor.execute(sql_requests.sel_3_5_min_track)
    records = cursor.fetchall()
    write_result(records, 'sel_3_5_min_track.txt')

    cursor.execute(sql_requests.sel_2018_2020_collections)
    records = cursor.fetchall()
    write_result(records, 'sel_2018_2020_collections.txt')

    cursor.execute(sql_requests.sel_artist_name_one_word)
    records = cursor.fetchall()
    write_result(records, 'sel_artist_name_one_word.txt')

    cursor.execute(sql_requests.sel_track_with_word_my)
    records = cursor.fetchall()
    write_result(records, 'sel_track_with_word_my.txt')

    cursor.execute(sql_requests_2.count_artists_in_genres)
    records = cursor.fetchall()
    write_result(records, 'count_artists_in_genres.txt')

    cursor.execute(sql_requests_2.count_tracks_in_19_20)
    records = cursor.fetchall()
    write_result(records, 'count_tracks_in_19_20.txt')

    cursor.execute(sql_requests_2.avr_dur_tracks_by_albums)
    records = cursor.fetchall()
    write_result(records, 'avr_dur_tracks_by_albums.txt')

    cursor.execute(sql_requests_2.artist_not_20)
    records = cursor.fetchall()
    write_result(records, 'artist_not_20.txt')

    cursor.execute(sql_requests_2.specific_artist)
    records = cursor.fetchall()
    write_result(records, 'specific_artist.txt')

    cursor.execute(sql_requests_2.plst_with_artist_more_1_genre)
    records = cursor.fetchall()
    write_result(records, 'plst_with_artist_more_1_genre.txt')

    cursor.execute(sql_requests_2.tracks_not_in_playlists)
    records = cursor.fetchall()
    write_result(records, 'tracks_not_in_playlists.txt')

    cursor.execute(sql_requests_2.artist_min_track)
    records = cursor.fetchall()
    write_result(records, 'artist_min_track.txt')

    cursor.execute(sql_requests_2.albums_min_tracks)
    records = cursor.fetchall()
    write_result(records, 'albums_min_tracks.txt')

    cursor.close()
    conn.close()


def write_result(records: list, file_name: str):
    with open(file_name, mode='w', encoding='utf-8') as f:
        for record in records:
            for item in record:
                f.write(str(item) + '   ')
            f.write('\n')


if __name__ == '__main__':
    client_id = 'd018c4cbd53c4ba8b1568ecae7e7f976'
    client_secret = '51a75365a27f45bc8a00af6efbd0b4f7'
    db_pass = '@Kab189100!'

    playlists_ids = ['06iN03o811VWPvLwayMETN', '1iqt8e4JKpN3YxIxy86djO', '4ZiYJzYXl6clxsL0er7fdu',
                     '37i9dQZEVXbNG2KDcFcKOF', '37i9dQZEVXbLiRSasKsNU9', '37i9dQZEVXbNv6cjoMVCyg',
                     '37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DWVciwe52Zt0R']

    album_ids = ['4u5Ik7NMYl3EITJngbMS4V', '1YuRC8Fj5XdgpuoA7yBDnr', '5htuLCzUNQ5BRlngbw20Mu', '6SbrIpVsaJ5wgCQtMMwVR2',
                 '16iIPsnAjGZea8TeOCzeN8']

    # get_playlists(playlists_ids, client_id=client_id, client_secret=client_secret, limit=20,
    #                 file_name = 'db_playlists.json')
    #
    # fill_playlists(dbname='music', user='postgres', password=db_pass, host='localhost',
    #                 file_name = 'db_playlists.json')

    # get_albums(album_ids=album_ids, limit=20, client_id=client_id, client_secret=client_secret,
    #           file_name='db_albums.json')
    #
    # fill_albums(dbname='music', user='postgres', password=db_pass, host='localhost', file_name = 'db_albums.json')

    save_results(dbname='music', user='postgres', password=db_pass, host='localhost')