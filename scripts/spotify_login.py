#!/usr/bin/env python3
import io
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

auth_manager=SpotifyOAuth(
    show_dialog=True,
    open_browser=False,
    scope='user-read-currently-playing'
)

sp = spotipy.Spotify(auth_manager=auth_manager)
user = sp.current_user()

print("Succesfully logged in as user {}.".format(user['display_name']))
