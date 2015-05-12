from threeOldThreeNew.settings import SPOTIFY_AUTH, TARGET_PLAYLIST
from spotipy import Spotify, util


class SpotifyClient:
    def __init__(self):
        token = self.get_token()
        self.sp = Spotify(auth=token)

    def get_token(self):
        scope = 'playlist-modify-private'
        return util.prompt_for_user_token(
            SPOTIFY_AUTH['USERNAME'],
            scope,
            client_id=SPOTIFY_AUTH['CLIENT_ID'],
            client_secret=SPOTIFY_AUTH['CLIENT_SECRET'],
            redirect_uri=SPOTIFY_AUTH['REDIRECT_URI'])

    def search_album(self, album_name, artist_name):
        results = self.sp.search(q=album_name, limit=20, type="album")
        for album in results["albums"]["items"]:
            if 'GB' in album['available_markets']:
                return album

    def get_album(self, album_name, artist_name):
        album_id = self.search_album(album_name, artist_name)
        try:
            return self.sp.album(album_id['uri'])
        except TypeError:
            return {"tracks": []}

    def get_album_tracks(self, album_name, artist_name):
        try:
            return self.get_album(album_name, artist_name)['tracks']
        except TypeError:
            return None

    def list_track_ids(self, album_name, artist_name):
        track_ids = []
        album_items = self.get_album_tracks(album_name, artist_name)
        if album_items:
            for track in album_items['items']:
                track_ids.append(track['id'])
        return track_ids

    def get_playlist(self):
        return self.sp.user_playlist(SPOTIFY_AUTH['USERNAME'], TARGET_PLAYLIST)

    def get_playlist_track_ids(self):
        track_ids = []
        offset = 0
        tracks = self.sp.user_playlist_tracks(
            SPOTIFY_AUTH['USERNAME'], TARGET_PLAYLIST, None, 100, offset)

        track_items = tracks['items']
        while tracks['next']:  # Paginate
            offset = offset + 100
            tracks = self.sp.user_playlist_tracks(
                SPOTIFY_AUTH['USERNAME'], TARGET_PLAYLIST, None, 100, offset)
            track_items = track_items + tracks['items']

        if len(track_items) > 0:
            for track in track_items:
                track_ids.append(track["track"]['id'])
        return track_ids

    def add_tracks(self, track_id_list):
        playlist_id = self.get_playlist()['id']
        self.sp.user_playlist_add_tracks(SPOTIFY_AUTH['USERNAME'],
                                         playlist_id,
                                         track_id_list)
