from threeOldThreeNew.settings import (INSTAGRAM_AUTH,
                                       INSTAGRAM_USER,
                                       TARGET_TAG)
from instagram.client import InstagramAPI
from urlparse import parse_qs


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
        get_media, next_page = self.api.user_recent_media(user_id=user_id,
                                                          count=30)
        media = get_media
        while next_page:  # Paginate using the query string returned
            qry_str = next_page.split("?")[-1]
            max_id = parse_qs(qry_str)['max_id'][0]
            get_media, next_page = self.api.user_recent_media(user_id=user_id,
                                                              count=30,
                                                              max_id=max_id)
            media = media + get_media

        return media

    def get_recent_album_details(self):
        # Add the album artist details to self.recent_albums
        recent_media = []
        for media in self.recent_media():
            try:
                caption_text = media.caption.text
                artist, album = self.parse_name(caption_text)
            except AttributeError:
                print "Cannot get caption text for %s" % media.link
                artist, album = (None, None)
            if artist and album:
                recent_media.append((artist, album))
        return recent_media

    def parse_name(self, comment_text):
        # Parse album and artist from the comment
        try:
            tag, artist, album = comment_text.split("-")
            if tag.strip() != TARGET_TAG:
                raise ValueError  # lazy way to skip non 3old3new posts
        except ValueError:
            # if there are too few dashes, move on
            print "Cannot parse %s " % comment_text
            return [None, None]

        return artist.strip(), album.strip()
