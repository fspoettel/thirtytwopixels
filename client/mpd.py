import os
from pathlib import Path
from subprocess import check_output


# @see https://beets.readthedocs.io/en/stable/plugins/fetchart.html
COVER_NAME = "cover.jpg"
MUSIC_DIR = os.getenv("DIR_BEETS")


def get_playback_file():
    state = check_output(["mpc", "--format", "%file%", "current"]).decode("utf-8")

    lines = state.splitlines()[:1]
    if lines:
        file = Path(MUSIC_DIR) / lines[0]
        # mpd may be playing a file outside of `MUSIC_DIR`
        return file if file.exists() else None

    return None


def get_parent_dir(file):
    return file.resolve().parent if file else None


def get_cover_file(directory):
    cover_path = directory / COVER_NAME
    if not cover_path.is_file():
        raise ValueError("No cover found")
    return cover_path


def get_cover():
    file = get_playback_file()
    if not file:
        raise IOError("Nothing is currently playing.")

    album = get_parent_dir(file)
    if not album:
        raise ValueError("Could not locate current playback in directory.")

    return get_cover_file(album)
