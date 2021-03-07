# thirtytwopixels

<div>
    <img height="400" src="./assets/build_dark.jpg" alt="Finished build in a dark room" />
</div>

> wireless LED album art display

Supported players:
- [mpd](https://www.musicpd.org/)+[ncmpcpp](https://wiki.archlinux.org/index.php/ncmpcpp)
- spotify
- other players via the command-line interface

## Hardware

- Raspberry Pi Zero WH
- [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211)
- A 32x32 LED matrix with a HUB75 connection (available on e.g. Adafruit, Pimoroni, Aliexpress). I used [this one](https://shop.pimoroni.com/products/rgb-led-matrix-panel?variant=35962488650).
- A 5V 4A power adapter

Refer to the [Adafruit instructions](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/) to set it up.
I recommend to do [the PWM mod](https://github.com/hzeller/rpi-rgb-led-matrix#improving-flicker), it removed noticeable flicker for me. This requires minor soldering.

## Setup

The project is split into two parts:

- a `server` script that runs on a raspberry pi connected to the LED matrix
- a client script that is invoked from `ncmpcpp`'s config hooks and a CLI. Communication between client and server is handled by a 0MQ TCP socket.

### Client

Clone this repo:

``` sh
git clone https://github.com/fspoettel/thirtytwopixels
```

Install required modules:

```sh
pip3 install -r requirements.txt
```

#### Command-line interface (CLI)

- `python3 scripts/show.py <path_to_image>` displays an arbitrary image
- `python3 scripts/clear.py` clears the display

#### MPD integration

Add the following lines to `~/.ncmpcpp/config`:

```conf
# errors and output is appended to syslog
execute_on_song_change="(path_to_repo/scripts/on_song_change.py &> /dev/null &)"
execute_on_player_state_change = "(path_to_repo/scripts/on_player_state_change.py &> /dev/null &)"
```

Make sure that our hooks are executable:

```sh
chmod +x scripts/on_song_change.py
chmod +x scripts/on_player_state_change.py
```

If your pi is not using the host name `raspberrypi.local`, you will need to adjust `ZMQ_HOST` in `./client/matrix_connection.py`.

> ℹ️ It is assumed that `cover.{jpg,png}` files are stored in the album folders alongside music files. If that is not the case, you'll need to implement a module analogous to `./client/mpd.py` and call its `get_cover` method in `./scripts/on_song_change.py`. The method should return an absolute file system path to an image.

### Server (Raspberry Pi)

Install raspbian on your pi and connect it to your network. ssh into it and make sure the following packages are installed:

```sh
sudo apt install python3 pip3 git libjpeg-dev
```

Clone this repo **recursively** to include the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) submodule:

```sh
git clone --recursive https://github.com/fspoettel/thirtytwopixels
```

Install required modules. Note that the script **needs to use** sudo to interface with the hardware:

```sh
cd thirtytwopixels
sudo pip3 install -r requirements.txt
```

Setup [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix). This may take a while to complete.

```sh
cd matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
```

Set / adjust panel options in `server/matrix_factory.py`:

```py
def matrix_factory(width):
    options = RGBMatrixOptions()
    # ...
    panel = RGBMatrix(options=options)
    return panel

```

Run the server:

```sh
sudo python3 server/server.py
```

You can now send test images to the panel via the cli. Once you are happy with the panel config, you can add the server as a `systemd` service which is started at startup. To do that, create the following file at `/etc/systemd/system/thirtytwopixels.service`:

```sh
[Unit]
Description=thirtytwopixels tcp server

[Service]
ExecStart=/usr/bin/python3 /usr/local/lib/thirtytwopixels/server/server.py

[Install]
WantedBy=default.target
```

and move the repo to `/usr/local/lib/`:

```sh
mv thirtytwopixels /usr/local/lib/
sudo chown root:root /usr/local/lib/thirtytwopixels/server/server.py
sudo chmod 644 /usr/local/lib/thirtytwopixels/server/server.py
```

You can then enable the service via:

```sh
sudo systemctl enable thirtytwopixels.service
```

### Spotify

> Caution: the cli and socket interface currently will not work if you are using spotify. If this is an issue for you, please open a feature request.

Create a [spotify application](https://developer.spotify). As redirect_url, set `http://localhost:9090/callback`. (feel free to change, it doesn't matter)
Then run:

``` sh
export SPOTIPY_CLIENT_ID=<app client id>
export SPOTIPY_CLIENT_SECRET=<app client secret>
export SPOTIPY_REDIRECT_URI="http://localhost:9090/callback"
./scripts/spotify_login.py
```

Open the displayed URL in your local browser and log into spotify. It redirects you to a non-existing `http://localhost:9090/callback` URL with some query params. Copy the URL and past it into the ssh terminal. If it worked, the message _Succesfully logged in as user {you}_ should be displayed and a file `.cache` should be added in the repository root.

Edit the service to include spotify credentials. Run `sudo systemctl edit thirtytwopixels.service` and set enter the 

```
[Service]
WorkingDirectory=/usr/local/lib/thirtytwopixels
Environment="SPOTIPY_CLIENT_ID=<app client id>"
Environment="SPOTIPY_CLIENT_SECRET=<app client secret>"
Environment="SPOTIPY_REDIRECT_URI=http://localhost:9090/callback"
```

Edit `./server/server.py`, comment out the line `provider = SocketBinding(panel)` and uncomment the line `provider = SpotifyBinding(panel)`.

Restart the server:

```sh
sudo systemctl restart thirtytwopixels.service
```

## Pictures

<div align="center">
    <img src="./assets/build_light.jpg" alt="Finished build in a light room" />
</div>

<div align="center">
    <img src="./assets/build_back.jpg" alt="Back of finished build" />
</div>

## In the wild

- [Hackaday article](https://hackaday.com/2020/10/11/lo-fi-art-on-a-32x32-matrix/)
- [flipflip's AlbumArtDisplay](https://github.com/phkehl/AlbumArtDisplay) using ESP32 and Arduino
- Built something? [Add it!](https://github.com/fspoettel/thirtytwopixels/edit/master/README.md)
