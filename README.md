# thirtytwopixels

> RGB LED matrix album art display for mpd+ncmpcpp (and possibly other players)

## Hardware

- Raspberry Pi Zero W
- [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211)
- A 32x32 LED matrix with a HUB75 connection (available on Adafruit and Aliexpress)
- A 5V 4A power adapter

Refer to the [Adafruit instructions](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/) to set it up.
I recommend to do the PWM mod, it completely removed noticeable flicker for me.

## Setup

The project is split into two parts:

- a client that is invoked from `ncmpcpp`'s `execute_song_on_change` callback
- a server that is run on a raspberry pi in your local network

Communication between client and server is handled by a 0MQ TCP socket.

### Client Setup

Clone this repo:

``` sh
git clone https://github.com/fspoettel/thirtytwopixels
```

Install required modules:

```sh
pip3 install -r requirements.txt
```

Add the following line to `~/.ncmpcpp/config`:

```conf
# errors and output is appended to syslog
execute_on_song_change="(path_to_repo/on_song_change.py &> /dev/null &)"
```

Make sure that `./on_song_change.py` is executable:

```sh
chmod +x on_song_change.py
```

If your pi is not using the hostname `raspberrypi.local`, you will need to adjust `ZMQ_HOST` in `./client/matrix.py`.

> ℹ️ It is assumed that `cover.jpg` files are stored in the album folders alongside music files. If that is not the case, you'll need to implement a module analogous to `./client/mpd.py` and call its `get_cover` method in `./on_song_change.py`. The method should return an absolute file system path to an image.

### Server setup

Clone this repo recursively:

```sh
git clone --recursive https://github.com/fspoettel/thirtytwopixels
```

Install required modules:

```sh
pip3 install -r requirements.txt
```

Setup [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix):

```sh
cd matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
```

Set panel options in `server.py`. You probably at least want to touch the pixel mapper config:

```py
def matrix_factory(width):
    options = RGBMatrixOptions()
    # ...
    panel = RGBMatrix(options=options)
    return panel

```

Run the server:

```sh
python3 server/server.py
```
