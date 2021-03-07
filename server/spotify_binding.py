import io
import syslog
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image


def get_spotify_client():
    auth_manager = SpotifyOAuth(
        show_dialog=True, open_browser=False, scope="user-read-currently-playing"
    )

    return spotipy.Spotify(auth_manager=auth_manager)


class SpotifyBinding:
    def __init__(self, panel):
        self.panel = panel
        self.current_id = None
        self.spotify = get_spotify_client()
        self.bind()

    def bind(self):
        while True:
            try:
                album_id = self.set_cover()
                if album_id is None:
                    self.panel.clear()
                    self.current_id = None
                else:
                    self.current_id = album_id
            except Exception as e:
                syslog.syslog(syslog.LOG_ERR, str(e))
                print(e)
            finally:
                time.sleep(0.5)

    def set_cover(self):
        current_track = self.get_current_track()
        if current_track is None:
            return None

        album = current_track['item']['album']
        album_id = album['id']

        if album_id == self.current_id:
            return album_id

        cover = self.extract_cover_url(current_track)
        thumbnail = self.get_cover_thumbnail(cover)
        self.panel.draw(thumbnail)

        return album_id

    def get_current_track(self):
        track = self.spotify.current_user_playing_track()
        return track or None

    def extract_cover_url(self, track):
        try:
            cover = track["item"]["album"]["images"][-1]["url"]
            return cover
        except:
            return None

    def get_cover_thumbnail(self, cover_url):
        res = requests.get(cover_url)
        content = res.content

        byte_io = io.BytesIO()
        img_io = io.BytesIO(content)

        im = Image.open(img_io).resize([32, 32])
        im.save(byte_io, format="PPM")

        return byte_io
