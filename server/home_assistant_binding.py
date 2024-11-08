import requests
import io
import os
import time
import syslog
from PIL import Image

class HomeAssistantBinding:
    def __init__(self, panel):
        base_url = os.getenv("HA_BASE_URL")
        entity_id = os.getenv('HA_ENTITY_ID')
        token = os.getenv('HA_TOKEN')
        if not base_url or not entity_id or not token:
            raise ValueError("base_url, entity_id, and token must be specified")

        self.panel = panel
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/states/{entity_id}"
        self.token = token
        self.album_art_url = None
        self.cached_byte_io = None
        self.cached_url = None
        self.bind()

    def bind(self):
        while True:
            try:
                album_art_url = self.set_cover()
                if album_art_url is None:
                    self.panel.clear()
                    self.album_art_url = None
                else:
                    self.album_art_url = album_art_url
            except Exception as e:
                syslog.syslog(syslog.LOG_ERR, str(e))
                print(e)
            finally:
                time.sleep(1)

    def set_cover(self):
        album_art_url = self.fetch_album_art()
        if album_art_url:
            thumbnail = self.get_cover_thumbnail(album_art_url)
            self.panel.draw(thumbnail)
        return album_art_url

    def fetch_album_art(self):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(self.api_url, headers=headers)
        album_art_url = None
        if response.status_code == 200:
            data = response.json()
            if 'entity_id' not in data:
                syslog.syslog(syslog.LOG_ERR, "Entity not found.")
                return None
            if 'entity_picture' in data['attributes']:
                state = data['state']
                if state == "idle":
                    return None
                elif state == "playing":
                    album_art_url = data['attributes']['entity_picture']
                    if album_art_url.startswith('/api/'):
                        album_art_url = f"{self.base_url}{album_art_url}"
        else:
            syslog.syslog(syslog.LOG_ERR, "Failed to fetch data from Home Assistant API: {response.status_code}")
        return album_art_url

    def get_cover_thumbnail(self, cover_url):
        if cover_url == self.cached_url:
            return self.cached_byte_io

        res = requests.get(cover_url)
        content = res.content

        byte_io = io.BytesIO()
        img_io = io.BytesIO(content)

        im = Image.open(img_io).resize([self.panel.matrix.width, self.panel.matrix.height])
        im.save(byte_io, format="PPM")

        self.cached_byte_io = byte_io
        self.cached_url = cover_url

        return byte_io