
#1
count_artists_in_genres = 'SELECT genres.name, COUNT(genres_artists.artist_id) AS count FROM genres ' \
                                'LEFT JOIN genres_artists ON genres.id = genres_artists.genre_id GROUP BY genres.name'

#2
count_tracks_in_19_20 = 'SELECT count(tracks.id) AS count FROM tracks ' \
                            'LEFT JOIN albums ON tracks.album_id = albums.id ' \
                            'WHERE albums.start_year BETWEEN 2019 AND 2020'

#3
avr_dur_tracks_by_albums = 'SELECT albums.name, AVG(tracks.duration) FROM albums ' \
                                'LEFT JOIN tracks ON albums.id = tracks.album_id GROUP BY albums.name'

#4
artist_not_20 ='SELECT name FROM artists ' \
                    'LEFT JOIN albums_artists ON artists.id = albums_artists.artist_id ' \
                    'WHERE albums_artists.album_id NOT IN ' \
                        '(SELECT id FROM albums WHERE albums.start_year = 2020)'

#5
specific_artist = "SELECT collections.name FROM collections " \
                    "LEFT JOIN collections_tracks ON collections.id = collections_tracks.collection_id " \
                    "LEFT JOIN tracks ON tracks.id = collections_tracks.track_id " \
                    "LEFT JOIN albums ON albums.id = tracks.album_id " \
                    "LEFT JOIN albums_artists ON albums.id = albums_artists.album_id " \
                    "LEFT JOIN artists ON artists.id = albums_artists.artist_id " \
                    "WHERE artists.name = 'Artik'"

#6
plst_with_artist_more_1_genre = 'SELECT albums.name from albums ' \
                                    'LEFT JOIN albums_artists ON albums.id = albums_artists.album_id ' \
                                    'LEFT JOIN genres_artists ON albums_artists.artist_id = genres_artists.artist_id ' \
                                    'GROUP BY albums.name ' \
                                    'HAVING COUNT(genres_artists.genre_id) > 1'

#7
tracks_not_in_playlists = 'SELECT name  FROM tracks ' \
                                'LEFT JOIN collections_tracks ON tracks.id = collections_tracks.track_id ' \
                                'WHERE collections_tracks.track_id IS NULL ORDER BY name'

#8
artist_min_track = 'SELECT artists.name FROM artists ' \
                        'LEFT JOIN albums_artists ON artists.id = albums_artists.artist_id ' \
                        'LEFT join ALBUMS ON albums.id = albums_artists.album_id ' \
                        'LEFT JOIN tracks ON tracks.album_id = albums.id ' \
                        'WHERE tracks.duration = (SELECT MIN(tracks.duration) FROM tracks)'

#9
albums_min_tracks = 'SELECT albums.name FROM albums ' \
                        'LEFT JOIN tracks ON albums.id = tracks.album_id ' \
                        'GROUP BY albums.name ' \
                        'HAVING COUNT(tracks.id) = (' \
                            'select COUNT(album_id) as count from tracks GROUP BY album_id ORDER BY count LIMIT 1)'