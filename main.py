from typing import List
import spotify
import psycopg2
import json
import pprint


def create_json(data: list):
    with open('db_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_data(playlist_ids: list, limit: int, client_id, client_secret):
    sp = spotify.Spotify(client_id, client_secret)
    db_data = sp.get_playlists(playlist_ids, limit)
    create_json(db_data)

def fill_db(dbname, user, password, host):
    db_data = load_json('db_data.json')

    insert_genres = 'INSERT INTO genres(name) VALUES (%s) ON CONFLICT ON CONSTRAINT genre_unic DO NOTHING'

    insert_artists = 'INSERT INTO artists(name) VALUES(%s) ON CONFLICT ON CONSTRAINT artist_unic DO NOTHING'

    insert_albums = 'INSERT INTO albums(name, start_year) VALUES (%s, %s)' \
                    'ON CONFLICT ON CONSTRAINT album_unic DO NOTHING'

    insert_collections = 'INSERT INTO collections(name, start_year) VALUES (%s, %s) ' \
                         'ON CONFLICT ON CONSTRAINT collection_unic DO NOTHING'

    insert_tracks = 'INSERT INTO tracks(name, duration, album_id) SELECT %s, %s, albums.id ' \
                    'FROM albums WHERE albums.name = %s ON CONFLICT ON CONSTRAINT track_unic DO NOTHING'

    insert_albums_artists = 'INSERT INTO albums_artists(album_id, artist_id)' \
                            'VALUES ((SELECT albums.id FROM albums WHERE albums.name = %s),' \
                            '(SELECT artists.id FROM artists WHERE artists.name = %s))' \
                            'ON CONFLICT ON CONSTRAINT pk_aa DO NOTHING'

    insert_collections_tracks = 'INSERT INTO collections_tracks(collection_id, track_id)' \
                                'VALUES((SELECT collections.id FROM collections WHERE collections.name = %s),' \
                                      '(SELECT tracks.id FROM tracks WHERE tracks.name = %s))'

    insert_genres_artists = 'INSERT INTO genres_artists(genre_id, artist_id)' \
                            'VALUES ((SELECT genres.id FROM genres WHERE genres.name = %s),' \
                                    '(SELECT artists.id FROM artists WHERE artists.name = %s))' \
                            'ON CONFLICT ON CONSTRAINT pk_ga DO NOTHING'

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    for item in db_data:

        cursor.execute(insert_albums, [item['album'], item['album_release'][0:4]])
        cursor.execute(insert_collections, [item['playlist'], item['playlist_release']])

        for artist in item['artists']:
            cursor.execute(insert_artists, [artist])
            cursor.execute(insert_albums_artists, [item['album'], artist])
            for genre in item['artists'][artist]:
                cursor.execute(insert_genres, [genre])

        cursor.execute(insert_tracks, [item['track'], item['duration'] / 1000, item['album']])
        cursor.execute(insert_collections_tracks, [item['playlist'], item['track']])

        for artist in item['artists']:
            for genre in item['artists'][artist]:
                cursor.execute(insert_genres_artists, [genre, artist])

    conn.commit()
    cursor.close()
    conn.close()

def save_results(dbname: str, user: str, password: str, host: str):

    sel_albums = 'SELECT name, start_year FROM albums WHERE albums.start_year = 2018 ORDER BY name'

    sel_max_duration_track = 'SELECT name, duration FROM tracks ORDER BY duration DESC LIMIT 1'

    sel_3_5_min_track = 'SELECT name from tracks WHERE duration >= 60*3.5 ORDER BY name'

    sel_2018_2020_collections = 'SELECT name FROM collections WHERE start_year >= 2018 ' \
                                'AND start_year <= 2020 ORDER BY start_year'

    sel_artist_name_one_word = "SELECT name FROM artists WHERE TRIM(name) NOT LIKE '% %' ORDER BY name"

    sel_track_with_word_my = "SELECT name FROM tracks WHERE LOWER(name) LIKE '% мой %'" \
                   "OR LOWER(name) LIKE 'мой %' " \
                   "OR LOWER(name) LIKE '% мой' " \
                   "OR LOWER(name) LIKE '% my %' " \
                   "OR LOWER(name) LIKE 'my %'	" \
                   "OR LOWER(name) LIKE '% my';"

    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    cursor = conn.cursor()

    cursor.execute(sel_albums)
    records = cursor.fetchall()
    write_result(records, 'albums_2018.txt')

    cursor.execute(sel_max_duration_track)
    records = cursor.fetchall()
    write_result(records, 'max_duration_track.txt')

    cursor.execute(sel_3_5_min_track)
    records = cursor.fetchall()
    write_result(records, 'sel_3_5_min_track.txt')

    cursor.execute(sel_2018_2020_collections)
    records = cursor.fetchall()
    write_result(records, 'sel_2018_2020_collections.txt')

    cursor.execute(sel_artist_name_one_word)
    records = cursor.fetchall()
    write_result(records, 'sel_artist_name_one_word.txt')

    cursor.execute(sel_track_with_word_my)
    records = cursor.fetchall()
    write_result(records, 'sel_track_with_word_my.txt')

    cursor.close()
    conn.close()

def write_result(records: list, file_name: str):
    with open(file_name, mode='w', encoding='utf-8') as f:
        for record in records:
            for item in record:
                f.write(str(item) + '   ')
            f.write('\n')


if __name__ == '__main__':

    playlists_ids = ['06iN03o811VWPvLwayMETN', '1iqt8e4JKpN3YxIxy86djO', '4ZiYJzYXl6clxsL0er7fdu',
                            '37i9dQZEVXbNG2KDcFcKOF', '37i9dQZEVXbLiRSasKsNU9', '37i9dQZEVXbNv6cjoMVCyg',
                            '37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DWVciwe52Zt0R']

    get_data(playlists_ids, client_id='dummy', client_secret='dummy', limit=20)

    fill_db(dbname='music', user='postgres', password='dummy', host='localhost')

    save_results(dbname='music', user='postgres', password='dummy', host='localhost')

