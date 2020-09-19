# thirtytwopixels

> RGB matrix album art display for mpd+ncmpcpp (and possibly other players)

## Hardware

- Raspberry Pi Zero W
- [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211)
- A 32x32 LED matrix (available on Adafruit and Aliexpress)
- A 5V 4A power adapter

Refer to the Adafruit instructions to set this up.

## Setup

The project is split into two parts:

- a client that is invoked from `ncmpcpp`'s `execute_song_on_change` callback
- a server that is run on a raspberry pi in your local network

Communication between clients / server is handled by a 0MQ TCP socket.

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
execute_on_song_change="(path_to_repo/on_song_change.py &> /dev/null &)"
```

Make sure that `./on_song_change.py` is executable:

```sh
chmod +x on_song_change.py
```

If your pi is not using the hostname `raspberrypi.local`, you will need to adjust `ZMQ_HOST` in `./client/matrix.py`.

> ℹ️ The client assumes that `cover.jpg` files are stored in the album folders alongside files. If that is not the case, you'll need to implement a module analogous to `./client/mpd.py` and call its `get_cover` method in `./on_song_change.py`. The method should return an absolute file system path to an image.

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

Run the server:

```sh
python3 server/server.py
```
