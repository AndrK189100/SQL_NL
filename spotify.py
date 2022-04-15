import base64
import requests
import time


class Spotify:

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token = self.__get_token__()

    def __get_token__(self):

        auth = str(base64.b64encode((self.__client_id + ':' + self.__client_secret).encode('ascii')))[2:-1]

        params = {'grant_type': 'client_credentials'}
        headers = {'Authorization': 'Basic ' + auth, 'Content-Type': 'application/x-www-form-urlencoded'}
        url = 'https://accounts.spotify.com/api/token'
        return requests.post(url=url, params=params, headers=headers).json()['access_token']

    def get_playlists(self, playlist_ids: list, limit: int = 5):
        url = 'https://api.spotify.com/v1/'
        headers = {'Authorization': 'Bearer ' + self.__token, 'Content-Type': 'application/json'}
        params = {'limit': '50'}
        #db_data = {}
        db = []
        playlist_release = 2016
        for id in playlist_ids:


            while True:
                resp = requests.get(url=url + 'playlists/' + id, headers=headers)
                if resp.status_code == 200:
                    break
                time.sleep(3)

            playlist = resp.json()
            #track_data = {}
            i = 0
            for track in playlist['tracks']['items']:
                arts = track['track']['artists']
                artists = {}
                for art in arts:

                    url_art = url + 'artists/' + art['id']

                    while True:
                        resp = requests.get(url=url_art, headers=headers)
                        if resp.status_code == 200:
                            break
                        time.sleep(3)

                    art_genre = resp.json()['genres']
                    artists[art['name']] = art_genre

                record = {'playlist': playlist['name'],
                          'playlist_release': playlist_release,
                          'album': track['track']['album']['name'],
                          'album_release': track['track']['album']['release_date'],
                          'track': track['track']['name'],
                          'duration': track['track']['duration_ms'],
                          'artists': artists}

                # track_data[track['track']['name']] = {'album': track['track']['album']['name'],
                #                                       'album_rel': track['track']['album']['release_date'],
                #                                       'duration': track['track']['duration_ms'],
                #                                       'artists': artists}

                db.append(record)
                i += 1
                if i == limit:
                    break
            playlist_release += 1
            #db_data[playlist['name']] = track_data
            #time.sleep(20)
        return db
