
insert_genres = 'INSERT INTO genres(name) VALUES (%s) ON CONFLICT ON CONSTRAINT genre_unic DO NOTHING'

insert_artists = 'INSERT INTO artists(name) VALUES(%s) ON CONFLICT ON CONSTRAINT artist_unic DO NOTHING'

insert_albums = 'INSERT INTO albums(name, start_year) VALUES (%s, %s)' \
                    'ON CONFLICT ON CONSTRAINT album_unic DO NOTHING'

insert_collections = 'INSERT INTO collections(name, start_year) VALUES (%s, %s) ' \
                         'ON CONFLICT ON CONSTRAINT collection_unic DO NOTHING'

insert_tracks = 'INSERT INTO tracks(name, duration, album_id) ' \
                    'SELECT %s, %s, albums.id ' \
                    'FROM albums ' \
                    'WHERE albums.name = %s ' \
                    'ON CONFLICT ON CONSTRAINT track_unic DO NOTHING'

insert_albums_artists = 'INSERT INTO albums_artists(album_id, artist_id)' \
                            'VALUES (' \
                                '(SELECT albums.id FROM albums WHERE albums.name = %s),' \
                                '(SELECT artists.id FROM artists WHERE artists.name = %s)' \
                            ')' \
                            'ON CONFLICT ON CONSTRAINT pk_aa DO NOTHING'

insert_collections_tracks = 'INSERT INTO collections_tracks(collection_id, track_id)' \
                                'VALUES(' \
                                    '(SELECT collections.id FROM collections WHERE collections.name = %s),' \
                                    '(SELECT tracks.id FROM tracks WHERE tracks.name = %s)' \
                                ')'

insert_genres_artists = 'INSERT INTO genres_artists(genre_id, artist_id)' \
                            'VALUES (' \
                                '(SELECT genres.id FROM genres WHERE genres.name = %s),' \
                                '(SELECT artists.id FROM artists WHERE artists.name = %s)' \
                            ')' \
                            'ON CONFLICT ON CONSTRAINT pk_ga DO NOTHING'

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