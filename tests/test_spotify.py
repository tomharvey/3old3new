from threeOldThreeNew.spotify_client import SpotifyClient
from unittest import main, TestCase


class SpotifyBaseTest(TestCase):
    def setUp(self):
        self.spotify_client = SpotifyClient()
        self.album_name = "Daily Operation"
        self.artist_name = "Gang Starr"

    def test_00_search_album(self):
        dOps = self.spotify_client.search_album(self.album_name,
                                                self.artist_name)
        self.assertTrue(dOps['uri'] == 'spotify:album:74DwNAuirHLDLVLrBQAnVg')

    def test_01_get_album(self):
        gang = self.spotify_client.get_album(self.album_name,
                                             self.artist_name)
        self.assertTrue(gang['id'] == '74DwNAuirHLDLVLrBQAnVg')
        self.assertTrue(len(gang['tracks']['items']) == 18)
        self.assertTrue(gang['name'] == 'Daily Operation')
        self.assertTrue(gang['artists'][0]['name'] == "Gang Starr")
        self.assertTrue(len(gang['artists']) == 1)

    def test_02_get_tracks(self):
        tracks = self.spotify_client.get_album_tracks(self.album_name,
                                                      self.artist_name)
        self.assertTrue(tracks['total'] == 18)
        self.assertTrue(len(tracks['items']) == 18)

    def test_03_list_track_ids(self):
        ids = self.spotify_client.list_track_ids(self.album_name,
                                                 self.artist_name)
        self.assertTrue(len(ids) == 18)

    def test_04_get_playlist(self):
        play = self.spotify_client.get_playlist()
        self.assertTrue(play['name'] == '3old3new')

    def test_05_get_playlist_track_ids(self):
        track_ids = self.spotify_client.get_playlist_track_ids()
        self.assertTrue(len(track_ids) > 0)

if __name__ == '__main__':
    main()
    #import pdb;pdb.set_trace()
