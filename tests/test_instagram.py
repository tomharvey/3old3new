from threeOldThreeNew.instagram_client import InstagramClient
from unittest import main, TestCase


class InstagramBaseTest(TestCase):
    def setUp(self):
        self.instagram_client = InstagramClient()

    def test_00_search_user(self):
        tomg = self.instagram_client.search_user()
        self.assertTrue(len(tomg) == 1)

    def test_01_get_user_id(self):
        tomg_id = self.instagram_client.get_user_id()
        self.assertTrue(tomg_id > 0)

    def test_02_parse_name(self):
        standard = "#3old3new - Gang Starr - Daily Operation"
        ar, al = self.instagram_client.parse_name(standard)
        self.assertTrue(ar == "Gang Starr")
        self.assertTrue(al == "Daily Operation")

        # return None if the dashes are too few
        whack = "#3old3new - Gang Starr"
        ar, al = self.instagram_client.parse_name(whack)
        self.assertIsNone(ar)
        self.assertIsNone(al)

        # return None if the tag is not #3old3new
        whack = "#4old4new - Gang Starr - Daily Operation"
        ar, al = self.instagram_client.parse_name(whack)
        self.assertIsNone(ar)
        self.assertIsNone(al)

    def test_03_get_recent_albums(self):
        recent_media = self.instagram_client.get_recent_album_details()
        self.assertTrue(len(recent_media) > 0)


if __name__ == '__main__':
    main()
