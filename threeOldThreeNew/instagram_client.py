from threeOldThreeNew.settings import (INSTAGRAM_AUTH,
                                       INSTAGRAM_USER,
                                       MEDIA_COUNT)
from instagram.client import InstagramAPI


class InstagramClient:
    """ Find muscal user's recent posts
        return a list of album and artist names.
    """
    def __init__(self):
        # Make an unauthenticated connection
        self.api = InstagramAPI(
            client_id=INSTAGRAM_AUTH['CLIENT_ID'],
            client_secret=INSTAGRAM_AUTH['CLIENT_SECRET'])

    def search_user(self):
        # Find the user based on settings
        return self.api.user_search(q=INSTAGRAM_USER)

    def get_user_id(self):
        # Convert the user name specified into a user_id
        return self.search_user()[0].id

    def recent_media(self):
        # Get a list of the most recent posts.
        user_id = self.get_user_id()
        get_media = self.api.user_recent_media(user_id=user_id,
                                               count=MEDIA_COUNT)
        media = get_media[0]

        if len(media) < MEDIA_COUNT:
            self.get_more_media(media, get_media[1])

        return media

    def get_recent_album_details(self):
        # Add the album artist details to self.recent_albums
        recent_media = []
        for media in self.recent_media():
            artist, album = self.parse_name(media.caption.text)
            if artist and album:
                recent_media.append((artist, album))
        return recent_media

    def parse_name(self, comment_text):
        # Parse album and artist from the comment
        try:
            tag, artist, album = comment_text.split("-")
            if tag.strip() != "#3old3new":
                raise ValueError  # lazy way to skip non 3old3new posts
        except ValueError:
            # if there are too few dashes, move on
            return [None, None]

        return artist.strip(), album.strip()

    def get_more_media(self, media, pagination):
        # TODO, not sure what the max count is here
        return media
