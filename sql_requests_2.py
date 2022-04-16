
count_artists_in_genres = 'SELECT genres.name, COUNT(genres_artists.artist_id) AS count FROM genres ' \
                                'LEFT JOIN genres_artists ON genres.id = genres_artists.genre_id GROUP BY genres.name'

count_tracks_in_19_20 = 'SELECT count(tracks.id) AS count FROM tracks ' \
                            'LEFT JOIN albums ON tracks.album_id = albums.id ' \
                            'WHERE albums.start_year BETWEEN 2019 AND 2020'

avr_dur_tracks_by_albums = 'SELECT albums.name, AVG(tracks.duration) FROM albums ' \
                                'LEFT JOIN tracks ON albums.id = tracks.album_id GROUP BY albums.name'

artist_not_20 ='SELECT name FROM artists ' \
                    'LEFT JOIN albums_artists ON artists.id = albums_artists.artist_id ' \
                    'WHERE albums_artists.album_id NOT IN ' \
                        '(SELECT id FROM albums WHERE albums.start_year = 2020)'

specific_artist = "SELECT collections.name FROM collections " \
                        "LEFT JOIN collections_tracks ON collections.id = collections_tracks.collection_id " \
                        "LEFT JOIN tracks ON tracks.id = collections_tracks.track_id " \
                        "LEFT JOIN albums ON albums.id = tracks.album_id " \
                        "LEFT JOIN albums_artists ON albums.id = albums_artists.album_id " \
                        "WHERE albums_artists.artist_id = " \
                            "(SELECT id FROM artists WHERE artists.name = 'Artik')"

plst_with_artist_more_1_genre = 'SELECT albums.name FROM albums ' \
                                    'LEFT JOIN albums_artists ON albums.id = albums_artists.album_id ' \
                                    'WHERE albums_artists.artist_id IN ' \
                                        '(SELECT artist_id FROM' \
                                            '(SELECT artist_id, COUNT(genre_id) AS genres_count	FROM genres_artists ' \
                                                'GROUP BY genres_artists.artist_id' \
                                            ') AS artists ' \
                                        'WHERE genres_count > 1) ' \
                                    'GROUP BY albums.name'

tracks_not_in_playlists = 'SELECT name  FROM tracks ' \
                                'LEFT JOIN collections_tracks ON tracks.id = collections_tracks.track_id ' \
                                'WHERE collections_tracks.track_id IS NULL ORDER BY name'

artist_min_track = 'SELECT artists.name FROM artists ' \
                        'LEFT JOIN albums_artists ON artists.id = albums_artists.artist_id ' \
                        'LEFT join ALBUMS ON albums.id = albums_artists.album_id ' \
                        'LEFT JOIN tracks ON tracks.album_id = albums.id ' \
                        'WHERE tracks.id IN ' \
                            '(SELECT id FROM tracks WHERE tracks.id IN ' \
                                '(SELECT id FROM tracks ORDER BY tracks.duration limit 1))'

albums_min_tracks = 'SELECT name FROM' \
                        '(SELECT albums.name, count(tracks.id) AS count FROM albums ' \
                            'LEFT JOIN tracks ON tracks.album_id = albums.id ' \
                            'GROUP BY albums.name' \
                        ') AS tbl ' \
                        'WHERE count IN ' \
                            '(SELECT COUNT(tracks.id) AS count FROM albums ' \
                                'LEFT JOIN tracks ON tracks.album_id = albums.id ' \
                                'GROUP BY albums.name ORDER BY count LIMIT 1' \
                        ');'