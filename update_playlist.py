from threeOldThreeNew.instagram_client import InstagramClient
from threeOldThreeNew.spotify_client import SpotifyClient


def add_missing_tracks_to_playlist():
    ic = InstagramClient()
    sp = SpotifyClient()

    recent_posts = ic.get_recent_album_details()
    for post in recent_posts:
        artist = post[0]
        album = post[1]

        album_track_ids = sp.list_track_ids(album, artist)
        if len(album_track_ids) == 0:
            print "NO TRACKS FOUND FOR: %s - %s" % (artist, album)
        else:
            existing_tracks = sp.get_playlist_track_ids()

            # Filter for existing tracks
            new_track_ids = []
            for track_id in album_track_ids:
                if track_id not in existing_tracks:
                    new_track_ids.append(track_id)

            if len(new_track_ids):
                sp.add_tracks(new_track_ids)


if __name__ == '__main__':
    add_missing_tracks_to_playlist()
